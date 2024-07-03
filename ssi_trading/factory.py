import logging
from functools import lru_cache

from ssi_fc_data.fc_md_client import MarketDataClient

from ssi_trading.config import DataServiceConfig


@lru_cache(maxsize=1024)
def create_market_data_client(cfg: DataServiceConfig) -> MarketDataClient:
    logging.info(f"Creating market data client: {cfg}")
    return MarketDataClient(cfg)
