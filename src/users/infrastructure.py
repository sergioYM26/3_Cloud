from constructs import Construct
import aws_cdk as cdk
import aws_cdk.aws_cognito as cognito

from config import SYWallaConfig


class Users(Construct):
    def __init__(
        self, scope: Construct, id: str, *, config: SYWallaConfig, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.user_pool = cognito.UserPool(
            self,
            f"{config.name}-{config.stage}-user-pool",
            user_pool_name=f"{config.name}-{config.stage}-user-pool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(username=True, email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True)
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_digits=True,
                require_lowercase=True,
                require_uppercase=True,
                require_symbols=True,
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        # Advertisers Group
        self.advertisers_group = self.user_pool.add_group(
            f"{config.name}-{config.stage}-advertisers-group",
            group_name="advertisers-group",
        )

        # Consumers Group
        self.consumers_group = self.user_pool.add_group(
            f"{config.name}-{config.stage}-consumers-group",
            group_name="consumers-group",
        )

        self.user_pool_client = self.user_pool.add_client(
            f"{config.name}-{config.stage}-user-pool-client",
            user_pool_client_name=f"{config.name}-{config.stage}-user-pool-client",
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    implicit_code_grant=True,
                    authorization_code_grant=True,
                ),
                scopes=[
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.PROFILE,
                ],
                callback_urls=[
                    config.web_domain,
                    "https://oauth.pstmn.io/v1/callback",
                ],
            ),
            prevent_user_existence_errors=True,
            access_token_validity=cdk.Duration.minutes(60),
            id_token_validity=cdk.Duration.minutes(60),
            refresh_token_validity=cdk.Duration.days(30),
        )

        self.user_pool_domain = self.user_pool.add_domain(
            f"{config.name}-{config.stage}-user-pool-domain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=f"{config.name}-{config.stage}",
            ),
        )
