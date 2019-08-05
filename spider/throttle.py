from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=1, period=1)
def call_api():
    print("call api")


while True:
    call_api()
