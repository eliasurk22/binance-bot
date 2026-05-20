from __future__ import annotations

import argparse
import os
import sys
from pprint import pformat

import requests

from bot.client import BinanceAPIError, BinanceFuturesTestnetClient
from bot.logging_config import setup_logging
from bot.orders import build_order_payload, extract_response_summary, format_order_summary
from bot.validators import ValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Binance Futures Testnet order placer")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--order-type", required=True, choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Limit price; required for LIMIT orders")
    parser.add_argument("--api-key", default=os.getenv("BINANCE_API_KEY"), help="Binance API key")
    parser.add_argument("--api-secret", default=os.getenv("BINANCE_API_SECRET"), help="Binance API secret")
    parser.add_argument("--base-url", default="https://testnet.binancefuture.com", help="Binance Futures Testnet base URL")
    parser.add_argument("--log-dir", default="logs", help="Directory for application logs")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    logger = setup_logging(args.log_dir)

    try:
        if not args.api_key or not args.api_secret:
            raise ValidationError("API credentials are required via --api-key/--api-secret or environment variables")

        payload = build_order_payload(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        print(format_order_summary(payload))

        client = BinanceFuturesTestnetClient(
            api_key=args.api_key,
            api_secret=args.api_secret,
            base_url=args.base_url,
            logger=logger,
        )
        response = client.place_order(**payload)
        summary = extract_response_summary(response)

        print("Response ->")
        print(pformat(summary, sort_dicts=False))
        print("Order placed successfully.")
        return 0

    except ValidationError as exc:
        logger.error("validation_error error=%s", exc)
        print(f"Validation error: {exc}", file=sys.stderr)
        return 2
    except BinanceAPIError as exc:
        logger.error("api_error status_code=%s payload=%s", exc.status_code, exc.payload)
        print(f"Binance API error: {exc}", file=sys.stderr)
        return 3
    except requests.RequestException as exc:
        logger.exception("request_exception error=%s", exc)
        print(f"Network error: {exc}", file=sys.stderr)
        return 4
    except Exception as exc:
        logger.exception("unexpected_error error=%s", exc)
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
