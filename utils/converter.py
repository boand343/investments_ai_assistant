from tinkoff.invest.schemas import Bond, Quotation, MoneyValue, HistoricCandle
from tinkoff.invest.schemas import _grpc_helpers
from sqlalchemy.orm import DeclarativeBase
from plum import dispatch
from typing import Type, Any, Union
from tinkoff.invest.utils import quotation_to_decimal, money_to_decimal


class SimpleTypeMapper:

    @classmethod
    @dispatch
    def to_simple_type(cls, attr_name: str, attr_value: MoneyValue) -> dict[Any, Any]:
        return {attr_name + '_value': money_to_decimal(attr_value),
                attr_name + '_currency': attr_value.currency
                }

    @classmethod
    @dispatch
    def to_simple_type(cls, attr_name: str, attr_value: Quotation) -> dict[Any, Any]:
        return {attr_name: quotation_to_decimal(attr_value)}

    @classmethod
    @dispatch
    def to_simple_type(cls, attr_name: str, attr_value: str | bool) -> dict[Any, Any]:
        return {attr_name: attr_value}

    @classmethod
    @dispatch
    def to_simple_type(cls, attr_name: str, attr_value) -> dict[Any, Any]:
        return {attr_name: str(attr_value)}

    @classmethod
    @dispatch
    def convert(cls, from_obj: _grpc_helpers.Message, to_type: Type[DeclarativeBase]) -> DeclarativeBase:
        attributes = {}
        for attr, value in vars(from_obj).items():
            simple_type_attr_dict = cls.to_simple_type(attr, value)
            cls._add_dicts(attributes, simple_type_attr_dict)
        return to_type(**attributes)

    @classmethod
    def _add_dicts(cls, dict1, dict2):
        common_keys = set(dict1.keys()) & set(dict2.keys())
        if common_keys:
            raise KeyError(f"Ключи {common_keys} уже существуют в первом словаре.")
        dict1.update(dict2)