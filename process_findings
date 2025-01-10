# process_findings.py

def process_findings(findings_df, severity_filter=['Critical', 'High']):
    """
    Deduplicates the findings and filters them based on severity (Critical/High).
    :param findings_df: DataFrame of raw findings
    :param severity_filter: List of severity labels to filter by (default is ['Critical', 'High'])
    :return: Filtered DataFrame with deduplicated and severity-filtered findings
    """
    # Ensure the Finding ID is a string and drop duplicates based on this ID
    findings_df['Finding ID'] = findings_df['Finding ID'].apply(str)
    findings_df.drop_duplicates(subset=['Finding ID'], keep='last', inplace=True)

    # Filter findings by severity
    filtered_findings = findings_df[findings_df['Severity.Label'].isin(severity_filter)]
    
    return filtered_findings
