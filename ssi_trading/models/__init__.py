from dataclasses import dataclass
from typing import Optional


@dataclass
class _SSIBaseRequest:
    success: Optional[bool] = False
    market_id: Optional[str] = None
    account_id: Optional[str] = None
