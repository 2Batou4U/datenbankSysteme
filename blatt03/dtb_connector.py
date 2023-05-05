import sys

import mariadb


def alter_column(table_name: str, column_name: str, column_type: str) -> str:
    cursor = get_connection()
    check_table_query = f"""SHOW COLUMNS FROM `{table_name}` LIKE '{column_name}';"""
    cursor.execute(statement=check_table_query)

    if len(cursor.fetchall()) > 0:
        alter_table_query = f"""ALTER TABLE {table_name} DROP COLUMN {column_name};"""
    else:
        alter_table_query = f"""ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} NULL;"""

    cursor.execute(statement=alter_table_query)

    return alter_table_query


def add_row(table_name: str, row_tuple: tuple) -> str:
    cursor = get_connection()

    rows_to_be_inserted = ""
    for idx, row in enumerate(row_tuple):
        rows_to_be_inserted += f"""{row}{',' if idx + 1 != len(row_tuple) else ''}"""

    add_row_query = f"""INSERT INTO {table_name} VALUES {rows_to_be_inserted};"""
    try:
        cursor.execute(add_row_query)
    except mariadb.IntegrityError as ierr:
        print(ierr)

    return add_row_query


def delete_row(table_name: str, rows_dict: dict) -> str:

    pass


# alter_column(table_name='Assistant', column_name='ABCDEFG', column_type='int')
row_tuple = (('3008', 'Adrian', 'Schlafen', '2127'),
             ('3009', 'Lena', 'Unity', '2127'),
             ('3010', 'Anna', 'Beschweren', '2127'))

add_row(table_name='Assistant', row_tuple=row_tuple)
