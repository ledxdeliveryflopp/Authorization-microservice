from dataclasses import dataclass
import hvac
from hvac.exceptions import InvalidPath, VaultDown
from src.settings.exceptions import VaultInvalidPath, VaultInvalidSealed
from src.settings.settings import settings


@dataclass
class VaultRepository:
    client = hvac.Client(
        url=settings.vault_settings.vault_url,
        token=settings.vault_settings.vault_token,
    )

    async def create_secret(self, email: str, password: str):
        """Сохранение секрета в vault"""
        try:
            new_secret = self.client.secrets.kv.v2.create_or_update_secret(
                mount_point=settings.vault_settings.vault_mount,
                path=f'{email}-secret-password',
                secret=dict(password=f"{password}"),
            )
            return new_secret
        except VaultDown:
            raise VaultInvalidSealed

    async def read_secret(self, email: str):
        """Чтение секрета из vault"""
        try:
            secret_by_vault = self.client.secrets.kv.read_secret_version(
                mount_point=settings.vault_settings.vault_mount, path=f'{email}-secret-password')
            secret = secret_by_vault["data"]["data"]["password"]
            return secret
        except InvalidPath:
            raise VaultInvalidPath
