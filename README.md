# Binance Futures Testnet Order CLI

A small Python 3 application for placing **USDT-M Futures** orders on Binance Futures Testnet using direct REST calls.

## Features

- Place `MARKET` and `LIMIT` orders
- Supports `BUY` and `SELL`
- Validates CLI input before calling the API
- Clean structure with separate client, order, validation, and logging modules
- Logs API requests, responses, and errors to a file
- Handles validation, API, and network errors clearly

## Project Structure

```text
trading_bot/
  bot/
    __init__.py
    client.py
    orders.py
    validators.py
    logging_config.py
  cli.py
README.md
requirements.txt
logs/
```

## Setup

1. Register and activate a Binance Futures Testnet account.
2. Generate API credentials.
3. Clone or unzip this project.
4. Create and activate a virtual environment.
5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Export credentials (recommended):

```bash
export BINANCE_API_KEY="your_testnet_key"
export BINANCE_API_SECRET="your_testnet_secret"
```

## Run

Base URL used by default:

```text
https://testnet.binancefuture.com
```

### MARKET order example

```bash
python trading_bot/cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --order-type MARKET \
  --quantity 0.001
```

### LIMIT order example

```bash
python trading_bot/cli.py \
  --symbol BTCUSDT \
  --side SELL \
  --order-type LIMIT \
  --quantity 0.001 \
  --price 120000
```

## Output

The CLI prints:

- order request summary
- order response details: `orderId`, `status`, `executedQty`, `avgPrice` when available
- a success or failure message

## Assumptions

- The user already has a Binance Futures Testnet account with active API credentials.
- The symbol is a valid USDT-M contract such as `BTCUSDT`.
- Quantity and price precision depend on Binance symbol filters; invalid precision is surfaced as an API error.
- `newOrderRespType=RESULT` is used so the response is more informative.

## Logging

By default, logs are written to `logs/trading_bot.log`.

The repository also includes sample log files showing one market order and one limit order flow.

## Notes

- This app targets **testnet only**.
- No secrets are stored in the source code.
- A public GitHub repository is preferred for submission, but this package can also be submitted as a zip file.
