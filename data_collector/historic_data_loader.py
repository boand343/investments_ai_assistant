from datetime import datetime, UTC
import os

from tinkoff.invest import Client, CandleInterval
from typing import Optional, List, Dict, Union
from utils.converter import SimpleTypeMapper
from databases.models.tinkoff_db import DatabaseManager, tinkoffdb_manager, Base, HistoricCandleTable, BondTable, ShareTable, EtfTable, \
                                        CurrencyTable, FutureTable
from dotenv import load_dotenv
import logging


logger = logging.getLogger(__name__)

class TinkoffDataLoader:
    db_manager: DatabaseManager = tinkoffdb_manager
    table: Base

    @classmethod
    def _save(
            cls,
            data_iter,
            additional_fields: Optional[Dict] = None
    ) -> int:
        """
        Сохранение свечей в БД

        :param data_iter: Итератор от Tinkoff API
        :param additional_fields: Дополнительные поля
        :return: Количество сохранённых свечей
        """
        Session = cls.db_manager.get_session()
        session = Session()
        count = 0

        try:
            for data in data_iter:
                historic_candle_table = SimpleTypeMapper.convert(data, cls.table)

                if additional_fields:
                    for field, value in additional_fields.items():
                        setattr(historic_candle_table, field, value)

                session.add(historic_candle_table)
                count += 1

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        return count

    @staticmethod
    def _getClient():
        if not os.getenv('TOKEN'):
            raise ValueError("Tinkoff API token not found in environment variables")
        return Client(os.getenv('TOKEN'))

class HistoricCandleLoader(TinkoffDataLoader):
    db_manager = tinkoffdb_manager
    table = HistoricCandleTable

    @classmethod
    def load(
            cls,
            figi: Union[str, List[str]],
            interval: Union[str, List[str]],
            from_date: datetime,
            to_date: datetime
    ) -> int:
        """
        Загрузка свечей в БД

        :param figi: FIGI инструмента
        :param interval: Интервал свечей (строка или CandleInterval)
        :param from_date: Начальная дата
        :param to_date: Конечная дата
        :return: Количество загруженных свечей
        """

        if not os.getenv('TOKEN'):
            raise ValueError("Tinkoff API token not found in environment variables")

        # Преобразуем в списки если переданы одиночные значения
        figi_list = [figi] if isinstance(figi, str) else figi
        interval_list = [interval] if isinstance(interval, str) else interval

        total_candles = 0
        try:
            with cls._getClient() as client:
                for current_figi in figi_list:
                    for current_interval in interval_list:
                        logger.info(
                            f"Loading candles for FIGI {current_figi}, "
                            f"interval {current_interval}"
                        )

                        candles = client.get_all_candles(
                            instrument_id=current_figi,
                            from_=from_date,
                            to=to_date,
                            interval=CandleInterval[current_interval]  # Конвертируем строку в CandleInterval
                        )

                        count = cls._save(
                            candles,
                            additional_fields={
                                'figi': current_figi,
                                'interval': current_interval
                            }
                        )
                        total_candles += count
                        logger.info(f"Saved {count} candles for FIGI {current_figi}")

        except KeyError as e:
            logger.error(f"Invalid CandleInterval value: {str(e)}")
            raise ValueError(f"Invalid interval value. Details: {str(e)}")
        except Exception as e:
            logger.error(f"Error loading candles: {str(e)}")
            raise

        logger.info(f"Total candles loaded: {total_candles}")
        return total_candles


# Добавим в historic_data_loader.py

class InstrumentLoader(TinkoffDataLoader):
    """Базовый класс для загрузки инструментов"""

    @classmethod
    def load_instrument(cls, instrument_type: str) -> int:
        """
        Загрузка инструментов в БД

        :param instrument_type: Тип инструмента (bonds, shares, etfs, currencies, futures)
        :return: Количество загруженных инструментов
        """

        try:
            with cls._getClient() as client:
                instruments_service = client.instruments

                # Выбираем нужный метод в зависимости от типа инструмента
                if instrument_type == 'bonds':
                    instruments = instruments_service.bonds()
                elif instrument_type == 'shares':
                    instruments = instruments_service.shares()
                elif instrument_type == 'etfs':
                    instruments = instruments_service.etfs()
                elif instrument_type == 'currencies':
                    instruments = instruments_service.currencies()
                elif instrument_type == 'futures':
                    instruments = instruments_service.futures()
                else:
                    raise ValueError(f"Unknown instrument type: {instrument_type}")

                response_time = datetime.now(UTC)
                # Конвертируем и сохраняем инструменты
                count = cls._save(instruments.instruments, additional_fields={'response_time': response_time})
                logger.info(f"Saved {count} {instrument_type}")
                return count

        except Exception as e:
            logger.error(f"Error loading {instrument_type}: {str(e)}")
            raise


class BondLoader(InstrumentLoader):
    db_manager = tinkoffdb_manager
    table = BondTable

    @classmethod
    def load(cls) -> int:
        """Загрузка облигаций"""
        return cls.load_instrument('bonds')


class ShareLoader(InstrumentLoader):
    db_manager = tinkoffdb_manager
    table = ShareTable  # Нужно добавить ShareTable в tinkoff_db.py

    @classmethod
    def load(cls) -> int:
        """Загрузка акций"""
        return cls.load_instrument('shares')


class EtfLoader(InstrumentLoader):
    db_manager = tinkoffdb_manager
    table = EtfTable  # Нужно добавить EtfTable в tinkoff_db.py

    @classmethod
    def load(cls) -> int:
        """Загрузка ETF"""
        return cls.load_instrument('etfs')


class CurrencyLoader(InstrumentLoader):
    db_manager = tinkoffdb_manager
    table = CurrencyTable  # Нужно добавить CurrencyTable в tinkoff_db.py

    @classmethod
    def load(cls) -> int:
        """Загрузка валют"""
        return cls.load_instrument('currencies')


class FutureLoader(InstrumentLoader):
    db_manager = tinkoffdb_manager
    table = FutureTable  # Нужно добавить FutureTable в tinkoff_db.py

    @classmethod
    def load(cls) -> int:
        """Загрузка фьючерсов"""
        return cls.load_instrument('futures')

def __reload_historic_candle(from_date: datetime, to_date: datetime, figi: str, interval: str):
    Session = HistoricCandleLoader.db_manager.get_session()
    with Session() as session:
        filter_obj = session.query(HistoricCandleTable).filter(
            HistoricCandleTable.time >= from_date,
            HistoricCandleTable.time <= to_date,
            HistoricCandleTable.figi == figi,
            HistoricCandleTable.interval == interval
        )
        filter_obj.delete()
        session.commit()
    HistoricCandleLoader.load(figi, interval, from_date, to_date)

def __test_load():
    load_dotenv()
    from_ = datetime.strptime('2023/01/07', '%Y/%m/%d')
    to = datetime.strptime('2023/01/08', '%Y/%m/%d')
    figi = "BBG004730N88"
    interval = 'CANDLE_INTERVAL_HOUR'
    __reload_historic_candle(from_, to, figi, interval)
    BondLoader.load()
    ShareLoader.load()
    EtfLoader.load()
    CurrencyLoader.load()
    FutureLoader.load()

if __name__ == '__main__':
    __test_load()
