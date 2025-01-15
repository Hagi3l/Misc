def main():
    # Step 1: Extract findings
    severity_levels = ['CRITICAL', 'HIGH']
    findings_df = extract_findings(severity_levels)
    
    # Step 2: Deduplicate findings
    deduplicated_findings = deduplicate_findings(findings_df)
    
    # Step 3: Generate features CSV
    features_df = generate_features_csv(deduplicated_findings)
    
    # Step 4: Wait for user confirmation to upload features and extract IDs
    input("Please upload 'features.csv' to Azure DevOps and extract the IDs. Press Enter to continue.")
    
    # Step 5: Generate PBIs CSV
    pbis_df = generate_pbis_csv(deduplicated_findings, features_df)

if __name__ == '__main__':
    main()
