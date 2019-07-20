# coding: utf-8

from sqlalchemy import BigInteger, Column, DateTime, String

from . import Base


class StockProfile(Base):
    """ StockProfile is a data structure for simple and basic stock infomation.

    Required attributes:
        id: Unique id of a stock. Ex: 600100.
        name: Short name of the stock.

    Optional attributes:
        market: Exchange market corporation of the stock. Ex: SSE.
        pinyin: Pinyin acronym of the name. Ex: zhgf.
        value: Total market value.
        float_value: Free-float market value.
        shares: Total outstanding shares.
        float_shares: Free-float shares.
        update_time: Lastest update time.
    """

    __tablename__ = "stock_profile"

    id = Column(String(16), primary_key=True)
    name = Column(String(16), nullable=False)
    market = Column(String(16))
    pinyin = Column(String(16))

    value = Column(BigInteger)
    float_value = Column(BigInteger)
    shares = Column(BigInteger)
    float_shares = Column(BigInteger)

    pe = Column(Numeric(precision=8, scale=2))
    pe_ttm = Column(Numeric(precision=8, scale=2))
    pb = Column(Numeric(precision=8, scale=2))
    roe = Column(Numeric(precision=8, scale=2))
    eps = Column(Numeric(precision=8, scale=3))

    update_time = Column(DateTime)
