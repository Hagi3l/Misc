def deduplicate_findings(df):
    """
    Deduplicate findings based on unique identifiers.

    :param df: DataFrame of findings.
    :return: Deduplicated DataFrame.
    """
    # Use 'Id' as the unique identifier for findings
    deduplicated_df = df.drop_duplicates(subset='Id')
    return deduplicated_df

# Deduplicate findings
deduplicated_findings = deduplicate_findings(findings_df)
print(f"Deduplicated findings: {len(deduplicated_findings)}")
