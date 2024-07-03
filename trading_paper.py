import logging
import time

from dotenv import load_dotenv

from ssi_trading.config import TradingServiceConfig, DataServiceConfig
from ssi_trading.server import SSIServices
from ssi_trading.services.client.data import MarketDataService
from ssi_trading.services.paper.futures import PaperFutureTradingService
from ssi_trading.services.stream.bar import BarDataStream
from ssi_trading.services.stream.index import IndexDataStream
from ssi_trading.services.stream.market import MarketDataStream
import os


load_dotenv()


if __name__ == "__main__":
    list_symbols = ["VN30F2407", "VN30F2108"]
    list_indexes = ["VN30"]

    data_config = DataServiceConfig(
        consumer_id=os.environ['DATA_CONSUMER_ID'],
        consumer_secret=os.environ['DATA_CONSUMER_SECRET'],
        symbols=None
    )

    market_config = DataServiceConfig(
        consumer_id=os.environ['DATA_CONSUMER_ID'],
        consumer_secret=os.environ['DATA_CONSUMER_SECRET'],
        symbols=list_symbols
    )

    index_config = DataServiceConfig(
        consumer_id=os.environ['DATA_CONSUMER_ID'],
        consumer_secret=os.environ['DATA_CONSUMER_SECRET'],
        symbols=list_indexes
    )

    bar_config = DataServiceConfig(
        consumer_id=os.environ['DATA_CONSUMER_ID'],
        consumer_secret=os.environ['DATA_CONSUMER_SECRET'],
        symbols=list_symbols
    )

    fr_config = DataServiceConfig(
        consumer_id=os.environ['DATA_CONSUMER_ID'],
        consumer_secret=os.environ['DATA_CONSUMER_SECRET'],
        symbols=list_symbols
    )

    trading_config = TradingServiceConfig(
        consumer_id=os.environ['TRADING_CONSUMER_ID'],
        consumer_secret=os.environ['TRADING_CONSUMER_SECRET'],
        account_id=os.environ['ACCOUNT_ID'],
        paper_trading=True,
        account_type="future"
    )

    ssis = SSIServices().add_trading_service(
        service=PaperFutureTradingService(trading_config)
    ).add_data_stream(
        stream=MarketDataStream(market_config)
    ).add_data_stream(
        stream=IndexDataStream(index_config)
    ).add_data_stream(
        stream=BarDataStream(fr_config)
    ).add_data_service(
        service=MarketDataService(data_config)
    )

    ssis.start_data_stream()
    ssis.start_trading_stream()

    while True:
        time.sleep(60)
        logging.info("=================================")
        logging.info(f"Tick data : {ssis.get_df_index_from_stream('VN30')}")
        # logging.info(f"All pending orders : {ssis.pending_orders()}")
        # logging.info(f"All positions : {ssis.current_positions()}")
        # logging.info(f"Account balance : {ssis.account_balance()}")
        # logging.info(f"Portfolio : {ssis.view_portfolio()}")
        # logging.info(f"Current market ({list_symbols[0]}) : {ssis.get_current_market_from_stream(list_symbols[0])}")
        # logging.info(f"Current index ({list_indexes[0]}) : {ssis.get_current_index_from_stream(list_indexes[0])}")
