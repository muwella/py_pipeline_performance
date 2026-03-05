# 📖 Developer Documentation

Welcome to the Developer Wiki for the **RPA Analytics Pipeline**. This document outlines the system architecture, module responsibilities, and data schemas to help new developers and data analysts understand and extend the project.

---

## 🏗️ System Architecture & Data Flow

The project follows a classic ETL (Extract, Transform, Load) architecture, designed to process transactional logs from RPA orchestrators (like Blue Prism) and enrich them with static business dimensions.

1. **Extract:** Reads daily execution logs and static master data (Automations and Markets) from `data/inputs/`.
2. **Transform:** Applies business logic using vectorization in `pandas`. It calculates the actual human time saved based on FTEs, working hours, and transaction volumes, and categorizes exceptions into System or Business errors.
3. **Load:** Outputs a flattened, denormalized dataset (`dev_analytics_dataset.csv` or `prod_analytics_dataset.csv`) to `data/outputs/`, ready to be ingested by BI tools (Power BI, Tableau) using a Star Schema or Single-Table approach.

---

## 🧩 Module Breakdown (`src/`)

* **`config.py`**: The central source of truth for all file paths and directory structures. It uses `os.path.join` to ensure cross-platform compatibility.
* **`parser.py`**: Handles CLI arguments using `argparse`. Defines the execution mode (`--mode DEV` or `--mode PROD`).
* **`simulator.py`**: A synthetic data generator used exclusively in `DEV` mode. It builds realistic DataFrames for markets, automations, and transactional logs, simulating realistic execution times and exception rates over a 90-day period.
* **`etl.py`**: Contains the core business logic.
  * Merges Master Data with Transactional Logs.
  * Parses exception reasons to classify them (`exception_classification`).
  * Calculates financial ROI metrics (`Net_Time_Saved_Mins`).
* **`main.py`**: The main orchestrator. It initializes the logger, parses arguments, validates the existence of required input files (`init_file_validations`), and triggers the ETL process.

---

## 📊 Data Dictionary (Output Schema)

The final dataset generated in `data/outputs/` contains the following key calculated fields, which are meant to be consumed by the BI layer:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Item Key` | String | Unique identifier for the transaction (Queue Item). |
| `AUT_ID` | String | Unique identifier for the RPA Process. |
| `AUT_NAME` | String | Human-readable name of the automated process. |
| `MARKET` | String | Country code (e.g., AR, MX, CO). |
| `Created` / `Ended` | Datetime | Start and end timestamps of the item processing. |
| `Duration` | Float | Bot execution time in seconds. |
| `Status` | String | Final status of the queue item (`Completed` or `Exception`). |
| `Items_Processed` | Integer | Binary flag (`1` for Success, `0` for Exception). |
| `Exception Reason`| String | Raw error message from the RPA orchestrator. |
| `Exception_Category`| String | Classified error: `Success`, `System Exception`, or `Business Exception`. |
| `Human_Mins_Per_Item`| Float | Theoretical human minutes required to process one item manually. |
| `Net_Time_Saved_Mins`| Float | Total ROI in minutes: *(Human_Mins_Per_Item * Items_Processed) - Bot_Time_Mins*. |

---

## 🚀 How to Extend the Project

### Adding a New Market
To add a new country to the pipeline, update the `markets_master.csv` file in the `data/inputs/` directory with the country code and the standard monthly working hours for that region.

### Adding a New Automation
Update the `automations_master.csv` file. You must provide:
1. `AUT_ID` and `AUT_NAME`.
2. `MARKET` (Must exist in the markets master file).
3. `FTE` (Full-Time Equivalent human effort recovered).
4. `EXPECTED_MONTHLY_VOL` (Expected monthly transactions to calculate per-item value).