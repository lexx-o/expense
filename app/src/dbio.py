import pandas as pd
from config import config

from driveio import File
from sqlalchemy import Engine


def write_table_update_log(*, partition: str, file: File, engine) -> None:
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
    log.to_sql(name='update_log', con=engine, schema=config.schema, if_exists='append', index=False)


def read_table_update_log(engine: Engine) -> pd.DataFrame:
    """
    Reads table of expense partition table update log.
    Args:
        engine: SQLAlchemy engine
    Returns:
        DataFrame of update_log table
    """
    return pd.read_sql(sql=f"SELECT * FROM {config.schema}.update_log", con=engine)
