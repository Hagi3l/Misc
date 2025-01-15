import uuid

def generate_features_csv(df, output_file='features.csv'):
    """
    Generate a features CSV for SecOps.

    :param df: DataFrame of findings.
    :param output_file: Path to the output CSV.
    :return: DataFrame with features.
    """
    features = df[['GeneratorId', 'AwsAccountId']].drop_duplicates()
    features['FeatureId'] = [str(uuid.uuid4()) for _ in range(len(features))]
    features['Title'] = 'Security Finding Remediation'  # Generic title
    features['Description'] = 'Actions required by SecOps team for remediation.'

    features.to_csv(output_file, index=False)
    print(f"Features CSV generated: {output_file}")
    return features

# Generate features
features_df = generate_features_csv(deduplicated_findings)
