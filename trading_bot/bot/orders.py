from __future__ import annotations

from typing import Dict, Any

from .validators import (
    normalize_symbol,
    validate_order_type,
    validate_price_for_type,
    validate_positive_decimal,
    validate_side,
)


def build_order_payload(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str | float,
    price: str | float | None = None,
    time_in_force: str = "GTC",
) -> Dict[str, Any]:
    symbol = normalize_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_positive_decimal(quantity, "quantity")
    price = validate_price_for_type(order_type, price)

    payload: Dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "newOrderRespType": "RESULT",
    }

    if order_type == "LIMIT":
        payload["price"] = price
        payload["timeInForce"] = time_in_force

    return payload


def format_order_summary(payload: Dict[str, Any]) -> str:
    return (
        f"Request -> symbol={payload['symbol']} side={payload['side']} "
        f"type={payload['type']} quantity={payload['quantity']} "
        f"price={payload.get('price', 'N/A')}"
    )


def extract_response_summary(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty"),
        "avgPrice": response.get("avgPrice") or response.get("price") or "N/A",
        "symbol": response.get("symbol"),
        "side": response.get("side"),
        "type": response.get("type"),
    }
