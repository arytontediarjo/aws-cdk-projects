import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Amazon S3
AmazonS3_node1664249879662 = glueContext.create_dynamic_frame.from_catalog(
    database="medium_glue_db",
    table_name="employees",
    transformation_ctx="AmazonS3_node1664249879662",
)

# Script generated for node Select Fields
SelectFields_node1664207891801 = SelectFields.apply(
    frame=AmazonS3_node1664249879662,
    paths=[
        "employeeid",
        "firstname",
        "postalcode",
        "region",
        "city",
        "address",
        "hiredate",
        "birthdate",
        "titleofcourtesy",
        "title",
        "lastname",
    ],
    transformation_ctx="SelectFields_node1664207891801",
)

# Script generated for node Amazon S3
AmazonS3_node1664209632477 = glueContext.write_dynamic_frame.from_options(
    frame=SelectFields_node1664207891801,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://medium1997-glue-db/etl-output/",
        "partitionKeys": ["region"],
    },
    format_options={"compression": "snappy"},
    transformation_ctx="AmazonS3_node1664209632477",
)

job.commit()
