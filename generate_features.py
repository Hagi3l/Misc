# generate_features.py
import pandas as pd

def generate_features(filtered_findings_df):
    """
    Generates Features for SecOps team and saves them into CSVs with unique tags.
    :param filtered_findings_df: DataFrame of filtered findings (Critical/High)
    :return: List of CSV filenames that contain the generated features
    """
    # Create Features DataFrame
    features = pd.DataFrame({
        'Tag': [f"feature-{finding_type}-{i}" for i, finding_type in enumerate(filtered_findings_df['FindingType'], 1)],  # Tag with severity and unique index
        'Title': filtered_findings_df['Title'],  # Example title from findings
        'Description': filtered_findings_df['Description'],  # Example description from findings
    })

    # Generate chunks of features if over 1000 entries (Azure DevOps limit)
    feature_chunks = [features[i:i+1000] for i in range(0, len(features), 1000)]

    # Save Feature CSVs
    feature_csv_files = []
    for i, chunk in enumerate(feature_chunks):
        file_name = f'features_chunk_{i+1}.csv'
        chunk.to_csv(file_name, index=False)
        feature_csv_files.append(file_name)

    return feature_csv_files
