from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, Date, DateTime, PrimaryKeyConstraint, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

import os
from dotenv import load_dotenv


class DatabaseManager:

    def __init__(self, db_name, echo=True):
        self.db_name = db_name
        self.echo = echo

    def create_engine(self):
        engine_string = f"postgresql://{os.getenv('postgres_user')}:{os.getenv('postgres_password')}@{os.getenv('postgres_host')}:{os.getenv('postgres_port')}/{self.db_name}"
        return create_engine(engine_string, echo=self.echo)

    def get_session(self):
        """Возвращает новую сессию для работы с БД."""
        return sessionmaker(bind=self.create_engine())


class Base(DeclarativeBase):
    pass

class BondTable(Base):
    __tablename__ = 'bond'
    __table_args__ = (PrimaryKeyConstraint('response_time', 'figi', name='pk_bond_response_time_figi'),
                      {'schema': 'raw'}
                      )

    response_time = Column(DateTime)
    figi = Column(String)
    ticker = Column(String)
    class_code = Column(String)
    isin = Column(String)
    lot = Column(Integer)
    currency = Column(String)
    klong = Column(Float)
    kshort = Column(Float)
    dlong = Column(Float)
    dshort = Column(Float)
    dlong_min = Column(Float)
    dshort_min = Column(Float)
    short_enabled_flag = Column(Boolean)
    name = Column(String)
    exchange = Column(String)
    coupon_quantity_per_year = Column(Integer)
    maturity_date = Column(Date)
    nominal_value = Column(Float)
    nominal_currency = Column(String)
    initial_nominal_currency = Column(String)
    initial_nominal_value = Column(Float)
    state_reg_date = Column(Date)
    placement_date = Column(Date)
    placement_price_currency = Column(String)
    placement_price_value = Column(Float)
    aci_value_currency = Column(String)
    aci_value_value = Column(Float)
    country_of_risk = Column(String)
    country_of_risk_name = Column(String)
    sector = Column(String)
    issue_kind = Column(String)
    issue_size = Column(Float)
    issue_size_plan = Column(Float)
    trading_status = Column(String)
    otc_flag = Column(Boolean)
    buy_available_flag = Column(Boolean)
    sell_available_flag = Column(Boolean)
    floating_coupon_flag = Column(Boolean)
    perpetual_flag = Column(Boolean)
    amortization_flag = Column(Boolean)
    min_price_increment = Column(Float)
    api_trade_available_flag = Column(Boolean)
    uid = Column(UUID(as_uuid=True))
    real_exchange = Column(String)
    position_uid = Column(UUID(as_uuid=True))
    asset_uid = Column(UUID(as_uuid=True))
    for_iis_flag = Column(Boolean)
    for_qual_investor_flag = Column(Boolean)
    weekend_flag = Column(Boolean)
    blocked_tca_flag = Column(Boolean)
    subordinated_flag = Column(Boolean)
    liquidity_flag = Column(Boolean)
    first_1min_candle_date = Column(DateTime)
    first_1day_candle_date = Column(DateTime)
    risk_level = Column(String)
    brand = Column(String)
    bond_type = Column(String)
    call_date = Column(Date)
    dlong_client = Column(Float)
    dshort_client = Column(Float)

class HistoricCandleTable(Base):
    __tablename__ = 'historic_candle'
    __table_args__ = (PrimaryKeyConstraint('figi', 'interval', 'time', name='pk_historic_candle_figi_interval_time'),
                      {'schema': 'raw'}
                      )
    figi = Column(String)
    interval = Column(String)
    time = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    is_complete = Column(Boolean)
    candle_source_type = Column(String)


class ShareTable(Base):
    __tablename__ = 'share'
    __table_args__ = (
        PrimaryKeyConstraint('response_time', 'figi', name='pk_share_response_time_figi'),
        {'schema': 'raw'}
    )

    # Основные идентификаторы
    response_time = Column(DateTime)
    figi = Column(String)
    ticker = Column(String)
    class_code = Column(String)
    isin = Column(String)

    # Параметры торговли
    lot = Column(Integer)
    currency = Column(String)
    klong = Column(Float)  # Конвертируется из Quotation
    kshort = Column(Float)  # Конвертируется из Quotation
    dlong = Column(Float)  # Конвертируется из Quotation
    dshort = Column(Float)  # Конвертируется из Quotation
    dlong_min = Column(Float)  # Конвертируется из Quotation
    dshort_min = Column(Float)  # Конвертируется из Quotation
    short_enabled_flag = Column(Boolean)

    # Описательные атрибуты
    name = Column(String)
    exchange = Column(String)
    ipo_date = Column(Date)
    issue_size = Column(BigInteger)

    # Страновые риски
    country_of_risk = Column(String)
    country_of_risk_name = Column(String)
    sector = Column(String)

    # Параметры эмиссии
    issue_size_plan = Column(BigInteger)
    nominal_value = Column(Float)  # Конвертируется из MoneyValue
    nominal_currency = Column(String)

    # Статус торговли
    trading_status = Column(String)
    otc_flag = Column(Boolean)
    buy_available_flag = Column(Boolean)
    sell_available_flag = Column(Boolean)
    div_yield_flag = Column(Boolean)

    # Тип акции
    share_type = Column(String)

    # Ценовые параметры
    min_price_increment = Column(Float)  # Конвертируется из Quotation

    # Флаги доступности
    api_trade_available_flag = Column(Boolean)
    liquidity_flag = Column(Boolean)

    # Идентификаторы
    uid = Column(String)
    real_exchange = Column(String)
    position_uid = Column(String)
    asset_uid = Column(String)
    instrument_exchange = Column(String)

    # Флаги особенностей
    for_iis_flag = Column(Boolean)
    for_qual_investor_flag = Column(Boolean)
    weekend_flag = Column(Boolean)
    blocked_tca_flag = Column(Boolean)

    # Даты первой свечи
    first_1min_candle_date = Column(DateTime)
    first_1day_candle_date = Column(DateTime)

    # Бренд
    brand = Column(String)

    # Клиентские параметры
    dlong_client = Column(Float)  # Конвертируется из Quotation
    dshort_client = Column(Float)  # Конвертируется из Quotation


class EtfTable(Base):
    __tablename__ = 'etf'
    __table_args__ = (
        PrimaryKeyConstraint('response_time', 'figi', name='pk_etf_response_time_figi'),
        {'schema': 'raw'}
    )

    # Основные идентификаторы
    response_time = Column(DateTime)
    figi = Column(String)
    ticker = Column(String)
    class_code = Column(String)
    isin = Column(String)

    # Параметры торговли
    lot = Column(Integer)
    currency = Column(String)
    klong = Column(Float)  # Конвертируется из Quotation
    kshort = Column(Float)  # Конвертируется из Quotation
    dlong = Column(Float)  # Конвертируется из Quotation
    dshort = Column(Float)  # Конвертируется из Quotation
    dlong_min = Column(Float)  # Конвертируется из Quotation
    dshort_min = Column(Float)  # Конвертируется из Quotation
    short_enabled_flag = Column(Boolean)

    # Описательные атрибуты
    name = Column(String)
    exchange = Column(String)
    fixed_commission = Column(Float)  # Конвертируется из Quotation
    focus_type = Column(String)

    # Даты и параметры выпуска
    released_date = Column(Date)
    num_shares = Column(Float)  # Конвертируется из Quotation

    # Страновые риски
    country_of_risk = Column(String)
    country_of_risk_name = Column(String)
    sector = Column(String)

    # Параметры ребалансировки
    rebalancing_freq = Column(String)

    # Статус торговли
    trading_status = Column(String)
    otc_flag = Column(Boolean)
    buy_available_flag = Column(Boolean)
    sell_available_flag = Column(Boolean)

    # Ценовые параметры
    min_price_increment = Column(Float)  # Конвертируется из Quotation

    # Флаги доступности
    api_trade_available_flag = Column(Boolean)
    liquidity_flag = Column(Boolean)

    # Идентификаторы
    uid = Column(String)
    real_exchange = Column(String)
    position_uid = Column(String)
    asset_uid = Column(String)
    instrument_exchange = Column(String)

    # Флаги особенностей
    for_iis_flag = Column(Boolean)
    for_qual_investor_flag = Column(Boolean)
    weekend_flag = Column(Boolean)
    blocked_tca_flag = Column(Boolean)

    # Даты первой свечи
    first_1min_candle_date = Column(DateTime)
    first_1day_candle_date = Column(DateTime)

    # Бренд
    brand = Column(String)

    # Клиентские параметры
    dlong_client = Column(Float)  # Конвертируется из Quotation
    dshort_client = Column(Float)  # Конвертируется из Quotation

class CurrencyTable(Base):
    __tablename__ = 'currency'
    __table_args__ = (
        PrimaryKeyConstraint('response_time', 'figi', name='pk_currency_response_time_figi'),
        {'schema': 'raw'}
    )

    # Основные идентификаторы
    response_time = Column(DateTime)
    figi = Column(String)
    ticker = Column(String)
    class_code = Column(String)
    isin = Column(String)

    # Параметры торговли
    lot = Column(Integer)
    currency = Column(String)
    klong = Column(Float)  # Конвертируется из Quotation
    kshort = Column(Float)  # Конвертируется из Quotation
    dlong = Column(Float)  # Конвертируется из Quotation
    dshort = Column(Float)  # Конвертируется из Quotation
    dlong_min = Column(Float)  # Конвертируется из Quotation
    dshort_min = Column(Float)  # Конвертируется из Quotation
    short_enabled_flag = Column(Boolean)

    # Описательные атрибуты
    name = Column(String)
    exchange = Column(String)
    nominal_value = Column(Float)  # Конвертируется из MoneyValue
    nominal_currency = Column(String)  # Часть MoneyValue

    # Страновые риски
    country_of_risk = Column(String)
    country_of_risk_name = Column(String)

    # Статус торговли
    trading_status = Column(String)
    otc_flag = Column(Boolean)
    buy_available_flag = Column(Boolean)
    sell_available_flag = Column(Boolean)

    # Специфичные для валюты поля
    iso_currency_name = Column(String)
    min_price_increment = Column(Float)  # Конвертируется из Quotation

    # Флаги доступности
    api_trade_available_flag = Column(Boolean)

    # Идентификаторы
    uid = Column(String)
    real_exchange = Column(String)
    position_uid = Column(String)

    # Флаги особенностей
    for_iis_flag = Column(Boolean)
    for_qual_investor_flag = Column(Boolean)
    weekend_flag = Column(Boolean)
    blocked_tca_flag = Column(Boolean)

    # Даты первой свечи
    first_1min_candle_date = Column(DateTime)
    first_1day_candle_date = Column(DateTime)

    # Бренд
    brand = Column(String)

    # Клиентские параметры
    dlong_client = Column(Float)  # Конвертируется из Quotation
    dshort_client = Column(Float)  # Конвертируется из Quotation


class FutureTable(Base):
    __tablename__ = 'future'
    __table_args__ = (
        PrimaryKeyConstraint('response_time', 'figi', name='pk_future_response_time_figi'),
        {'schema': 'raw'}
    )

    # Основные идентификаторы
    response_time = Column(DateTime)
    figi = Column(String)
    ticker = Column(String)
    class_code = Column(String)

    # Параметры торговли
    lot = Column(Integer)
    currency = Column(String)
    klong = Column(Float)  # Конвертируется из Quotation
    kshort = Column(Float)  # Конвертируется из Quotation
    dlong = Column(Float)  # Конвертируется из Quotation
    dshort = Column(Float)  # Конвертируется из Quotation
    dlong_min = Column(Float)  # Конвертируется из Quotation
    dshort_min = Column(Float)  # Конвертируется из Quotation
    short_enabled_flag = Column(Boolean)

    # Описательные атрибуты
    name = Column(String)
    exchange = Column(String)

    # Даты торгов
    first_trade_date = Column(DateTime)
    last_trade_date = Column(DateTime)

    # Специфичные для фьючерсов поля
    futures_type = Column(String)
    asset_type = Column(String)
    basic_asset = Column(String)
    basic_asset_size = Column(Float)  # Конвертируется из Quotation

    # Страновые риски
    country_of_risk = Column(String)
    country_of_risk_name = Column(String)
    sector = Column(String)

    # Дата экспирации
    expiration_date = Column(DateTime)

    # Статус торговли
    trading_status = Column(String)
    otc_flag = Column(Boolean)
    buy_available_flag = Column(Boolean)
    sell_available_flag = Column(Boolean)

    # Ценовые параметры
    min_price_increment = Column(Float)  # Конвертируется из Quotation
    min_price_increment_amount = Column(Float)  # Конвертируется из Quotation

    # Флаги доступности
    api_trade_available_flag = Column(Boolean)

    # Идентификаторы
    uid = Column(String)
    real_exchange = Column(String)
    position_uid = Column(String)
    basic_asset_position_uid = Column(String)

    # Флаги особенностей
    for_iis_flag = Column(Boolean)
    for_qual_investor_flag = Column(Boolean)
    weekend_flag = Column(Boolean)
    blocked_tca_flag = Column(Boolean)

    # Даты первой свечи
    first_1min_candle_date = Column(DateTime)
    first_1day_candle_date = Column(DateTime)

    # Маржинальные требования
    initial_margin_on_buy_value = Column(Float)  # Конвертируется из MoneyValue
    initial_margin_on_buy_currency = Column(String)
    initial_margin_on_sell_value = Column(Float)  # Конвертируется из MoneyValue
    initial_margin_on_sell_currency = Column(String)

    # Бренд
    brand = Column(String)

    # Клиентские параметры
    dlong_client = Column(Float)  # Конвертируется из Quotation
    dshort_client = Column(Float)  # Конвертируется из Quotation

tinkoffdb_manager = DatabaseManager('tinkoff_db')


def create_all_tables():
    """Создает все таблицы в базе данных через метаданные"""
    engine = tinkoffdb_manager.create_engine()

    # Создаем схему raw если она не существует
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
        conn.commit()

    # Создаем все таблицы
    Base.metadata.create_all(engine)
    print("Все таблицы успешно созданы")

if __name__ == '__main__':
    load_dotenv()
    create_all_tables()