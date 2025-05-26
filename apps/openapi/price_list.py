
TOKENS_COUNT = 1000000

PRICE_LIST = {
    "gpt-4o": {
        "prompt": 2.50 / TOKENS_COUNT,
        "completion": 10.00 / TOKENS_COUNT,
        "cached": 1.25 / TOKENS_COUNT
    },
    "gpt-4.1": {
        "prompt": 2.00 / TOKENS_COUNT,
        "completion": 8.00 / TOKENS_COUNT,
        "cached": 0.50 / TOKENS_COUNT
    }
}