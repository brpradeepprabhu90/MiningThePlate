
import pandas as pd
import pyreadstat
def xpt_to_csv(xpt_file, csv_file):
    #df.to_csv('MCQ_23.csv', index=False)

    # Read XPT file
    df = pd.read_sas(xpt_file, format='xport')
    
    # Save to CSV
    df.to_csv(csv_file, index=False)
    print(f"Converted {xpt_file} to {csv_file}")


def readStatToCsv(stat_file, csv_file):
    df, meta = pyreadstat.read_sas7bdat(stat_file)
    df.to_csv(csv_file, index=False)

readStatToCsv("nsch_2024e_screener.sas7bdat", "nsch_2024e_screener.csv")