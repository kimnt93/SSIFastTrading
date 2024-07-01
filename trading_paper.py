import logging
import time

from dotenv import load_dotenv

from ssi_trading.config import TradingServiceConfig, DataServiceConfig
from ssi_trading.server import SSIServices
from ssi_trading.services.paper.futures import PaperFutureTradingService
from ssi_trading.services.stream.index import IndexDataStream
from ssi_trading.services.stream.market import MarketDataStream
import os

load_dotenv()


if __name__ == "__main__":
    list_symbols = ["VN30F2407", "VN30F2108"]
    list_indexes = ["VN30"]

    data_config = DataServiceConfig(
        consumer_id=os.environ['CONSUMER_ID'],
        consumer_secret=os.environ['CONSUMER_SECRET'],
    )

    trading_config = TradingServiceConfig(
        consumer_id="",
        consumer_secret="",
        account_id=os.environ['ACCOUNT_ID'],
        paper_trading=True,
    )

    ssis = SSIServices().add_trading_service(
        service=PaperFutureTradingService(trading_config)
    ).add_data_stream(
        stream=MarketDataStream(data_config, list_symbols=list_symbols)
    ).add_data_stream(
        stream=IndexDataStream(data_config, list_indexes=list_indexes)
    )

    ssis.start_stream()

    while True:
        time.sleep(60)
        logging.info("=================================")
        logging.info(f"All pending orders : {ssis.pending_orders()}")
        logging.info(f"All positions : {ssis.current_positions()}")
        logging.info(f"Account balance : {ssis.account_balance()}")
        logging.info(f"Portfolio : {ssis.view_portfolio()}")
        logging.info(f"Current market ({list_symbols[0]}) : {ssis.get_current_market_from_stream(list_symbols[0])}")
        logging.info(f"Current index ({list_indexes[0]}) : {ssis.get_current_index_from_stream(list_indexes[0])}")