# process_findings.py
import pandas as pd

def filter_and_deduplicate_findings(df):
    # Filter for Critical and High severity findings
    filtered_df = df[df['Severity'].isin(['Critical', 'High'])]

    # Deduplicate based on the 'Id' of the findings
    deduplicated_df = filtered_df.drop_duplicates(subset='Id')

    return deduplicated_df
