import config
import parser
import logging
import os
from simulator import generate_input
import etl

def init_logger():
    logging.basicConfig(
        level=logging.INFO,
        format=f"{parser.args.mode} - %(asctime)s - [%(module)s.%(funcName)s]: %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def init_file_validations(logs_path):
    required_files = [
        config.AUT_MASTER_PATH,
        config.MKT_MASTER_PATH,
        logs_path
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
      logging.error(f"Missing input files: {missing_files}")
      return False
    return True

def main():
    parser.init_parser()
    init_logger()
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    if parser.args.mode == 'DEV':
        logs_path = config.LOGS_DEV_PATH
        output_path = config.OUTPUT_DEV_PATH
        generate_input()
    else:
        logs_path = config.LOGS_PROD_PATH
        output_path = config.OUTPUT_PROD_PATH

    if init_file_validations(logs_path):
        etl.etl(logs_path, output_path)

if __name__ == "__main__":
    main()