from constructs import Construct
from aws_cdk import Duration
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_sqs as sqs
from aws_cdk import aws_sns_subscriptions as sns_subs
from aws_cdk import aws_sns as sns
from aws_cdk import aws_s3_notifications as s3n
from aws_cdk import Stack
from aws_cdk import aws_iam as iam


class APIStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Using pre-created roles to avoid givin iam:CreateRole to lab cdk cfn deploy role
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/CustomizeRolesOptions.html
        iam.Role.customize_roles(
            self,
            use_precreated_roles={
                "APIStack/BucketNotificationsHandler050a0587b7544547bf325f094a3db834/Role": "cdk-apistack-role",
                "APIStack/ImageGetAndSaveLambda/ServiceRole": "cdk-apistack-role",
            },
        )

        bucket = s3.Bucket(self, "CW-Workshop-Images")

        asset_bucket = s3.Bucket.from_bucket_name(
            scope=self,
            id="lamba_layer_zipfile",
            bucket_name="TO BE PROVIDED",
        )

        requests_layer_file = (
            "requests_layer3_11.zip"
        )

        requests = lambda_.LayerVersion(
            self,
            "requests_layer",
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_11],
            layer_version_name="requests_layer",
            code=lambda_.S3Code(bucket=asset_bucket, key=requests_layer_file),
        )

        image_get_and_save_lambda = lambda_.Function(
            self,
            "ImageGetAndSaveLambda",
            function_name="ImageGetAndSaveLambda",
            runtime=lambda_.Runtime.PYTHON_3_11,
            layers=[requests],
            code=lambda_.Code.from_asset("api/runtime"),
            handler="get_save_image.handler",
            environment={"BUCKET_NAME": bucket.bucket_name},
        )

        bucket.grant_read_write(image_get_and_save_lambda)

        api = apigateway.RestApi(
            self,
            "REST_API",
            rest_api_name="Image Upload Service",
            cloud_watch_role=False,
            description="CW workshop - upload image for workshop.",
        )

        get_image_integration = apigateway.LambdaIntegration(
            image_get_and_save_lambda,
            request_templates={"application/json": '{ "statusCode": "200" }'},
        )

        api.root.add_method("GET", get_image_integration)

        upload_queue = sqs.Queue(
            self, id="uploaded_image_queue", visibility_timeout=Duration.seconds(30)
        )

        self.upload_queue_url = upload_queue.queue_url
        self.upload_queue_arn = upload_queue.queue_arn

        sqs_subscription = sns_subs.SqsSubscription(
            upload_queue, raw_message_delivery=True
        )

        upload_event_topic = sns.Topic(self, id="uploaded_image_topic")

        upload_event_topic.add_subscription(sqs_subscription)

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT, s3n.SnsDestination(upload_event_topic)
        )

    @property
    def sqs_url(self) -> str:
        return self.upload_queue_url

    @property
    def sqs_arn(self) -> str:
        return self.upload_queue_arn
