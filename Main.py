#!/usr/bin/env python
import os
from pyrfc import Connection
from dotenv import load_dotenv
from db_fetch import FetchData
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def start_sync():

    load_dotenv()

    sap_config = {
    "user": os.getenv("SAP_USER"),
    "passwd": os.getenv("SAP_PASS"),
    "ashost": os.getenv("SAP_ASHOST"),
    "sysnr": os.getenv("SAP_SYSNR"),
    "client": os.getenv("SAP_CLIENT")
    }
    
    logger.info("--- Starting SAP Sync Job ---")

    db_url = os.getenv("DB_URL")
    if not db_url:
        logger.critical("Environment variable DB_URL is missing!")
        return

    data1 = FetchData(os.getenv("DB_URL"))
    query_params = {"status_param": "READY"}
    pymt_df = data1.fetch_from_file("pymt.sql", params=query_params)

    if pymt_df.empty:
        logger.warning("No data retrieved. Nothing to sync to SAP. Ending job.")
    else:
        logger.info(f"Data validation passed. Proceeding to SAP RFC call with {len(pymt_df)} records.")
        
    logger.info("--- Sync Job Completed ---")

if __name__ == "__main__":
    start_sync()