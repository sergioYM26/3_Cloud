import os
from constructs import Construct
import aws_cdk.aws_apigateway as apigateway
from config import SYWallaConfig
from api.create_lambdas import ApiLambdas

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
        images_bucket: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambdas = ApiLambdas(
            self,
            config=config,
            ads_table=ads_table,
            images_bucket=images_bucket,
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
            deploy_options=apigateway.StageOptions(
                stage_name=config.stage,
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
            self.lambdas.list_ads,
            integration_responses=[default_integration_response],
        )
        create_ad_integration = apigateway.LambdaIntegration(
            self.lambdas.create_ad,
            integration_responses=[default_integration_response],
        )

        get_ad_integration = apigateway.LambdaIntegration(
            self.lambdas.get_ad,
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
        ad_id_resource = ad_resource.add_resource("{ad_id}")
        ad_id_resource.add_method(
            "GET",
            get_ad_integration,
            method_responses=[default_method_response],
        )

        # Comments - Integrations
        post_comment_integration = apigateway.LambdaIntegration(
            self.lambdas.post_comment,
            integration_responses=[default_integration_response],
        )

        # Comments - resources
        comment_resource = ad_id_resource.add_resource("comment")
        comment_resource.add_method(
            "POST",
            post_comment_integration,
            method_responses=[default_method_response],
        )

        # Chat - Integrations
        get_chat_messages_integration = apigateway.LambdaIntegration(
            self.lambdas.get_chat_messages,
            integration_responses=[default_integration_response],
        )

        post_chat_message_integration = apigateway.LambdaIntegration(
            self.lambdas.post_chat_message,
            integration_responses=[default_integration_response],
        )

        # Chat - resources
        chat_resource = api.root.add_resource("chat")
        chat_id_resource = chat_resource.add_resource("{chat_id}")
        chat_id_resource.add_method(
            "GET",
            get_chat_messages_integration,
            method_responses=[default_method_response],
        )
        chat_id_resource.add_method(
            "POST",
            post_chat_message_integration,
            method_responses=[default_method_response],
        )
