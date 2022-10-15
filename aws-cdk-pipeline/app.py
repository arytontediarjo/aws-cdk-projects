#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_cdk_pipeline.aws_cdk_pipeline_stack import AwsCdkPipelineStack



app = cdk.App()
AwsCdkPipelineStack(app, "AwsCdkPipelineStack", 
    env=cdk.Environment(account="939927276846", region="us-east-1")
)

app.synth()
