import os
from constructs import Construct
import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_lambda as _lambda
from config import SYWallaConfig

RUNTIME_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/runtime"


class Api(Construct):
    """."""

    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        config: SYWallaConfig,
        ads_table: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.list_ads = _lambda.DockerImageFunction(
            self,
            f"{config.name}-{config.stage}-list-ads-lambda",
            function_name=f"{config.name}-{config.stage}-list-ads-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                f"{RUNTIME_PATH}/list_ads"
            ),
            environment={"TABLE_NAME": ads_table},
        )

        self.create_ad = _lambda.DockerImageFunction(
            self,
            f"{config.name}-{config.stage}-create-ad-lambda",
            function_name=f"{config.name}-{config.stage}-create-ad-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                f"{RUNTIME_PATH}/create_ad"
            ),
            environment={"TABLE_NAME": ads_table},
        )

        # API Gateway REST API
        api = apigateway.RestApi(
            self,
            f"{config.name}-{config.stage}-api",
            rest_api_name=f"{config.name}-{config.stage}-api",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_methods=["GET", "OPTIONS"],
                allow_origins=apigateway.Cors.ALL_ORIGINS,
            ),
        )

        default_integration_response = apigateway.IntegrationResponse(
            status_code="200",
            response_parameters={
                "method.response.header.Access-Control-Allow-Origin": "'*'"
            },
        )
        default_method_response = apigateway.MethodResponse(
            status_code="200",
            response_parameters={
                "method.response.header.Access-Control-Allow-Origin": True
            },
        )

        # Advertisements - Integrations
        list_ads_integration = apigateway.LambdaIntegration(
            self.list_ads,
            integration_responses=[default_integration_response],
        )
        create_ad_integration = apigateway.LambdaIntegration(
            self.create_ad,
            integration_responses=[default_integration_response],
        )

        # Advertisements - resources
        ad_resource = api.root.add_resource("ad")
        ad_resource.add_method(
            "GET",
            list_ads_integration,
            method_responses=[default_method_response],
        )
        ad_resource.add_method(
            "POST",
            create_ad_integration,
            method_responses=[default_method_response],
        )
        ad_id_resource = ad_resource.add_resource("{id}")
        ad_id_resource.add_method("GET")

        # Comments
        comment_resource = ad_id_resource.add_resource("comment")
        comment_resource.add_method("POST")
        comment_resource.add_method("GET")

        # Chat
        chat_resource = api.root.add_resource("chat")
        chat_id_resource = chat_resource.add_resource("{id}")
        chat_id_resource.add_method("POST")
        chat_id_resource.add_method("GET")
