from ratelimit import limits, sleep_and_retry


# cause the current thread to sleep until the specified time period has ellapsed
# and then retry the function
@sleep_and_retry
@limits(calls=1, period=1)
def call_api():
    print("call api")


while True:
    call_api()
