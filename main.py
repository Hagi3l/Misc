import time
from extract_findings import extract_findings
from deduplicate_findings import deduplicate_findings
from generate_features import generate_features_csv
from generate_pbis import generate_pbis_csv

def main():
    """
    Main script to extract findings, generate features, and create PBIs.
    """
    # Step 1: Extract Findings
    print("Extracting findings from AWS Security Hub...")
    severity_levels = ['CRITICAL', 'HIGH']  # You can expand this later to include other severities
    findings_df = extract_findings(severity_levels)
    print(f"Extracted {len(findings_df)} findings")

    # Step 2: Deduplicate Findings
    print("Deduplicating findings...")
    deduplicated_findings = deduplicate_findings(findings_df)
    print(f"Deduplicated findings: {len(deduplicated_findings)}")

    # Step 3: Generate Features CSV
    print("Generating features CSV...")
    features_file = 'features.csv'
    features_df = generate_features_csv(deduplicated_findings, features_file)
    print(f"Features CSV generated: {features_file}")

    # Pause for user confirmation to upload features to Azure DevOps
    print("\n--- Action Required ---")
    print("Upload the 'features.csv' file to Azure DevOps and extract the Feature IDs into 'features_with_ids.csv'.")
    print("Press Enter once the 'features_with_ids.csv' file is ready.")
    input()  # Wait for user confirmation

    # Step 4: Generate PBIs CSV
    print("Generating PBIs CSV...")
    features_with_ids_file = 'features_with_ids.csv'  # File containing Feature IDs after upload
    pbis_file = 'pbis.csv'
    generate_pbis_csv(deduplicated_findings, features_with_ids_file, pbis_file)
    print(f"PBIs CSV generated: {pbis_file}")

    print("\n--- Process Completed ---")
    print("Both 'features.csv' and 'pbis.csv' have been generated. You can now upload them to Azure DevOps.")

if __name__ == "__main__":
    main()
