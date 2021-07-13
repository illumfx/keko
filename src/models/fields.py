import json
from typing import Any, List, Optional, Type, Union

from tortoise.fields.base import Field
from tortoise.models import Model

# https://stackoverflow.com/questions/64161083/how-to-use-postgresql-array-field-in-tortoise-orm


class BigIntArrayField(Field, list):
    """
    Int Array field specifically for PostgreSQL.

    This field can store list of int values.
    """

    SQL_TYPE = "bigint[]"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(
        self, value: List[int], instance: "Union[Type[Model], Model]"
    ) -> Optional[List[int]]:
        return value

    def to_python_value(self, value: Any) -> Optional[List[int]]:
        if isinstance(value, str):
            array = json.loads(value.replace("'", '"'))
            return [int(x) for x in array]
        return value


class TextArrayField(Field, list):
    """
    Text field specifically for PostgreSQL.

    This field can store list of text values.
    """

    SQL_TYPE = "text[]"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(
        self, value: List[int], instance: "Union[Type[Model], Model]"
    ) -> Optional[List[int]]:
        return value

    def to_python_value(self, value: Any) -> Optional[List[int]]:
        if isinstance(value, str):
            array = json.loads(value.replace("'", '"'))
            return [int(x) for x in array]
        return value
