import config
import logging
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_input(num_records=5000):
    logging.info("START")
    np.random.seed(42)
    random.seed(42)

    markets_data = {
        'MARKET': [
            'AR', 'BO', 'BR', 'CL', 'CO', 'CR', 'CU', 'DO', 'EC', 'SV', 
            'GT', 'HN', 'MX', 'NI', 'PA', 'PY', 'PE', 'PR', 'UY', 'VE'
        ],
        'MONTHLY_HOURS': [
            160, 192, 176, 168, 170, 192, 176, 176, 160, 176, 
            192, 176, 180, 192, 192, 192, 192, 160, 176, 160
        ]
    }
    df_markets = pd.DataFrame(markets_data)
    df_markets.to_csv(config.MKT_MASTER_PATH, index=False)

    automations_data = {
        'AUT_ID': [f'AUT000{3619+i}' for i in range(12)],
        'AUT_NAME': [
            'Technical Closing of Orders', 'Invoice Posting SAP', 'HR Onboarding', 'Bank Reconciliation',
            'Payroll Processing', 'Vendor Master Data', 'IT Helpdesk Password Reset', 'Supply Chain Tracking',
            'Expense Report Audit', 'Lead Generation Scraper', 'Compliance Reporting', 'Customer Support Routing'
        ],
        'MARKET': ['AR', 'MX', 'CO', 'CL', 'BR', 'PE', 'UY', 'CR', 'PA', 'EC', 'AR', 'MX'],
        'FTE': [9.1, 4.5, 2.0, 1.5, 8.0, 3.5, 1.2, 4.8, 1.8, 2.2, 5.5, 6.5],
        'EXPECTED_MONTHLY_VOL': [2000, 5000, 150, 800, 3500, 2000, 500, 3000, 600, 800, 2500, 4500]
    }
    df_automations = pd.DataFrame(automations_data)
    df_automations.to_csv(config.AUT_MASTER_PATH, index=False)

    start_date = datetime.now() - timedelta(days=90)
    data = []
    aut_ids = df_automations['AUT_ID'].tolist()

    for i in range(num_records):
        aut_id = random.choice(aut_ids)
        
        random_days = random.randint(0, 90)
        created = start_date + timedelta(days=random_days, hours=random.randint(8, 18), minutes=random.randint(0, 59))
        
        success_prob = 0.85 + ((random_days / 90) * 0.13)
        status = random.choices(['Completed', 'Exception'], weights=[success_prob, 1 - success_prob])[0]
        
        exception_reason = ""
        if status == 'Exception':
            exc_type = random.choices(['System', 'Business'], weights=[0.2, 0.8])[0]
            if exc_type == 'System':
                exception_reason = random.choice(["Target application could not be identified", "Timeout waiting for screen"])
                duration_sec = random.randint(5, 15)
            else:
                exception_reason = random.choice(["Business Exception: Invalid Tax ID", "Business Exception: Missing mandatory field", "Business Exception: Account locked"])
                duration_sec = random.randint(15, 60)
        else:
            duration_sec = max(5, int(np.random.normal(loc=45, scale=15)))
        
        ended = created + timedelta(seconds=duration_sec)
        
        data.append({
            'Item Key': f"ITEM-{10000+i}-{aut_id}",
            'Priority': random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0],
            'Status': status,
            'Tags': "",
            'Resource': random.choice(["VM-BP-PROD-01", "VM-BP-PROD-02", "VM-BP-PROD-03"]),
            'Attempt': 1,
            'Created': created.strftime('%Y-%m-%d %H:%M:%S'),
            'Ended': ended.strftime('%Y-%m-%d %H:%M:%S'),
            'Duration': duration_sec,
            'Exception Reason': exception_reason,
            'AUT_ID': aut_id
        })

    df_logs = pd.DataFrame(data)
    df_logs.to_csv(config.LOGS_DEV_PATH, index=False)

    logging.info("END")