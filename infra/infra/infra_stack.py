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


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        docs_bucket = s3.Bucket(
            self,
            "AwsenseDocsBucket",
            bucket_name=f"awsense-docs-{self.account}-{self.region}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        chatbot_lambda = _lambda.Function(
            self,
            "AwsenseLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="src.handler.lambda_handler",
            code=_lambda.Code.from_asset("../backend"),
            timeout=Duration.seconds(30),
            memory_size=1024,
        )

        api = apigw.RestApi(
            self,
            "AwsenseApi",
            rest_api_name="AWSense API",
        )

        health = api.root.add_resource("health")
        health.add_method("GET",
                          apigw.LambdaIntegration(chatbot_lambda)) # type: ignore
        chat = api.root.add_resource("chat")
        chat.add_method(
            "POST",
            apigw.LambdaIntegration(chatbot_lambda))  # type: ignore
        CfnOutput(
            self,
            "ApiUrl",
            value=api.url
        )
