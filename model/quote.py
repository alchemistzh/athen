#!/usr/bin/env python3
# coding: utf-8

from sqlalchemy import Column, String, Date, Numeric, BigInteger

from . import Base


class Quote(Base):
    """ Quote defines data structure for a quote of stock trading in in period of time.

    Required attributes:
        id: Unique id of a stock. Ex: 600100.
        span: Time span of the quote: day, week, Month, etc...
        date: The date of the quote. TODO: Determine start or end date to use.
        open: Opening price.
        high: Highest price.
        low: Lowest price.
        close: Closing price.
        volume: Volume of shares traded.
        amount: Amount of money traded.

    Optional attributes:
        change: Changed of amount.
        percent: Change in percent.
        turnover: Turnover rate in percentage.
    """

    __tablename__ = "quote"

    id = Column(String(16), primary_key=True)
    span = Column(String(16), primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Numeric(precision=10, scale=3), nullable=False)
    high = Column(Numeric(precision=10, scale=3), nullable=False)
    low = Column(Numeric(precision=10, scale=3), nullable=False)
    close = Column(Numeric(precision=10, scale=3), nullable=False)
    volume = Column(BigInteger, nullable=False)
    amount = Column(BigInteger, nullable=False)

    change = Column(Numeric(precision=10, scale=3))
    percent = Column(Numeric(precision=8, scale=3))
    turnover = Column(Numeric(precision=8, scale=2))
