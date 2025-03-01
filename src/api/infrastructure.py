import os
import aws_cdk as cdk
import aws_cdk.aws_apigateway as apigateway
from aws_cdk.aws_cognito import UserPool
from constructs import Construct


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
        user_pool: UserPool,
        ads_table: str,
        comments_table: str,
        images_bucket: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambdas = ApiLambdas(
            self,
            config=config,
            ads_table=ads_table,
            comments_table=comments_table,
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

        authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self,
            f"{config.name}-{config.stage}-authorizer",
            authorizer_name=f"{config.name}-{config.stage}-authorizer",
            cognito_user_pools=[user_pool],
            identity_source="method.request.header.Authorization",
            results_cache_ttl=cdk.Duration.minutes(5),
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
        ad_resource = api.root.add_resource("ads")
        ad_resource.add_method(
            "GET",
            list_ads_integration,
            method_responses=[default_method_response],
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorization_scopes=["openid", "email", "profile"],
        )
        ad_resource.add_method(
            "POST",
            create_ad_integration,
            method_responses=[default_method_response],
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorization_scopes=["openid", "email", "profile"],
        )
        ad_id_resource = ad_resource.add_resource("{ad_id}")
        ad_id_resource.add_method(
            "GET",
            get_ad_integration,
            method_responses=[default_method_response],
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorization_scopes=["openid", "email", "profile"],
        )

        # Comments - Integrations
        post_comment_integration = apigateway.LambdaIntegration(
            self.lambdas.post_comment,
            integration_responses=[default_integration_response],
        )

        # Comments - resources
        comment_resource = ad_id_resource.add_resource("comments")
        comment_resource.add_method(
            "POST",
            post_comment_integration,
            method_responses=[default_method_response],
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorization_scopes=["openid", "email", "profile"],
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
        chat_resource = api.root.add_resource("chats")
        chat_id_resource = chat_resource.add_resource("{chat_id}")
        chat_id_resource.add_method(
            "GET",
            get_chat_messages_integration,
            method_responses=[default_method_response],
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorization_scopes=["openid", "email", "profile"],
        )
        chat_id_resource.add_method(
            "POST",
            post_chat_message_integration,
            method_responses=[default_method_response],
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorization_scopes=["openid", "email", "profile"],
        )
