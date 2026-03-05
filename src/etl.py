import config
import logging
import os
import pandas as pd
import numpy as np

def etl(logs_path, output_path):
    logging.info("START")
    
    try:
        df_aut = pd.read_csv(config.AUT_MASTER_PATH)
        df_mkt = pd.read_csv(config.MKT_MASTER_PATH)
        df_logs = pd.read_csv(logs_path)
                
        df_logs['Duration'] = df_logs['Duration'].astype(float)
        df_logs['Items_Processed'] = np.where(df_logs['Status'] == 'Completed', 1, 0)

        df_master = pd.merge(df_aut, df_mkt, on='MARKET', how='left')
        df_master['Human_Mins_Per_Item'] = (df_master['FTE'] * df_master['MONTHLY_HOURS'] * 60) / df_master['EXPECTED_MONTHLY_VOL']
        
        df_final = pd.merge(
            df_logs, 
            df_master[['AUT_ID', 'AUT_NAME', 'MARKET', 'Human_Mins_Per_Item']], 
            on='AUT_ID', 
            how='left'
        )
        
        def exception_classification(reason):
            if pd.isna(reason) or reason == "": return "Success"
            elif "Business" in str(reason): return "Business Exception"
            else: return "System Exception"
                
        df_final['Exception_Category'] = df_final['Exception Reason'].apply(exception_classification)
        
        df_final['Human_Time_Saved_Mins'] = df_final['Items_Processed'] * df_final['Human_Mins_Per_Item']
        df_final['Bot_Time_Mins'] = df_final['Duration'] / 60
        df_final['Net_Time_Saved_Mins'] = df_final['Human_Time_Saved_Mins'] - df_final['Bot_Time_Mins']
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_final.to_csv(output_path, index=False)

        logging.info("END")
  
    except Exception as e:
        logging.exception("An exception occurred during the ETL process")