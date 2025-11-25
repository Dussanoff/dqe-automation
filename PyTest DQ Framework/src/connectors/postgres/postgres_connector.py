import typing
import pandas as pd
import psycopg2

class PostgresConnectorContextManager:
    def __init__(self, host: str, port: int, database: str, user: str, password: str, autocommit: bool = False):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.autocommit = autocommit
        self.connection: typing.Optional[psycopg2.extensions.connection] = None

    def __enter__(self):
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.connection.autocommit = self.autocommit
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.connection:
            self.connection.close()

    def get_data_sql(self, sql):
        try:
            data_df = pd.read_sql(sql, self.connection)
            return data_df
        except Exception as e:
            print(f'Failed to receive data from DB\nError: {e}\n')
            raise

