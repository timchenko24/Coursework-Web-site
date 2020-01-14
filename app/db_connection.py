import pyodbc
import pandas as pd


def connect_to_db(db_name, query):
    connection_string = 'DRIVER={0}; SERVER=DESKTOP-8J2BR8L; DATABASE={1}; ' \
                        'Trusted_Connection=yes'.format('ODBC Driver 11 for SQL Server', db_name)
    sql_conn = pyodbc.connect(connection_string)
    df = pd.read_sql(query, sql_conn)
    last_id = list(df['id'])[-1]
    return sql_conn, sql_conn.cursor(), last_id
