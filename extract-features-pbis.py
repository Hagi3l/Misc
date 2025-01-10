import uuid

def prepare_features_and_pbis(filtered_findings_df):
    # Group findings to create Features based on Severity and Finding Type
    features_data = filtered_findings_df.groupby(['Severity.Label', 'Finding Type']).size().reset_index()
    features_data.columns = ['Severity.Label', 'Finding Type', 'Count']
    features_data['ID'] = [str(uuid.uuid4()) for _ in range(len(features_data))]

    # Create Feature Titles
    features_data['Title'] = features_data.apply(
        lambda row: f"{'Mitigate' if row['Severity.Label'] == 'High' else 'Resolve'} {row['Severity.Label']} Findings: {row['Finding Type']}",
        axis=1
    )

    # Create Features CSV (SecOps actions for security findings)
    features = features_data[['Title', 'Severity.Label']]
    features['Work Item Type'] = 'Feature'
    features['Description'] = features.apply(
        lambda row: f"This feature tracks resolution of all {row['Severity.Label']} severity findings for {row['Finding Type']}.",
        axis=1
    )
    features['Assigned To'] = ''  # Assign to SecOps team or leave blank
    features['Tags'] = 'SecOps, AWS, Security'

    # Break features into chunks of 1000 for Azure DevOps import limit
    feature_chunks = [features[i:i+1000] for i in range(0, len(features), 1000)]
    
    # Save Features to CSVs (without ID, Azure DevOps will auto-generate it)
    feature_csv_files = []
    for i, chunk in enumerate(feature_chunks):
        file_name = f'features_chunk_{i+1}.csv'
        chunk[['Work Item Type', 'Title', 'Description', 'Assigned To', 'Tags']].to_csv(file_name, index=False)
        feature_csv_files.append(file_name)

    # Now, create PBIs (for findings assigned to project teams)
    pbis = filtered_findings_df.copy()
    pbis['Work Item Type'] = 'Product Backlog Item'

    # Link PBIs to Features by using the 'Finding Type' (assuming you will manually map these after upload)
    pbis['Parent ID'] = pbis['Finding Type'].map(dict(zip(features_data['Finding Type'], features_data['ID'])))

    pbis['Assigned To'] = ''  # Add project team assignments here
    pbis['Tags'] = 'AWS, Security'

    # Generate detailed HTML descriptions for PBIs
    def generate_html_description(row):
        return f"""
        <h2>Finding Details</h2>
        <ul>
            <li><b>Resource:</b> {row['Resource ID']}</li>
            <li><b>Resource Type:</b> {row['Resource Type']}</li>
            <li><b>Region:</b> {row['Region']}</li>
            <li><b>AWS Account:</b> {row['Account ID']}</li>
        </ul>
        <h2>Issue Description</h2>
        <p>The finding is classified as <b>{row['Severity.Label']}</b> severity. It indicates {row['Description']}.</p>
        <p>This may lead to potential security risks, including {row['Impact']}. Immediate attention is required.</p>
        """

    # Apply HTML description generation for PBIs
    pbis['Description'] = pbis.apply(generate_html_description, axis=1)

    # Break PBIs into chunks of 1000 for Azure DevOps import limit
    pbi_chunks = [pbis[i:i+1000] for i in range(0, len(pbis), 1000)]
    
    # Save PBIs to CSVs (with Parent ID linked)
    pbi_csv_files = []
    for i, chunk in enumerate(pbi_chunks):
        file_name = f'pbis_chunk_{i+1}.csv'
        chunk[['Work Item Type', 'Title', 'Description', 'Assigned To', 'Tags', 'Parent ID']].to_csv(file_name, index=False)
        pbi_csv_files.append(file_name)

    return feature_csv_files, pbi_csv_files

# Create the Features and PBIs
feature_csvs, pbi_csvs = prepare_features_and_pbis(filtered_findings_df)

print("Feature CSVs:", feature_csvs)
print("PBI CSVs:", pbi_csvs)
