def _get_key_name(prefix: str, table_name: str, column_name: str) -> str:
    return f"{prefix}_{table_name}__{column_name}"


def get_foreign_key_name(table_name: str, column_name: str) -> str:
    return _get_key_name("fk", table_name, column_name)


def get_unique_key_name(table_name: str, column_name: str) -> str:
    return _get_key_name("uk", table_name, column_name)


def get_primary_key_name(table_name: str, column_name: str = "id") -> str:
    return _get_key_name("pk", table_name, column_name)


def get_index_name(table_name: str, column_name: str = "id") -> str:
    return _get_key_name("ix", table_name, column_name)
