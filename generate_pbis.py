def generate_pbis_csv(df, features_df, output_file='pbis.csv'):
    """
    Generate a PBIs CSV for project teams.

    :param df: DataFrame of findings.
    :param features_df: DataFrame of features.
    :param output_file: Path to the output CSV.
    :return: DataFrame with PBIs.
    """
    # Map features to PBIs
    feature_map = features_df.set_index(['GeneratorId', 'AwsAccountId'])['FeatureId']
    df['FeatureId'] = df.apply(lambda x: feature_map.get((x['GeneratorId'], x['AwsAccountId'])), axis=1)
    
    # Add PBIs details
    df['Title'] = df['Title'].fillna('Security Hub Finding')
    df['Description'] = (
        '<b>Finding Description:</b> ' + df['Description'].astype(str) +
        '<br/><b>Account ID:</b> ' + df['AwsAccountId'].astype(str) +
        '<br/><b>Generator ID:</b> ' + df['GeneratorId'].astype(str) +
        '<br/><b>Resources:</b> ' + df['Resources'].astype(str) +
        '<br/><b>Severity:</b> ' + df['Severity.Label'].astype(str)
    )
    
    # Keep only relevant columns for PBIs
    pbis = df[['FeatureId', 'Title', 'Description', 'Id']]
    
    pbis.to_csv(output_file, index=False)
    print(f"PBIs CSV generated: {output_file}")
    return pbis

# Generate PBIs
pbis_df = generate_pbis_csv(deduplicated_findings, features_df)
