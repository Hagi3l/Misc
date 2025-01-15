import pandas as pd

def generate_pbis_csv(findings_df, features_df, output_file):
    """
    Generates a CSV file for Azure DevOps PBIs based on Security Hub findings.

    :param findings_df: A Pandas DataFrame containing deduplicated findings.
    :param features_df: A DataFrame of generated features (with Tags).
    :param output_file: The path of the CSV file to generate.
    :return: A DataFrame of generated PBIs.
    """
    # Merge findings with features on shared columns (e.g., ProductName, AccountId, Region)
    findings_with_features = findings_df.merge(
        features_df, 
        left_on=['ProductName', 'AwsAccountId', 'Region'], 
        right_on=['Title', 'Account', 'Region'], 
        how='left'
    )
    
    # Initialize a list to store PBIs
    pbis = []

    for _, row in findings_with_features.iterrows():
        # Create a dictionary representing the PBI
        pbi = {
            'Title': f"Fix {row['FindingId']}",
            'Description': row['Description'],
            'Severity': row['SeverityLabel'],
            'Tags': row['Tags'],  # Inherit the Feature's tag for linking
        }
        pbis.append(pbi)

    # Convert the PBIs list to a DataFrame
    pbis_df = pd.DataFrame(pbis)
    
    # Save the DataFrame to a CSV file
    pbis_df.to_csv(output_file, index=False)
    
    return pbis_df

# Example usage
if __name__ == "__main__":
    # Load deduplicated findings and features
    findings_df = pd.read_csv('deduplicated_findings.csv')
    features_df = pd.read_csv('features.csv')
    pbis_csv = 'pbis.csv'
    pbis_df = generate_pbis_csv(findings_df, features_df, pbis_csv)
    print(f"PBIs CSV generated: {pbis_csv}")
