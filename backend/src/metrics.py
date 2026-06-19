import boto3

cloudwatch = boto3.client("cloudwatch")


def publish_output_tokens(tokens: int):
    cloudwatch.put_metric_data(
        Namespace="AWSense",
        MetricData=[
            {
                "MetricName": "OutputTokens",
                "Value": tokens,
                "Unit": "Count",
            }
        ],
    )