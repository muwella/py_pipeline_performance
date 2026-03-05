import os

# *** GENERAL ***
BASE_DIR = "data"
INPUT_DIR = os.path.join(BASE_DIR, "inputs")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# *** INPUT ***
MKT_MASTER_PATH = os.path.join(INPUT_DIR, "markets_master.csv")
AUT_MASTER_PATH = os.path.join(INPUT_DIR, "automations_master.csv")
LOGS_DEV_PATH = os.path.join(INPUT_DIR, "dev_raw_logs.csv")
LOGS_PROD_PATH = os.path.join(INPUT_DIR, "prod_raw_logs.csv")

# *** OUTPUT ***
OUTPUT_DEV_PATH = os.path.join(OUTPUT_DIR, "dev_analytics_dataset.csv")
OUTPUT_PROD_PATH = os.path.join(OUTPUT_DIR, "prod_analytics_dataset.csv")