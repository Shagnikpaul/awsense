import boto3



def getCW():    
    cloudwatch = boto3.client("cloudwatch")
    return cloudwatch


def publish_output_tokens(tokens: int):
    getCW().put_metric_data(
        Namespace="AWSense",
        MetricData=[
            {
                "MetricName": "OutputTokens",
                "Value": tokens,
                "Unit": "Count",
            }
        ],
    )
