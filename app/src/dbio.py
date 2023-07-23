from dataclasses import dataclass

import pandas as pd
from sqlalchemy import Engine, text

from config import config
from config.variables import Columns
from driveio import File
from db.connector import pg_engine


@dataclass(frozen=True)
class Table:
    """A representation of PostgresDB tables"""
    name: str
    schema: str

    def __str__(self):
        return f"{self.schema}.{self.name}"

    def write(self, df: pd.DataFrame, engine: Engine = pg_engine):
        df.to_sql(name=self.name,
                  con=engine,
                  schema=self.schema,
                  index=False,
                  if_exists='replace')

    def read(self, engine: Engine = pg_engine, columns: list[str] = None):
        if columns:
            cols = ','.join(['"' + colname + '"' for colname in columns])
        else:
            cols = '*'
        return pd.read_sql(sql=f"SELECT {cols} FROM {self}", con=engine)


def write_table_update_log(*, partition: str, file: File, engine: Engine = pg_engine) -> None:
    """
    Writes to table of expense partition table update log.
    Args:
        partition: expense data partition
        file: Google Drive file
        engine: SQLAlchemy engine
    """
    log = pd.DataFrame.from_dict({'dttm': [pd.Timestamp.now()],
                                  'modified': [file.modified],
                                  'partition': [partition],
                                  'name': [file.name]
                                  })
    log.to_sql(name='update_log', con=engine, schema=config.db.schema, if_exists='append', index=False)


def read_table_update_log(engine: Engine = pg_engine) -> pd.DataFrame:
    """
    Reads table of expense partition table update log.
    Args:
        engine: SQLAlchemy engine
    Returns:
        DataFrame of update_log table
    """
    return pd.read_sql(sql=f"SELECT * FROM {config.db.schema}.update_log", con=engine)


def get_latest_log(log: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(index=config.partitions.keys())
    latest = log.sort_values(by=['dttm'], ascending=False).groupby(by=['partition']).last()
    modified_times = df.join(latest)
    modified_times['modified'] = pd.to_datetime(modified_times['modified'])
    return modified_times


def update_account_data_in_table(data: pd.DataFrame, table: Table, engine: Engine = pg_engine):
    """
    Updates table from a dataframe.
    Entries that have accounts found in the dataframe are cleared and then appended to the source table.
    """
    target = Table(name='_temp_target', schema=config.db.schema)
    target.write(data, engine=engine)

    query = f"""
        begin;
    
        create table {config.db.schema}._temp_result as
        select * 
        from {table} as source
        where source.\"{Columns.ACC}\" NOT IN
            (
            select distinct \"{Columns.ACC}\"
            from {target}
            )
        union all
        select *
        from {config.db.schema}._temp_target;
        
        alter table {table} rename to {table.name}_old;
        alter table {config.db.schema}._temp_result rename to {table.name};
        
        drop table {table}_old;
        drop table {config.db.schema}._temp_target;
        
        commit;
    """

    with engine.connect() as con:
        con.execute(text(query))
