from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    CfnOutput
)
from constructs import Construct
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_cloudwatch_actions as cw_actions
from aws_cdk import aws_iam as iam

class InfraStack(Stack):

    def __init__(self,
                 scope,
                 construct_id,
                 api_key,
                 groq_api_key,
                 hf_token,
                 **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        docs_bucket = s3.Bucket(
            self,
            "AwsenseDocsBucket",
            bucket_name=f"awsense-docs-{self.account}-{self.region}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        frontend_bucket = s3.Bucket(
            self,
            "AwsenseFrontendBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        throttle_table = dynamodb.Table(
            self,
            "ThrottleTable",
            partition_key=dynamodb.Attribute(
                name="sessionId",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute="ttl",
            removal_policy=RemovalPolicy.DESTROY,  # dev only
        )

        conversations_table = dynamodb.Table(
            self,
            "ConversationsTable",
            table_name="awsense-conversations",
            partition_key=dynamodb.Attribute(
                name="conversationId",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute="ttl",
            removal_policy=RemovalPolicy.DESTROY,  # dev only
        )

        conversations_table.add_global_secondary_index(
            index_name="clientId-updatedAt-index",
            partition_key=dynamodb.Attribute(
                name="clientId",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="updatedAt",
                type=dynamodb.AttributeType.STRING,
            ),
            projection_type=dynamodb.ProjectionType.ALL,
        )     

        chat_messages_table = dynamodb.Table(
            self,
            "ChatMessagesTable",
            table_name="awsense-chat-messages",
            partition_key=dynamodb.Attribute(
                name="conversationId",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute="ttl",
            removal_policy=RemovalPolicy.DESTROY,  # dev only
        )


        distribution = cloudfront.Distribution(
            self,
            "AwsenseFrontendDistribution",

            default_root_object="index.html",

            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(frontend_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
        )

        alert_topic = sns.Topic(
            self,
            "AwsenseAlerts",
            display_name="AWSense Alerts",
        )
        
        alert_topic.add_subscription(
            subscriptions.EmailSubscription(
                "shagnikpaul.772@gmail.com"
            )
        )

        s3deploy.BucketDeployment(
            self,
            "DeployFrontend",
            sources=[s3deploy.Source.asset("../frontend/dist")], 
            destination_bucket=frontend_bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )

        

        chatbot_lambda = _lambda.Function(
            self,
            "AwsenseLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="src.handler.lambda_handler",
            code=_lambda.Code.from_asset("../backend"),
            timeout=Duration.seconds(30),
            memory_size=1024,
            environment={
                "API_KEY": api_key,
                "GROQ_API_KEY": groq_api_key,
                "HF_TOKEN": hf_token,
                "THROTTLE_TABLE_NAME": throttle_table.table_name,
                "LOG_LEVEL": "INFO",
                "CONVERSATIONS_TABLE": conversations_table.table_name,
                "CHAT_MESSAGES_TABLE": chat_messages_table.table_name,
            },
        )
        chatbot_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "cloudwatch:PutMetricData"
                ],
                resources=["*"],
            )
        )
        lambda_error_alarm = cloudwatch.Alarm(
            self,
            "AwsenseLambdaErrors",
            metric=chatbot_lambda.metric_errors(),
            threshold=1,
            evaluation_periods=1,
        )

        lambda_error_alarm.add_alarm_action(
            cw_actions.SnsAction(alert_topic)
        )
        dashboard = cloudwatch.Dashboard(
            self,
            "AwsenseDashboard",
            dashboard_name="AWSenseDashboard",
        )

        # widget 1
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="Lambda Invocations",
                left=[
                    chatbot_lambda.metric_invocations()
                ],
            )
        )

        #widget 2
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="Lambda Errors",
                left=[
                    chatbot_lambda.metric_errors()
                ],
            )
        )

        # widget 3
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="P50 Latency",
                left=[
                    chatbot_lambda.metric_duration(
                        statistic="p50"
                    )
                ],
            )
        )

        #widget 4
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="P95 Latency",
                left=[
                    chatbot_lambda.metric_duration(
                        statistic="p95"
                    )
                ],
            )
        )

        # widget 5
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="Output Tokens",
                left=[
                    cloudwatch.Metric(
                        namespace="AWSense",
                        metric_name="OutputTokens",
                        statistic="Sum",
                    )
                ],
            )
        )
        
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="Throttle Table Reads",
                left=[
                    throttle_table.metric_consumed_read_capacity_units()
                ],
            )
        )

        throttle_table.grant_read_write_data(chatbot_lambda)
        conversations_table.grant_read_write_data(chatbot_lambda)
        chat_messages_table.grant_read_write_data(chatbot_lambda)

        api = apigw.RestApi(
            self,
            "AwsenseApi",
            rest_api_name="AWSense API",
        )

        health = api.root.add_resource(
            "health",
            default_cors_preflight_options={
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "OPTIONS"],
                "allow_headers": [
                    "Content-Type",
                    "x-api-key"
                ],
            },
        )

        health.add_method(
            "GET",
            apigw.LambdaIntegration(chatbot_lambda)  # type: ignore
        )

        chat = api.root.add_resource(
            "chat",
            default_cors_preflight_options={
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": ["POST", "OPTIONS"],
                "allow_headers": [
                    "Content-Type",
                    "x-api-key"
                ],
            },
        )

        chat.add_method(
            "POST",
            apigw.LambdaIntegration(chatbot_lambda)  # type: ignore
        )

        CfnOutput(
            self,
            "ApiUrl",
            value=api.url
        )
        CfnOutput(
            self,
            "FrontendURL",
            value=distribution.domain_name
        )
