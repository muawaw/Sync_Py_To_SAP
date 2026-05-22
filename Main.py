#!/usr/bin/env python
import os
import logging
import sys
import json
import requests
from dotenv import load_dotenv
import urllib.parse
from sqlalchemy import create_engine 

from db_fetch import FetchData
from barcode_service import BarcodeService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def initialization():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")

    pwd = urllib.parse.quote_plus(password)

    url = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"
    
    return create_engine(url)

def start_sync():

    load_dotenv()
    
    logger.info("--- Starting SAP Sync Job ---")

    db_url = initialization()
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY") 
    barcode_enabled = os.getenv("BARCODE_ENABLED", "False").lower() == "true"
    barcode_gen = BarcodeService(active=barcode_enabled)

    if not db_url or not api_url:
        logger.critical("Environment variable DB_URL or API_URL is missing!")
        return

    data1 = FetchData(db_url, db_name="DB_SAP")
    query_params = {"status_param": "READY"}
    pos_df = data1.fetch_from_file("posisi.sql", params=query_params)

<<<<<<< HEAD
    pos_df['psabv'] = pos_df['psabv'].astype(str).str.strip()
    pos_df['pstxt'] = pos_df['pstxt'].astype(str).str.strip().str.upper()

=======
>>>>>>> 9177ddb734d7ad0cd3a6731e46c01a98ae87e4cd
    breakpoint()

    if pos_df.empty:
        logger.warning("No data retrieved from DB. Ending job.")
        return
    
    records_to_send = []

<<<<<<< HEAD
    all_pymt_df = data1.fetch_from_file("pymt.sql")
    name_lookup = dict(zip(pos_df['pernr'].astype(str).str.strip(), pos_df['psabv']))

    for _, row in pos_df.iterrows():
    
        pos_nomenklatur = row['plans']      # NOMENKLATUR == plans
        pos_short_text  = row['psabv']  # DESK_KODE_REL == psabv
        pos_long_text   = row['pstxt']   # DESK_JABATAN == pstxt
        pos_name = row['name'] # NAMA PEJABAT
        pos_nik = row['pernr'] # NIK/NIPP

        pymt_df = all_pymt_df[all_pymt_df['pernr'] == pos_nik]

        logger.info(f"Checking PYMT for: [{pos_nik}] {pos_name}")

        if not pymt_df.empty:
            leave_record = pymt_df.iloc[0]

            pymt_id = leave_record['pelakhar']
            nomenklatur_pymt = name_lookup.get(pymt_id, "Lookup Failed")
            
            active_id   = leave_record['pernr']
            pymt        = nomenklatur_pymt 
            begda       = leave_record['tgl_mulai']
            endda       = leave_record['tgl_berakhir']
            is_sub      = True
        else:
            active_name = pos_name
            active_id   = pos_nik
=======
    for _, row in pos_df.iterrows():
    
        pos_nomenklatur = row['python_pos_id']      # NOMENKLATUR (MATCHING ZTABLE SAP)
        pos_short_text  = row['python_short_text']  # DESK_KODE_REL (MATCHING ZTABLE SAP)
        pos_long_text   = row['python_long_text']   # DESK_JABATAN (MATCHING ZTABLE SAP)
        orig_id   = row['python_emp_id']   # maps to employee ID
        orig_name = row['python_emp_name'] # maps to employee Name
        pos_id    = row['python_pos_id']  # maps to Position ID

        logger.info(f"Checking PYMT for: {orig_name}")
        
        pymt_df = FetchData.fetch_from_file(
            "pymt.sql", #maps to PYMT history sql
            params={"emp_id": orig_id}
        )

        if not pymt_df.empty:
            leave_record = pymt_df.iloc[0]
            
            # [ACTION]: These names must match what your 2nd SQL file returns
            active_name = leave_record['python_sub_name']
            active_id   = leave_record['python_sub_id']
            # Per your logic: KODE_PYMT should point to the substitute's role/link
            pymt        = leave_record['python_sub_short_text'] 
            begda       = leave_record['start_date']
            endda       = leave_record['end_date']
            is_sub      = True
        else:
            active_name = orig_name
            active_id   = orig_id
>>>>>>> 9177ddb734d7ad0cd3a6731e46c01a98ae87e4cd
            pymt        = ""
            begda       = "" 
            endda       = ""
            is_sub      = False

<<<<<<< HEAD
        barcode_b64 = None
        if barcode_enabled:
            logger.info(f"Generating digital sign for {active_name}")
        
            sig_key = f"{pos_nomenklatur}_{active_id}"
            barcode_b64 = barcode_gen.generate_barcode_as_base64(sig_key)
            if barcode_b64:
                logger.info(f"Barcode succesfully generated for {active_name}")
            else:
                logger.info(f"Failed to generate barcode for {active_name}")

        z_record = {
            "ID_PEJABAT": "",        # Let SAP handle numbering/auto-inc
            "KODE_GROUP_PR": "",     # Optional
            "KODE_GROUP": "",        # Optional
            "KODE_RELEASE_PR": "",   # Optional
            "KODE_RELEASE": "",      # Optional
            "DESK_KODE_REL": pos_short_text,  
            "NOMENKLATUR": pos_nomenklatur,
            "DESK_JABATAN": pos_long_text,
            "NAMA_PEJABAT": active_name,
            "TANDA_TANGAN": barcode_b64,      # The Base64 BMP
            "KODE_PYMT": pymt,          
            "KODE_POSISI": "",       # Optional
            "BEGDA": begda,
            "ENDDA": endda
        }
        records_to_send.append(z_record)

=======
    barcode_b64 = None
    if barcode_enabled:
        logger.info(f"Generating digital sign for {active_name}")
    
        sig_key = f"{pos_nomenklatur}_{active_id}"
        barcode_b64 = barcode_gen.generate_barcode_as_base64(sig_key)
        if barcode_b64:
            logger.info(f"Barcode succesfully generated for {active_name}")
        else:
            logger.info(f"Failed to generate barcode for {active_name}")

    z_record = {
        "ID_PEJABAT": "",        # Let SAP handle numbering/auto-inc
        "KODE_GROUP_PR": "",     # Optional
        "KODE_GROUP": "",        # Optional
        "KODE_RELEASE_PR": "",   # Optional
        "KODE_RELEASE": "",      # Optional
        "DESK_KODE_REL": pos_short_text,  
        "NOMENKLATUR": pos_nomenklatur,
        "DESK_JABATAN": pos_long_text,
        "NAMA_PEJABAT": active_name,
        "TANDA_TANGAN": barcode_b64,      # The Base64 BMP
        "KODE_PYMT": pymt,          
        "KODE_POSISI": "",       # Optional
        "BEGDA": begda,
        "ENDDA": endda
    }
        
    records_to_send.append(z_record)
>>>>>>> 9177ddb734d7ad0cd3a6731e46c01a98ae87e4cd
    logger.info(f"Prepared {len(records_to_send)} records for delivery.")
    
    try:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": api_key
        }
        
        response = requests.post(
            api_url, 
            json=records_to_send, 
            headers=headers,
            timeout=30          
        )

        if response.status_code == 200:
            logger.info("Successfully send data to API.")
        else:
            logger.error(f"Error to send data to API, Status: {response.status_code}, Msg: {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"CRITICAL: Network error, Failed to connect: {e}")

    logger.info("--- Sync Job Completed ---")

if __name__ == "__main__":
    start_sync()