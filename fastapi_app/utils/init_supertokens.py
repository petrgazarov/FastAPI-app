from typing import Union, Dict, Any
from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import thirdparty, session
from supertokens_python.recipe.thirdparty import Github
from supertokens_python.recipe.thirdparty.interfaces import (
    APIInterface,
    APIOptions,
    SignInUpPostOkResult,
    SignInUpPostNoEmailGivenByProviderResponse,
)
from supertokens_python.recipe.thirdparty.provider import Provider
from supertokens_python.recipe import dashboard
from supertokens_python.types import GeneralErrorResponse
import requests
from fastapi_app import database, services, models, config
from .logger import AppLogger


settings = config.get_settings()

logger = AppLogger().get_logger()


class GitHubApiError(Exception):
    pass


def get_github_user_info(access_token: str) -> Dict[str, str | None]:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        "https://api.github.com/user",
        headers=headers,
    )

    if response.status_code == 200:
        user_data = response.json()
        name = user_data["name"]
        return {
            "email": user_data["email"],
            "first_name": " ".join(name.split(" ")[:-1]) if name else None,
            "last_name": name.split(" ")[-1] if name else None,
            "image_url": user_data["avatar_url"],
        }
    else:
        raise GitHubApiError("Error: {response.status_code} - {response.text}")


def override_thirdparty_apis(original_implementation: APIInterface) -> APIInterface:
    original_sign_in_up_post = original_implementation.sign_in_up_post

    async def sign_in_up_post(
        provider: Provider,
        code: str,
        redirect_uri: str,
        client_id: Union[str, None],
        auth_code_response: Union[Dict[str, Any], None],
        api_options: APIOptions,
        user_context: Dict[str, Any],
    ) -> (
        SignInUpPostOkResult
        | SignInUpPostNoEmailGivenByProviderResponse
        | GeneralErrorResponse
    ):
        response = await original_sign_in_up_post(
            provider,
            code,
            redirect_uri,
            client_id,
            auth_code_response,
            api_options,
            user_context,
        )

        if isinstance(response, SignInUpPostOkResult):
            match provider.id:
                case "github":
                    user_info = get_github_user_info(
                        access_token=response.auth_code_response["access_token"],
                    )
                case _:
                    raise Exception("Unsupported provider")

            if response.created_new_user:
                db_gen = database.get_db()
                db = await anext(db_gen)
                await services.UsersService(db=db).create_user(
                    models.UserCreate(
                        email=str(user_info["email"]),
                        first_name=user_info["first_name"],
                        last_name=user_info["last_name"],
                        supertokens_id=response.user.user_id,
                        image_url=user_info["image_url"],
                    )
                )

        return response

    original_implementation.sign_in_up_post = sign_in_up_post
    return original_implementation


def init_supertokens() -> None:
    init(
        app_info=InputAppInfo(
            app_name="FastAPI App",
            api_domain="localhost:8000",
            website_domain=settings.app_url,
            api_base_path="/auth",
            website_base_path="/auth",
            api_gateway_path="/api",
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=settings.supertokens_connection_uri,
            api_key=settings.supertokens_api_key,
        ),
        framework="fastapi",
        recipe_list=[
            dashboard.init(),
            session.init(cookie_domain="localhost:8000"),
            thirdparty.init(
                override=thirdparty.InputOverrideConfig(apis=override_thirdparty_apis),
                sign_in_and_up_feature=thirdparty.SignInAndUpFeature(
                    providers=[
                        Github(
                            client_id=settings.github_client_id,
                            client_secret=settings.github_client_secret,
                        )
                    ]
                ),
            ),
        ],
        mode="asgi",
    )
