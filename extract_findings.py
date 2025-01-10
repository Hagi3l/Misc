# extract_findings.py
import boto3
import pandas as pd

def extract_security_hub_findings():
    # Create a Boto3 client for AWS Security Hub
    client = boto3.client('securityhub', region_name='us-west-2')  # Update to your region

    # Pagination for large result sets
    paginator = client.get_paginator('get_findings')
    findings = []

    for page in paginator.paginate():
        findings.extend(page['Findings'])

    # Create a DataFrame from the findings
    df = pd.DataFrame(findings)
    # Assuming these columns are available in the findings
    df = df[['Id', 'Title', 'Description', 'Severity', 'Resource', 'FindingType']]
    return df
