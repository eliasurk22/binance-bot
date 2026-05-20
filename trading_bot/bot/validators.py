from __future__ import annotations

from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


class ValidationError(ValueError):
    pass


def normalize_symbol(symbol: str) -> str:
    symbol = (symbol or "").strip().upper()
    if not symbol or not symbol.endswith("USDT"):
        raise ValidationError("symbol must be a non-empty USDT-M symbol like BTCUSDT")
    return symbol


def validate_side(side: str) -> str:
    side = (side or "").strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"side must be one of {sorted(VALID_SIDES)}")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = (order_type or "").strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"order_type must be one of {sorted(VALID_ORDER_TYPES)}")
    return order_type


def validate_positive_decimal(value: str | float, field_name: str) -> str:
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, TypeError):
        raise ValidationError(f"{field_name} must be a valid decimal number") from None
    if dec <= 0:
        raise ValidationError(f"{field_name} must be greater than 0")
    return format(dec.normalize(), "f")


def validate_price_for_type(order_type: str, price: str | float | None) -> str | None:
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("price is required when order_type is LIMIT")
        return validate_positive_decimal(price, "price")
    return None
