# Description: Futures trading client implementation.
#
import datetime
from typing import Union, List, Dict

from ssi_trading.config import TradingServiceConfig
from ssi_trading.models.trading import CreatedOrder, MaxBuySellQty, StockPosition, AccountBalance
from ssi_fctrading.models import fcmodel_requests
import logging
from ssi_trading.services.client import BaseTradingService
from ssi_trading.utils import generate_request_id


class FutureTradingService(BaseTradingService):

    def account_balance(self) -> Union[AccountBalance, None]:
        """
        {
            "message": "Success",
            "status": 200,
            "data": {
                "account": "0901358",
                "accountBalance": 11166309263,
                "fee": 0,
                "commission": 0,
                "interest": 1514965,
                "loan": 0,
                "deliveryAmount": 0,
                "floatingPL": 0,
                "totalPL": 0,
                "marginable": 0,
                "depositable": 1148597520,
                "rcCall": 0,
                "withdrawable": 10912447363,
                "nonCashDrawableRCCall": 0,
                "internalAssets": {
                    "cash": 1165730020,
                    "validNonCash": 0,
                    "totalValue": 11166309263,
                    "maxValidNonCash": 0,
                    "cashWithdrawable": 1148597520,
                    "ee": 8197059272
                },
                "exchangeAssets": {
                    "cash": 10000579243,
                    "validNonCash": 0,
                    "totalValue": 10000579243,
                    "maxValidNonCash": 0,
                    "cashWithdrawable": 9763849843,
                    "ee": 7322887382
                },
                "internalMargin": {
                    "initialMargin": 172660800,
                    "deliveryMargin": 0,
                    "marginReq": 172660800,
                    "accountRatio": 1.5462656096416592,
                    "usedLimitWarningLevel1": 75,
                    "usedLimitWarningLevel2": 85,
                    "usedLimitWarningLevel3": 90,
                    "marginCall": 0
                },
                "exchangeMargin": {
                    "marginReq": 172660800,
                    "accountRatio": 1.7265079932330476,
                    "usedLimitWarningLevel1": 75,
                    "usedLimitWarningLevel2": 85,
                    "usedLimitWarningLevel3": 90,
                    "marginCall": 0
                }
            }
        }

        :return:
        """
        try:
            fc_rq = fcmodel_requests.StockAccountBalance(self._account_id)
            res = self._client.get_stock_account_balance(fc_rq)
            data = res['data']
            if res['message'].lower() == 'success':
                return AccountBalance(
                    account_id=self._account_id,
                    market_id=self._market_id,
                    balance=data['accountBalance'],
                    trading_pl=data['totalPL'] - data['floatingPL'],
                    floating_pl=data['floatingPL'],
                    total_pl=data['totalPL'],
                    ee=data['exchangeAssets']['ee'],
                    nav=data['exchangeAssets']['totalValue'] - data['internalAssets']['totalValue'],
                    withdrawable=data['withdrawable'],
                    fee=data['fee'],
                    interest=data['interest'],
                    commission=data['commission']
                )

        except Exception as ex:
            logging.error(f"Error while getting account balance: {ex}")
            return None

    def order_history(self, order_status=None, start_date=None, end_date=None, page=1, page_size=50) -> Union[List[CreatedOrder], None]:
        """
            message: "Success",
            status: 200,
            data: {
            orderHistories: [
                {
                    uniqueID: null,
                    orderID: "12626539",
                    buySell: "B",
                    price: 800.0,
                    quantity: 10,
                    filledQty: 0,
                    orderStatus: "RJ",
                    marketID: "VNFE",
                    inputTime: "1603157594668",
                    modifiedTime: "1603157594668",
                    instrumentID: "VN30F2012",
                    orderType: "LO",
                    cancelQty: 0,
                    avgPrice: 0.0,
                    isForcesell: null,
                    isShortsell: null
                }
            ],
            account: "0901358"
            }
        """
        if start_date is None:
            start_date = datetime.datetime.now().strftime("%d/%m/%Y")
            end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")

        try:
            fc_rq = fcmodel_requests.OrderHistory(self._account_id, start_date, end_date)
            res = self._client.get_order_history(fc_rq)
            if res['message'].lower() == 'success':
                return [
                    CreatedOrder(
                        symbol=order['instrumentID'],
                        market_id=self._market_id,
                        account_id=self._account_id,
                        order_side=order['buySell'],
                        order_type=order['orderType'],
                        order_price=order['price'],
                        order_qty=order['quantity'],
                        order_id=order['orderID'],
                        order_status=order['orderStatus'],
                        avg_price=order['avgPrice'],
                        os_qty=order['quantity'] - order['filledQty'],
                        filled_qty=order['filledQty']
                    ) for order in res.get('orderHistories', [])
                ]
        except Exception as ex:
            logging.error(f"Error while getting order history: {ex}")
            return None

    def current_positions(self) -> Union[Dict[str, StockPosition], None]:
        """
        message: "Success",
        status: 200,
        data: {
        account: "0901358",
        openPosition: [
            {
                marketID: "VNFE",
                instrumentID: "VN30F2106",
                longQty: 8,
                shortQty: 0,
                net: 8,
                bidAvgPrice: 0,
                askAvgPrice: 0,
                tradePrice: 1452.7,
                marketPrice: 1452.7,
                floatingPL: 0,
                tradingPL: 0
            }
        ],
        closePosition: [ ]
        """
        fc_rq = fcmodel_requests.DerivativePosition(self._account_id, True)
        try:
            res = self._client.get_derivative_position(fc_rq)
            if res['message'].lower() == 'success':
                return {position['instrumentID']:  StockPosition(
                    market_id=self._market_id,
                    account_id=self._account_id,
                    symbol=position['instrumentID'],
                    position=position['longQty'] - position['shortQty'],
                    trading_pl=position['tradingPL'],
                    floating_pl=position['floatingPL'],
                    market_price=position['marketPrice'],
                    avg_price=position['tradePrice']
                ) for position in res.get('openPosition', [])}
        except Exception as ex:
            logging.error(f"Error while getting closed positions: {ex}")
            return None

    def closed_positions(self) -> Union[Dict[str, StockPosition], None]:
        """
        message: "Success",
        status: 200,
        data: {
        account: "0901358",
        openPosition: [
            {
                marketID: "VNFE",
                instrumentID: "VN30F2106",
                longQty: 8,
                shortQty: 0,
                net: 8,
                bidAvgPrice: 0,
                askAvgPrice: 0,
                tradePrice: 1452.7,
                marketPrice: 1452.7,
                floatingPL: 0,
                tradingPL: 0
            }
        ],
        closePosition: [ ]
        """
        fc_rq = fcmodel_requests.DerivativePosition(self._account_id, True)
        try:
            res = self._client.get_derivative_position(fc_rq)
            if res['message'].lower() == 'success':
                return {position['instrumentID']: StockPosition(
                    market_id=self._market_id, account_id=self._account_id,
                    symbol=position['instrumentID'],
                    position=position['longQty'] - position['shortQty'],
                    trading_pl=position['tradingPL'],
                    floating_pl=position['floatingPL'],
                    market_price=position['marketPrice'],
                    avg_price=position['tradePrice']
                ) for position in res.get('closePosition', [])}
        except Exception as ex:
            logging.error(f"Error while getting closed positions: {ex}")
            return None

    def max_buy_sell_qty(self, symbol, price, order_side) -> Union[MaxBuySellQty, None]:
        """
        message: "Success",
        status: 200,
        data: {
            account: "0041691",
            maxBuyQty: 8241440,
            marginRatio: "50%",
            purchasingPower: 99292902171
        }
        :param symbol:
        :param price:
        :param order_side:
        :return:
        """
        fc_rq = fcmodel_requests.MaxBuyQty(self._account_id, symbol, price)
        try:
            res = self._client.get_max_buy_qty(fc_rq)
            if res['message'].lower() == 'success':
                data = res['data']
                return MaxBuySellQty(
                    symbol=symbol,
                    max_qty=data.get('maxBuyQty') or data.get('maxSellQty'),
                    power=data.get('purchasingPower'),
                    market_id=self._market_id, account_id=self._account_id
                )
        except Exception as ex:
            logging.error(f"Error while getting max buy qty: {ex}")
            return None

    def __init__(self, config: TradingServiceConfig):
        super().__init__(config)

    def create_order(self, order: CreatedOrder) -> Union[CreatedOrder, None]:
        """
        {
            message: "Success",
            status: 200,
            data: {
                requestID: "1678195",
                requestData:
                {
                    instrumentID: "SSI",
                    market: "VN",
                    buySell: "B",
                    orderType: "LO",
                    channelID: "IW",
                    price: 21000,
                    quantity: 300,
                    account: "0901351",
                    stopOrder: false,
                    stopPrice: 0,
                    stopType: "string",
                    stopStep: 0,
                    lossStep: 0,
                    profitStep: 0
                }
            }
        }
        :param order:
        :return:
        """
        order.market_id = self._market_id
        order.account_id = self._account_id
        try:
            fc_req = fcmodel_requests.NewOrder(
                account=order.account_id,
                requestID=generate_request_id(),
                instrumentID=order.symbol,
                market=order.market_id,
                buySell=order.order_side,
                orderType=order.order_type,
                price=order.order_price,
                quantity=order.order_qty,
                deviceId=self._device_id,
                userAgent=self._user_agent,
                stopOrder=order.stop_order,
                stopPrice=order.stop_price,
                stopType=order.stop_type,
                stopStep=order.stop_step,
                lossStep=order.loss_step,
                profitStep=order.profit_step
            )
            res = self._client.der_new_order(fc_req)
            return order if res['message'].lower() == "success" else None
        except Exception as ex:
            logging.error(f"Error while creating order: {ex}")
            return None

    def cancel_order(self, order) -> Union[CreatedOrder, None]:
        """
        {
            message: "Success",
            status: 200,
            data: {
                requestID: "52513603",
                requestData: {
                    orderID: "12658867",
                    account: "0901358",
                    marketID: "VNFE",
                    instrumentID: "VN30F2106",
                    buySell: "B",
                    requestID: "52513603"
                }
            }
        }
        :param order:
        :return:
        """
        order.market_id = self._market_id
        order.account_id = self._account_id

        fc_rq = fcmodel_requests.CancelOrder(
            account=order.account_id,
            requestID=generate_request_id(),
            orderID=order.order_id,
            marketID=order.market_id,
            instrumentID=order.symbol,
            buySell=order.order_side,
            deviceId=self._device_id,
            userAgent=self._user_agent
        )

        try:
            res = self._client.der_cancle_order(fc_rq)
            return order if res['message'].lower() == "success" else None
        except Exception as ex:
            logging.error(f"Error while cancelling order: {ex}")
            return None

    def modify_order(self, order: CreatedOrder, new_qty: int = 0, new_price: float = 0) -> Union[CreatedOrder, None]:
        """
        {
            message: "Success",
            status: 200,
            data: {
                requestID: "93235974",
                requestData: {
                    orderID: "12658867",
                    price: 1410,
                    quantity: 2,
                    account: "0901358",
                    instrumentID: "VN30F2106",
                    marketID: "VNFE",
                    buySell: "B",
                    orderType: "LO"
                }
            }
        }
        :param order:
        :param new_qty:
        :param new_price:
        :return:
        """
        order.order_price = order.order_price or new_price
        order.order_qty = order.order_qty or new_qty
        order.market_id = self._market_id
        order.account_id = self._account_id

        fc_rq = fcmodel_requests.ModifyOrder(
            account=order.account_id,
            requestID=generate_request_id(),
            orderID=order.order_id,
            marketID=order.market_id,
            instrumentID=order.symbol,
            price=order.order_price,
            quantity=order.order_qty,
            buySell=order.order_side,
            orderType=order.order_type,
            deviceId=self._device_id,
            userAgent=self._user_agent
        )
        try:
            res = self._client.der_modify_order(fc_rq)
            return order if res['message'].lower() == "success" else None
        except Exception as ex:
            logging.error(f"Error while modifying order: {ex}")
            return None
