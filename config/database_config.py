import os

import psycopg
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

DB_CONNECTION_PARAMS = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "row_factory": dict_row,
}


class DatabaseConfig:
    def __init__(self, db_connection_params):
        self._pool = PooledDB(
            creator=psycopg,
            mincached=2,
            maxcached=2,
            maxconnections=5,
            blocking=True,
            **db_connection_params,
        )

    def _get_connection(self):
        return self._pool.connection()

    def fetch_all(self, sql, params=()):
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def fetch_one(self, sql, params=()):
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        finally:
            conn.close()

    def execute(self, sql, params=()):
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                row = cursor.fetchone() if cursor.description else None
                rowcount = cursor.rowcount
            conn.commit()
            return row, rowcount
        except Exception as e:
            print(f"Error in SQL execution: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
