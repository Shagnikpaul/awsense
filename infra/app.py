#!/usr/bin/env python3
import os
import aws_cdk as cdk
from infra.infra_stack import InfraStack
from dotenv import load_dotenv
load_dotenv()

app = cdk.App()
InfraStack(
    app,
    "AWSenseStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION")
    ),
    api_key=os.getenv("API_KEY"),
    groq_api_key=os.getenv("GROQ_API_KEY"),
    hf_token=os.getenv("HF_TOKEN")
    
)
app.synth()
