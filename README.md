# A Pythonic Way to Interact with SSI Trading API

### Document detail coming soon

This is a Pythonic way to interact with SSI Trading API.

## Overview
This library provides a convenient and Pythonic interface to interact with the SSI Trading API. It allows users to log in once for all market services, access various market APIs, trade futures and stocks, and obtain real-time market data. Additionally, it supports paper trading for both futures and stocks, enabling users to test trading strategies without risking real money.

## Installation

To install the package, run the following command:

```bash
pip install .
```

## Features
- [x] **Single Login:** Single login for all market services.
- [x] **Market APIs:** Access a variety of market data and services.
- [x] **Trading Futures:** Trade future derivatives.
- [ ] **Trading Fundamentals:** Trade stocks. (Coming soon)
- [x] **Paper Trading Futures:** Test future derivatives trading strategies without risking real money.
- [x] **Paper Trading Fundamentals:** Test stock trading strategies without risking real money.
- [x] **Real-time Data:** Get real-time data from the market.

## Usage

Here’s a basic example of how to use the library. For more detailed examples, see the examples in the [trading_paper.py](trading_paper.py) file.

```python
from ssi_trading.config import TradingServiceConfig, DataServiceConfig
from ssi_trading.server import SSIServices
from ssi_trading.services.client.data import MarketDataService
from ssi_trading.services.paper.futures import PaperFutureTradingService
from ssi_trading.services.stream.bar import BarDataStream
from ssi_trading.services.stream.index import IndexDataStream
from ssi_trading.services.stream.market import MarketDataStream

if __name__ == "__main__":
    ssis = SSIServices().add_trading_service(
        service=PaperFutureTradingService(<your config>)
    ).add_data_stream(
        stream=MarketDataStream(<your config>)
    ).add_data_stream(
        stream=IndexDataStream(<your config>)
    ).add_data_stream(
        stream=BarDataStream(<your config>)
    ).add_data_service(
        service=MarketDataService(<your config>)
    )

    ssis.start_data_stream()
    ssis.start_trading_stream()
    
    print(ssis.get_df_index_from_stream('VN30'))
```

For more examples and detailed usage, refer to the [trading_paper.py](trading_paper.py).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
Please contact the author for any questions or feedback.
