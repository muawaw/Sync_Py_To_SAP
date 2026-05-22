import pandas as pd
from sqlalchemy import create_engine, text
import os
import logging 

logger = logging.getLogger(__name__)

class FetchData:
    def __init__(self, engine, db_name="Database"):
        self.db_name = db_name
        try:
            logger.info(f"Initializing connection to {self.db_name}...")
            
            if engine is None:
                raise ValueError("Engine object is None. Check your initialization() logic.")
            
            self.engine = engine 
            
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(f"Connection to {self.db_name} successful.")
            
        except Exception as e:
            logger.error(f"Failed to connect to {self.db_name}: {e}")
            raise

    def _read_sql_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"SQL file not found at: {file_path}")
        with open(file_path, 'r') as file:
            return file.read()

    def fetch_from_file(self, sql_file_name, params=None):
        logger.info(f"Preparing to run query from file: {sql_file_name}")
        try:
            raw_sql = self._read_sql_file(sql_file_name)
<<<<<<< HEAD

            breakpoint()
=======
>>>>>>> 9177ddb734d7ad0cd3a6731e46c01a98ae87e4cd
            
            logger.info(f"Executing query on {self.db_name}...")
            with self.engine.connect() as connection:
                result_df = pd.read_sql(text(raw_sql), connection, params=params)
                
<<<<<<< HEAD
            if result_df.empty:
                emp_id = params.get('pernr') if isinstance(params, dict) else None
                if emp_id:
                    msg = f"[{sql_file_name}] No Active PYMT for NIK: {emp_id}."
                else:
                    msg = f"[{sql_file_name}] Query returned an empty dataset from {self.db_name}."
                
                print(msg)
                logger.warning(msg)
            else:
                print(f"[{sql_file_name}] Successfully fetched {len(result_df)} rows.")
                logger.info(f"SUCCESS: Fetched {len(result_df)} rows from {self.db_name}.")
=======
            print(f"[{sql_file_name}] Successfully fetched {len(result_df)} rows.")
            logger.info(f"SUCCESS: Fetched {len(result_df)} rows from {self.db_name}.")
>>>>>>> 9177ddb734d7ad0cd3a6731e46c01a98ae87e4cd
            return result_df
            
        except FileNotFoundError:
            logger.error(f"FAILED: SQL file '{sql_file_name}' not found.")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"FAILED: Error during {self.db_name} fetch: {e}")
            return pd.DataFrame()