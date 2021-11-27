import sentry_sdk

sentry_sdk.init(
    "https://1bf8d88f425048b4a29d7adaedd1f01e@o1079278.ingest.sentry.io/6083951",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

try:
    division_by_zero = 1 / 0
except Exception as e:
    sentry_sdk.capture_exception(error=e)
