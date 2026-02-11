class InvoiceService:
    def __init__(self) -> None:
        self._coupon_rate: Dict[str, float] = {
            "WELCOME10": 0.10,
            "VIP20": 0.20,
            "STUDENT5": 0.05
        }

        self._shipping_rules = {
            "TH": self._ship_th,
            "JP": self._ship_jp,
            "US": self._ship_us
        }

        self._tax_rate = {
            "TH": 0.07,
            "JP": 0.10,
            "US": 0.08
        }

    def _ship_th(self, subtotal: float) -> float:
        return 60 if subtotal < 500 else 0

    def _ship_jp(self, subtotal: float) -> float:
        return 600 if subtotal < 4000 else 0

    def _ship_us(self, subtotal: float) -> float:
        if subtotal < 100:
            return 15
        if subtotal < 300:
            return 8
        return 0
