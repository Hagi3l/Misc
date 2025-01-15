import boto3
import pandas as pd

def extract_findings(severity_levels, region_name='us-west-2'):
    """
    Extract findings from AWS Security Hub.

    :param severity_levels: List of severity levels to filter (e.g., ['CRITICAL', 'HIGH']).
    :param region_name: AWS region to query.
    :return: A Pandas DataFrame containing all findings.
    """
    client = boto3.client('securityhub', region_name=region_name)
    findings = []
    
    paginator = client.get_paginator('get_findings')
    response_iterator = paginator.paginate(
        Filters={
            'SeverityLabel': {'Value': severity_levels, 'Comparison': 'IN'}
        }
    )

    for page in response_iterator:
        findings.extend(page['Findings'])

    # Normalize findings into a DataFrame
    df = pd.json_normalize(findings)

    return df

# Example Usage
severity_levels = ['CRITICAL', 'HIGH']  # Focus on critical and high findings for now
findings_df = extract_findings(severity_levels)
print(f"Extracted {len(findings_df)} findings")
