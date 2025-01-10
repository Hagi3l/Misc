Sure! Let's walk through the entire process step-by-step, and I'll provide you with the full code for extracting AWS Security Hub findings, deduplicating them, creating Features and PBIs, and uploading them to Azure DevOps in chunks (ensuring that the CSV contains a maximum of 1000 items due to Microsoft’s import limit).

1. Extract Findings from AWS Security Hub

We'll start by extracting the findings from AWS Security Hub.

import boto3
import pandas as pd

# Assuming you already have the AWS credentials set up via AWS CLI or environment variables
def extract_security_hub_findings():
    client = boto3.client('securityhub', region_name='us-east-1')
    
    # Fetch the findings from AWS Security Hub (maximum 100 results per page)
    paginator = client.get_paginator('get_findings')
    findings = []
    
    for page in paginator.paginate():
        findings.extend(page['Findings'])

    # Normalize the JSON response into a DataFrame
    df = pd.json_normalize(findings)
    
    # Optional: Save the findings into a CSV
    df.to_csv('security_hub_findings.csv', index=False)
    return df

# Call the extraction function
findings_df = extract_security_hub_findings()

2. Deduplicate and Filter the Findings (Critical and High)

Now that we have the findings, we'll remove duplicates and filter them to keep only Critical and High severity levels.

# Deduplicate and filter for Critical and High severity
def process_findings(findings_df, severity_filter=['Critical', 'High']):
    # Deduplicate based on 'Finding ID' (ensure they are string type)
    findings_df['Finding ID'] = findings_df['Finding ID'].apply(str)
    findings_df.drop_duplicates(subset=['Finding ID'], keep='last', inplace=True)

    # Filter based on severity
    filtered_findings = findings_df[findings_df['Severity.Label'].isin(severity_filter)]
    
    return filtered_findings

filtered_findings_df = process_findings(findings_df)

3. Create Features and PBIs (with HTML Details)

Features (Parent Work Items)

Each Feature will be created for a specific severity and finding type.

Each Feature will be used to track the resolution of findings.


PBIs (Child Work Items)

Each PBI will represent a single finding and will be linked to its corresponding Feature.


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
        <p>This may lead to potential security risks, including {row['Impact']}.</p>
        <h2>Resolution Guidance</h2>
        <p>Please follow these steps to resolve the issue:</p>
        <ol>
            <li>{row['Remediation Steps']}</li>
        </ol>
        <p>For more information, refer to <a href='{row['Documentation Link']}'>AWS Documentation</a>.</p>
        <h2>Compliance Standards Violated</h2>
        <ul>
            <li>{row['Compliance Standards Violated']}</li>
        </ul>
        """

    pbis['Description'] = pbis.apply(generate_html_description, axis=1)

    # Break PBIs into chunks of 1000 for Azure DevOps import limit
    pbi_chunks = [pbis[i:i+1000] for i in range(0, len(pbis), 1000)]

    # Save PBIs to CSVs (without ID, Azure DevOps will auto-generate it)
    pbi_csv_files = []
    for i, chunk in enumerate(pbi_chunks):
        file_name = f'pbis_chunk_{i+1}.csv'
        chunk[['Work Item Type', 'Title', 'Description', 'Assigned To', 'Parent ID', 'Tags']].to_csv(file_name, index=False)
        pbi_csv_files.append(file_name)

    return feature_csv_files, pbi_csv_files

# Call the function to prepare Features and PBIs CSV files
feature_files, pbi_files = prepare_features_and_pbis(filtered_findings_df)

# Output the created files
print("Feature CSV files created:", feature_files)
print("PBI CSV files created:", pbi_files)

4. Handling File Uploads to Azure DevOps

Once the CSV files for Features and PBIs are created, you can manually upload them to Azure DevOps via the web interface, or you can use the Azure DevOps REST API to automate the import. Here's a quick overview of how to do it with the REST API:

Example API to Upload CSV to Azure DevOps:

import requests

def upload_to_azure_devops(file_path, organization, project, pat_token):
    url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/${file_path}?api-version=6.0'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {HTTPBasicAuth("", pat_token)}'
    }

    with open(file_path, 'rb') as file:
        response = requests.post(url, headers=headers, files={'file': file})
        if response.status_code == 200:
            print(f"Successfully uploaded {file_path}")
        else:
            print(f"Failed to upload {file_path}: {response.text}")

# Usage
upload_to_azure_devops('features_chunk_1.csv', 'your_organization', 'your_project', 'your_personal_access_token')
upload_to_azure_devops('pbis_chunk_1.csv', 'your_organization', 'your_project', 'your_personal_access_token')

Summary

This process handles the entire flow:

1. Extract findings from AWS Security Hub.


2. Deduplicate and filter for Critical and High severity.


3. Create Features for SecOps teams and PBIs for project teams.


4. Chunk the CSV files into groups of 1000 to comply with Azure DevOps limits.


5. Optionally, automate the upload to Azure DevOps using the REST API or manual upload.



Let me know if you need more details on any specific part of the process!

