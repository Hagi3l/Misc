# main.py
from extract_findings import extract_security_hub_findings
from process_findings import process_findings
from generate_features_and_pbis import prepare_features_and_pbis

def main():
    # Step 1: Extract findings from AWS Security Hub
    findings_df = extract_security_hub_findings()
    
    # Step 2: Process findings (deduplication and filtering for severity)
    filtered_findings_df = process_findings(findings_df)

    # Step 3: Generate Features and PBIs for Azure DevOps import
    feature_csv_files, pbi_csv_files = prepare_features_and_pbis(filtered_findings_df)

    print("Feature CSV Files:", feature_csv_files)
    print("PBI CSV Files:", pbi_csv_files)

if __name__ == "__main__":
    main()
