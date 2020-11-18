from dataclasses import dataclass
from datetime import timedelta

from common.enums.app_user_role import AppUserRole


@dataclass(frozen=True)
class DecodedBearerToken:
    user_id: int
    role: AppUserRole


@dataclass(frozen=True)
class BearerTokenRequest(DecodedBearerToken):
    expiration: timedelta
