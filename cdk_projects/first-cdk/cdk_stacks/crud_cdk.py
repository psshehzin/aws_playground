from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    RemovalPolicy
)
from constructs import Construct

class CrudCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        table = dynamodb.Table(
            self, "CrudAppTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Lambda Function
        crud_lambda = _lambda.Function(
            self, "BasicCrud",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="crudapp.handler",
            code=_lambda.Code.from_asset("lambda_functions"),
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        # Lambda Function
        home_lambda = _lambda.Function(
            self, "HomePage",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="helloworld.handler",
            code=_lambda.Code.from_asset("lambda_functions"),
        )

        # Grant DynamoDB Table Permissions to Lambda
        table.grant_read_write_data(crud_lambda)

        # api gateway declaration
        api_items = apigw.LambdaRestApi(
            self, "CrudApi",
            handler=crud_lambda,
            proxy=False
        )
        
        home_integration = apigw.LambdaIntegration(home_lambda)
        api_items.root.add_method("GET", home_integration)
        api_items.root.add_method("POST", home_integration)

        # Resource for /items endpoint
        items = api_items.root.add_resource("items")

        # Lambda Integration for GET and POST /items
        items_integration = apigw.LambdaIntegration(crud_lambda)
        items.add_method("GET", items_integration)
        items.add_method("POST", items_integration)

        
