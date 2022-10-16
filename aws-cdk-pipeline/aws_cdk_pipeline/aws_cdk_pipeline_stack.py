import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

class AwsCdkPipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline =  CodePipeline(self, "Pipeline", 
                        pipeline_name="AwsCdkPipeline",
                        synth=ShellStep("Synth", 
                            input=CodePipelineSource.git_hub("arytontediarjo/aws-cdk-projects", "main"),
                            commands=[
                                "cd aws_cdk_pipeline",
                                "npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt", 
                                "cdk synth"]
                        )
                    )