# main.py
import pandas as pd
from extract_findings import extract_security_hub_findings
from process_findings import filter_and_deduplicate_findings
from generate_features import generate_features
from generate_pbis import generate_pbis

def main():
    # Step 1: Extract Security Hub findings
    findings_df = extract_security_hub_findings()
    print(f"Extracted {len(findings_df)} findings from AWS Security Hub.")

    # Step 2: Filter and deduplicate the findings
    filtered_findings_df = filter_and_deduplicate_findings(findings_df)
    print(f"Filtered findings to {len(filtered_findings_df)} critical/high findings.")

    # Step 3: Generate Features for SecOps team
    feature_files = generate_features(filtered_findings_df)
    print(f"Generated {len(feature_files)} feature CSV files.")
    
    # Step 4: Wait for user confirmation that features have been uploaded
    input("Please upload the feature CSVs to Azure DevOps. Press Enter when done.")

    # Step 5: Load features data (Assuming the user uploads the file with features data)
    features_data = pd.read_csv('features_chunk_1.csv')  # Load first chunk or any relevant chunk

    # Step 6: Generate PBIs and link to features using tags
    pbi_files = generate_pbis(filtered_findings_df, features_data)
    print(f"Generated {len(pbi_files)} PBI CSV files.")

if __name__ == '__main__':
    main()
