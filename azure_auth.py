
from azure.identity import ClientSecretCredential
from azure.core.credentials import AccessToken
from datetime import datetime, timedelta
from typing import Dict


def get_credential(cfg: Dict) -> ClientSecretCredential:
    return ClientSecretCredential(
        tenant_id=cfg["tenant_id"],
        client_id=cfg["client_id"],
        client_secret=cfg["client_secret"],
    )


def get_management_token(credential: ClientSecretCredential) -> str:
    scope = "https://management.azure.com/.default"
    token: AccessToken = credential.get_token(scope)
    return token.token
