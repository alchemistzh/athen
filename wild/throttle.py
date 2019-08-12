#!/usr/bin/env python3
# coding: utf-8

import backoff
from ratelimit import limits, sleep_and_retry


# @backoff.on_exception(backoff.expo,
#                       requests.exceptions.RequestException,
#                       max_tries=5)
@sleep_and_retry
@limits(calls=1, period=1)
def call_api():
    """
    cause the current thread to sleep until the specified time period has ellapsed
    and then retry the function
    """
    print("call api")


while True:
    call_api()
