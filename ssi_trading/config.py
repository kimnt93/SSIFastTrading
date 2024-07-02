
# paper trading
PAPER_BASE_URL = "https://iboard-tapi.ssi.com.vn"
PAPER_REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "vi",
    "Sec-Ch-Ua": """Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120""",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Dest": "empty",
    "Origin": "https://papertrading.ssi.com.vn",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


class DataServiceConfig:
    def __init__(self, consumer_id: str, consumer_secret: str, symbols):
        self.consumerID = consumer_id
        self.consumerSecret = consumer_secret
        self.auth_type = 'Bearer'
        self.url = 'https://fc-data.ssi.com.vn/'
        self.stream_url = 'https://fc-datahub.ssi.com.vn/'
        self.symbols = symbols

    def __str__(self):
        return (f"DataServiceConfig(consumer_id={self.consumerID[:4]}..., "
                f"consumer_secret={self.consumerSecret[:4]}..., symbols={self.symbols})")


class TradingServiceConfig:
    def __init__(
            self,
            consumer_id: str,
            consumer_secret: str,
            account_id: str,
            account_type: str,  # fundamental or future
            auth_token: str = '',
            private_key: str = '',
            paper_trading: bool = False,
            two_fa_type: int = 0,  # 0-PIN, 1-OTP
            notify_id: int = -1,
    ):
        self.auth_token = auth_token
        self.paper_trading = paper_trading
        self.ConsumerID = consumer_id
        self.ConsumerSecret = consumer_secret
        self.account_type = account_type
        self.PrivateKey = private_key
        self.Url = 'https://fc-tradeapi.ssi.com.vn/'
        self.StreamURL = 'https://fc-tradehub.ssi.com.vn/'
        self.TwoFAType = two_fa_type
        self.NotifyId = notify_id
        self.account_id = account_id

    def __str__(self):
        return (f"TradingServiceConfig(consumer_id={self.ConsumerID[:4]}..., "
                f"consumer_secret={self.ConsumerSecret[:4]}..., "
                f"account_id={self.account_id}, account_type={self.account_type}, "
                f"paper_trading={self.paper_trading}, auth_token={self.auth_token[:4]}...)")
