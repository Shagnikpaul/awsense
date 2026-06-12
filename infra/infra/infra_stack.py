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


        distribution = cloudfront.Distribution(
            self,
            "AwsenseFrontendDistribution",

            default_root_object="index.html",

            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(frontend_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
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
            },
        )

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
