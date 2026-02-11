class InvoiceService:
    def __init__(self) -> None:
        self._coupon_rate: Dict[str, float] = {
            "WELCOME10": 0.10,
            "VIP20": 0.20,
            "STUDENT5": 0.05
        }

        self._shipping_rules = {
            "TH": lambda s: 60 if s < 500 else 0,
            "JP": lambda s: 600 if s < 4000 else 0,
            "US": lambda s: 15 if s < 100 else 8 if s < 300 else 0
        }

        self._tax_rate = {
            "TH": 0.07,
            "JP": 0.10,
            "US": 0.08
        }

    def _compute_shipping(self, country: str, subtotal: float) -> float:
        if country in self._shipping_rules:
            return self._shipping_rules[country](subtotal)
        return 25 if subtotal < 200 else 0

    def _compute_tax(self, country: str, subtotal: float, discount: float) -> float:
        rate = self._tax_rate.get(country, 0.05)
        return (subtotal - discount) * rate

    def _compute_discount(self, inv: Invoice, subtotal: float, warnings: List[str]) -> float:
        discount = 0.0
        if inv.membership == "gold":
            discount += subtotal * 0.03
        elif inv.membership == "platinum":
            discount += subtotal * 0.05
        elif subtotal > 3000:
            discount += 20

        if inv.coupon:
            code = inv.coupon.strip()
            if code in self._coupon_rate:
                discount += subtotal * self._coupon_rate[code]
            else:
                warnings.append("Unknown coupon")
        return discount

    def compute_total(self, inv: Invoice) -> Tuple[float, List[str]]:
        warnings: List[str] = []
        problems = self._validate(inv)
        if problems:
            raise ValueError("; ".join(problems))

        subtotal = sum(it.unit_price * it.qty for it in inv.items)
        fragile_fee = sum(5.0 * it.qty for it in inv.items if it.fragile)

        shipping = self._compute_shipping(inv.country, subtotal)
        discount = self._compute_discount(inv, subtotal, warnings)
        tax = self._compute_tax(inv.country, subtotal, discount)

        total = subtotal + shipping + fragile_fee + tax - discount
        total = max(total, 0)

        if subtotal > 10000 and inv.membership not in ("gold", "platinum"):
            warnings.append("Consider membership upgrade")

        return total, warnings
