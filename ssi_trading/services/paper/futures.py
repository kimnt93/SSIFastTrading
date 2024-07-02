# Description: Futures paper trading client implementation.
# You can visit https://papertrading.ssi.com.vn/
import datetime
import logging
from typing import Union, Dict, List

from langchain_community.chains.llm_requests import DEFAULT_HEADERS

from ssi_trading.config import TradingServiceConfig, PAPER_BASE_URL
from ssi_trading.models.trading import (
    CreatedOrder, MaxBuySellQty, StockPosition,
    AccountBalance,
)
from ssi_trading.services.client import BaseTradingService


class PaperFutureTradingService(BaseTradingService):
    def __init__(self, config: TradingServiceConfig):
        # Do not call supper method
        super().__init__(config)
        # setup paper api
        self._base_url = PAPER_BASE_URL
        self._request_headers = DEFAULT_HEADERS
        self._request_headers["Authorization"] = f"Bearer {self._account_token}"

        # create static url
        self.create_order_url = f"{PAPER_BASE_URL}/demo-trading/order"
        self.modify_order_url = f"{PAPER_BASE_URL}/demo-trading/order/modify"
        self.cancel_order_url = f"{PAPER_BASE_URL}/demo-trading/order/cancel"
        self.account_balance_url = f"{PAPER_BASE_URL}/demo-trading/der-account-balance"
        self.order_history_url = f"{PAPER_BASE_URL}/demo-trading/order"
        self.position_url = f"{PAPER_BASE_URL}/demo-trading/stock-derivative"
        self.max_buy_sell_url = f"{PAPER_BASE_URL}/demo-trading/max-buy-sell"

    def create_order(self, order: CreatedOrder) -> Union[CreatedOrder, None]:
        order.market_id = self._market_id
        order.account_id = self.account_id
        params = {
            "instrumentID": order.symbol,
            "account": order.account_id,
            "buySell": order.order_side,
            "channelID": "IW",
            "marketID": order.market_id,
            "orderType": order.order_type,
            "price": order.order_price,
            "quantity": order.order_qty,
            "stopOrder": order.stop_order,
            "stopPrice": order.stop_price,
            "lossStep": order.loss_step,
            "profitStep": order.profit_step,
            "isAutoPrice": False
        }
        response = self._client.post(self.create_order_url, json=params, headers=self._request_headers)
        response.raise_for_status()

        # create default response
        try:
            data = response.json()
            order.order_status = data['data'][0]['orderStatus']
            order.order_id = data['data'][0]['orderID']
            return order if data['code'].lower() == "success" else None
        except Exception as ex:
            logging.exception(ex)
            return None

    def cancel_order(self, order) -> Union[CreatedOrder, None]:
        order.market_id = self._market_id
        order.account_id = self.account_id

        payload = {
            "orderID": order.order_id,
            "marketID": order.market_id,
            "instrumentID": order.symbol,
            "buySell": order.order_side,
            "account": order.account_id,
        }
        response = self._client.post(self.cancel_order_url, json=payload, headers=self._request_headers)
        response.raise_for_status()
        try:
            data = response.json()
            return order if data['code'].lower() == "success" else None
        except Exception as ex:
            logging.exception(ex)
            return None

    def modify_order(self, order: CreatedOrder, new_qty: int = 0, new_price: float = 0) -> Union[CreatedOrder, None]:
        order.order_price = order.order_price or new_price
        order.order_qty = order.order_qty or new_qty
        order.market_id = self._market_id
        order.account_id = self.account_id

        payload = {
            "orderID": order.order_id,
            "account": order.account_id,
            "price": order.order_price,
            "quantity": order.order_qty,
            "marketID": order.market_id,
            "instrumentID": order.symbol,
            "buySell": order.order_side,
            "orderType": order.order_type
        }
        response = self._client.post(self.modify_order_url, json=payload, headers=self._request_headers)
        response.raise_for_status()
        try:
            data = response.json()
            order.success = True if data['code'] == "SUCCESS" else False
            order.order_status = data['data'][0]['orderStatus']
            return order if data['code'].lower() == "success" else None
        except Exception as ex:
            logging.exception(f"Error while modifying order: {ex}")
            return None

    def account_balance(self) -> Union[AccountBalance, None]:
        params = {"account": self.account_id}
        response = self._client.get(self.account_balance_url, headers=self._request_headers, params=params)
        response.raise_for_status()
        try:
            data = response.json()['data']
            return AccountBalance(
                account_id=self.account_id,
                market_id=self._market_id,
                balance=data['accountBalance'],
                trading_pl=data['totalPL'] - data['floatingPL'],
                floating_pl=data['floatingPL'],
                total_pl=data['totalPL'],
                ee=data['ee'],
                nav=data['nav'],
                withdrawable=data['withdrawable'],
                fee=data['fee'],
                interest=data['extInterest']
            ) if data['code'].lower() == "success" else None
        except Exception as ex:
            logging.exception(ex)
            return None

    def current_positions(self) -> Union[Dict[str, StockPosition], None]:
        response = self._client.get(self.position_url, headers=self._request_headers, params={"account": self.account_id})
        response.raise_for_status()
        try:
            data = response.json()
            return {
                row['instrumentID']: StockPosition(
                    account_id=self.account_id,
                    market_id=self._market_id,
                    symbol=row['instrumentID'],
                    position=row['longQty'] - row['shortQty'],
                    trading_pl=row['tradingPL'],
                    floating_pl=row['floatingPL'],
                    avg_price=row['tradePrice'],
                    market_price=row['marketPrice'],
                ) for row in data['data']['openPositions']
            } if data['code'].lower() == "success" else None
        except Exception as ex:
            logging.exception(f"Error while getting current positions: {ex}")
            return None

    def closed_positions(self) -> Union[Dict[str, StockPosition], None]:
        response = self._client.get(self.position_url, headers=self._request_headers, params={"account": self.account_id})
        response.raise_for_status()
        try:
            data = response.json()
            return {
                row['instrumentID']: StockPosition(
                    account_id=self.account_id,
                    market_id=self._market_id,
                    symbol=row['instrumentID'],
                    position=row['longQty'] - row['shortQty'],
                    trading_pl=row['tradingPL'],
                    floating_pl=row['floatingPL'],
                    avg_price=row['tradePrice'],
                    market_price=row['marketPrice'],
                ) for row in data['data']['closePositions']
            } if data['code'].lower() == "success" else None

        except Exception as ex:
            logging.exception(f"Error while getting closed positions: {ex}")
            return None

    def max_buy_sell_qty(self, symbol, price, order_side) -> Union[MaxBuySellQty, None]:
        params = {
            "stockSymbol": symbol,
            "account": self.account_id,
            "price": price,
            "type": order_side
        }
        response = self._client.get(self.max_buy_sell_url, headers=self._request_headers, params=params)
        response.raise_for_status()
        try:
            data = response.json()
            return MaxBuySellQty(
                account_id=self.account_id,
                market_id=self._market_id,
                symbol=symbol,
                max_qty=data['data'].get('maxBuyQty') or data['data'].get('maxSellQty') or 0,
                power=data['data']['purchasingPower']
            ) if data['code'].lower() == "success" else None
        except Exception as ex:
            logging.exception(f"Error while getting max buy sell qty: {ex}")
            return None

    def order_history(self, order_status=None, start_date=None, end_date=None, page=1, page_size=20) -> Union[List[CreatedOrder], None]:
        if start_date is None:
            start_date = datetime.datetime.now().strftime("%d/%m/%Y")
            end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
        params = {
            "account": self.account_id,
            "page": page,
            "pageSize": page_size,
            "orderStatus": order_status,
            "startDate": start_date,
            "endDate": end_date
        }
        response = self._client.get(self.order_history_url, headers=self._request_headers, params=params)
        response.raise_for_status()
        # init default with account, market id, false success
        try:
            data = response.json()
            return [
                CreatedOrder(
                    account_id=self.account_id,
                    market_id=row['marketID'],
                    symbol=row['instrumentID'],
                    order_side=row['buySell'],
                    order_type=row['orderType'],
                    order_price=row['price'],
                    avg_price=row['avgPrice'],
                    order_qty=row['quantity'],
                    os_qty=row['osQty'],
                    filled_qty=row['filledQty'],
                    order_status=row['currentOrderStatus'],
                    order_id=row['orderID'],
                ) for row in data['data'].get('orderHistories', [])
            ] if data['code'].lower() == "success" else None
        except Exception as ex:
            logging.exception(f"Error while getting order history: {ex}")
            return None
