from dataclasses import dataclass
from typing import ClassVar, List


@dataclass
class DataChannel:
    SECURITY_STATUS = "F"
    MARKET_DATA = "X"
    FR_ROOM_DATA = "R"
    INDEX_DATA = "MI"
    BAR_DATA = "B"


@dataclass
class AllIndexes:
    """
    {'VN30', 'HNX30', 'VNALL', 'VNSML', 'VNIT', 'VNX50', 'VNXALL', 'VNCOND', 'HNXIndex', 'VNUTI', 'VNMID', 'VNHEAL', 'VNSI', 'VNFINSELECT', 'VNREAL', 'VNIND', 'VN100', 'HNXUpcomIndex', 'VNDIAMOND', 'VNCONS', 'VNFINLEAD', 'VNMAT', 'VNIndex', 'VNENE', 'VNFIN'}
    """
    VN30 = "VN30"
    HNX30 = "HNX30"
    VNALL = "VNALL"
    VNSML = "VNSML"
    VNIT = "VNIT"
    VNX50 = "VNX50"
    VNXALL = "VNXALL"
    VNCOND = "VNCOND"
    HNXIndex = "HNXIndex"
    VNUTI = "VNUTI"
    VNMID = "VNMID"
    VNHEAL = "VNHEAL"
    VNSI = "VNSI"
    VNFINSELECT = "VNFINSELECT"
    VNREAL = "VNREAL"
    VNIND = "VNIND"
    VN100 = "VN100"
    HNXUpcomIndex = "HNXUpcomIndex"
    VNDIAMOND = "VNDIAMOND"
    VNCONS = "VNCONS"
    VNFINLEAD = "VNFINLEAD"
    VNMAT = "VNMAT"
    VNIndex = "VNIndex"
    VNENE = "VNENE"
    VNFIN = "VNFIN"
    ALL_INDEXES = {
        VN30, HNX30, VNALL, VNSML, VNIT, VNX50, VNXALL, VNCOND, HNXIndex, VNUTI, VNMID, VNHEAL, VNSI, VNFINSELECT,
        VNREAL, VNIND, VN100, HNXUpcomIndex, VNDIAMOND, VNCONS, VNFINLEAD, VNMAT, VNIndex, VNENE, VNFIN
    }


@dataclass
class OrderType:
    LIMIT = "LO"
    MARKET = "MAK"
    ATO = "ATO"
    ATC = "ATC"


@dataclass
class OrderSide:
    BUY = "B"
    SELL = "S"


@dataclass
class SecurityMarket:
    HOSE = "HOSE"
    HNX = "HNX"
    UPCOM = "UPCOM"
    DER = "DER"
    ALL_MARKET = {HOSE, HNX, UPCOM, DER}
    DEFAULT = None


@dataclass
class TradingMarket:
    STOCK = "VN"
    FUTURE = "VNFE"


@dataclass
class StopOrderType:
    DOWN = "D"
    UP = "U"
    TRAILING_UP = "V"
    TRAILING_DOWN = "E"
    OCO = "O"
    BULL_BEAR = "B"
    DEFAULT = ""


@dataclass
class OrderStatus:
    """
        STATUS_DETAILS: ClassVar[Dict[str, str]] = {
        "WA": "Chờ duyệt",
        "RS": "Chờ gửi lên sàn",
        "SD": "Đang gửi lên sàn",
        "QU": "Chờ khớp tại sàn",
        "FF": "Khớp toàn phần",
        "PF": "Khớp một phần",
        "FFPC": "Khớp 1 phần hủy phần còn lại",
        "WM": "Chờ sửa",
        "WC": "Chờ hủy",
        "CL": "Đã hủy",
        "RJ": "Từ chối",
        "EX": "Hết hiệu lực",
        "SOR": "Chờ kích hoạt",
        "SOS": "Đã kích hoạt",
        "IAV": "Lệnh trước phiên",
        "SOI": "Lệnh ĐK trước phiên"
    }
    """
    _WAITING_APPROVAL: ClassVar[str] = "WA"
    _READY_TO_SEND_EXCH: ClassVar[str] = "RS"
    _SENT_TO_EXCH: ClassVar[str] = "SD"
    _QUEUE_IN_EXCH: ClassVar[str] = "QU"
    _FULLY_FILLED: ClassVar[str] = "FF"
    _PARTIALLY_FILLED: ClassVar[str] = "PF"
    _FULLY_FILLED_PARTIALLY_CANCELLED: ClassVar[str] = "FFPC"
    _WAITING_MODIFY: ClassVar[str] = "WM"
    _WAITING_CANCEL: ClassVar[str] = "WC"
    _CANCELLED: ClassVar[str] = "CL"
    _REJECTED: ClassVar[str] = "RJ"
    _EXPIRED: ClassVar[str] = "EX"
    _STOP_ORDER_READY: ClassVar[str] = "SOR"
    _STOP_ORDER_SENT: ClassVar[str] = "SOS"
    _PRE_SESSION_ORDER: ClassVar[str] = "IAV"
    _PRE_SESSION_STOP_ORDER: ClassVar[str] = "SOI"
    _PAS: ClassVar[str] = "PAS"  # Placeholder for PAS

    # work with groups
    FILLED_ORDERS: ClassVar[List[str]] = [_PARTIALLY_FILLED, _FULLY_FILLED, _FULLY_FILLED_PARTIALLY_CANCELLED]
    WORKING_ORDERS: ClassVar[List[str]] = [
        _WAITING_APPROVAL, _READY_TO_SEND_EXCH, _SENT_TO_EXCH, _QUEUE_IN_EXCH,
        _PARTIALLY_FILLED, _WAITING_MODIFY, _WAITING_CANCEL, _STOP_ORDER_READY,
        _STOP_ORDER_SENT, _PRE_SESSION_ORDER
    ]
    CANCELED_ORDERS: ClassVar[List[str]] = [_CANCELLED, _REJECTED, _EXPIRED]
    WAITING_ORDERS: ClassVar[List[str]] = [_PRE_SESSION_STOP_ORDER, _PAS]
    REJECT_ORDERS: ClassVar[List[str]] = [_REJECTED]
