import pandas as pd
import uuid

def generate_features_csv(findings_df, output_file):
    """
    Generates a CSV file for Azure DevOps features based on Security Hub findings.

    :param findings_df: A Pandas DataFrame containing deduplicated findings.
    :param output_file: The path of the CSV file to generate.
    :return: A DataFrame of generated features.
    """
    # Step 1: Group findings by unique categories to generate features
    grouped_findings = findings_df.groupby(['ProductName', 'AwsAccountId', 'Region'])
    
    # Step 2: Initialize a list to store features
    features = []

    # Step 3: Loop through each group of findings
    for group_key, group in grouped_findings:
        product_name, account_id, region = group_key
        
        # Generate a unique title for the feature
        title = f"{product_name} | Account: {account_id} | Region: {region}"
        
        # Generate a UUID for traceability
        unique_tag = str(uuid.uuid4())
        
        # Create a dictionary representing the feature
        feature = {
            'Title': title,
            'Description': (
                f"This feature tracks findings for product '{product_name}' "
                f"in account '{account_id}' and region '{region}'."
            ),
            'Tags': unique_tag,  # Use the UUID as a Tag for traceability
        }
        
        # Append the feature to the list
        features.append(feature)

    # Step 4: Convert the features list to a DataFrame
    features_df = pd.DataFrame(features)
    
    # Step 5: Save the DataFrame to a CSV file
    features_df.to_csv(output_file, index=False)
    
    return features_df

# Example usage
if __name__ == "__main__":
    # Load deduplicated findings (example CSV as input)
    findings_df = pd.read_csv('deduplicated_findings.csv')
    features_csv = 'features.csv'
    features_df = generate_features_csv(findings_df, features_csv)
    print(f"Features CSV generated: {features_csv}")
