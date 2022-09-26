"""
This script is used for creating AWS stack 
connecting S3 bucket to Glue
"""
from constructs import Construct
from aws_cdk import (
    Aws,
    Stack,
    CfnOutput,
    Duration,
    aws_s3 as s3,
    aws_iam as iam,
    aws_s3_deployment as s3deploy,
    aws_glue as glue,
    aws_stepfunctions as sf,
    aws_stepfunctions_tasks as tasks,

)

"""
Get current AWS configuration
region and account id
"""
AWS_REGION = Aws.REGION
AWS_ACCOUNT_ID = Aws.ACCOUNT_ID
BUCKET_NAME = 'medium1997-glue-db'
BUCKER_URI = f"s3://{BUCKET_NAME}/" # bucket path
GLUE_DB_NAME = "medium_glue_db"
GLUE_CRAWLER_NAME = 'medium_bucket_crawler'


class AwsGlueEtlStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """
        This script is used to create a service role 
        that will be attached to a glue crawler
        """
        glue_job_role = iam.Role(
            self,
            'Glue-Job-Role',
            assumed_by=iam.ServicePrincipal('glue.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSGlueServiceRole')]
        )

        """
        code chunk to create S3 bucket
        """
        bucket = s3.Bucket(
            self,
            "createBucket",
            bucket_name=BUCKET_NAME)

        """
        code chunk to create glue database
        """
        glue_db = glue.CfnDatabase(
            self,
            id="createGlueDatabase",
            catalog_id=AWS_ACCOUNT_ID,
            database_input=glue.CfnDatabase.DatabaseInputProperty(
                description=f"Glue database '{GLUE_DB_NAME}'",
                name=GLUE_DB_NAME
            )
        )

        """
        Below will be the code chunk to create crawler that will be pointed to the S3 buckets
        """
        # this code will create the target S3 bucket where the crawler will be running
        targets_property = glue.CfnCrawler.TargetsProperty(
            s3_targets=[glue.CfnCrawler.S3TargetProperty(
                path=BUCKER_URI
            )]
        )

        # this code will create the crawler
        myCrawler = glue.CfnCrawler(
            self,
            'createGlueCrawler',
            name=GLUE_CRAWLER_NAME,
            database_name=GLUE_DB_NAME,
            role=glue_job_role.role_arn,
            targets=targets_property
        )
