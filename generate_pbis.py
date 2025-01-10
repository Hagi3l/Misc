# generate_pbis.py
import pandas as pd

def generate_pbis(filtered_findings_df, features_data):
    """
    Generates PBIs and links them to Features using Tags after the features have been uploaded to Azure DevOps.
    :param filtered_findings_df: DataFrame of filtered findings (Critical/High)
    :param features_data: DataFrame of features with Tags (extracted after uploading features)
    :return: List of CSV filenames that contain the generated PBIs
    """
    # Create PBIs DataFrame (product backlog items for project teams)
    pbis = filtered_findings_df.copy()
    pbis['Work Item Type'] = 'Product Backlog Item'

    # Generate Tags for PBIs based on Feature Title
    pbis['Tag'] = pbis['FindingType'].map(
        dict(zip(features_data['Title'], features_data['Tag']))
    )
    
    # Check if there are any unmatched PBIs
    unmatched_pbis = pbis[pbis['Tag'].isna()]
    if not unmatched_pbis.empty:
        print(f"Warning: {len(unmatched_pbis)} PBIs couldn't be matched to Features.")
    
    pbis['Assigned To'] = ''  # Add project team assignments here
    pbis['Tags'] = pbis['Tag']  # Ensure the same tag is added to PBI for easy filtering

    # Generate HTML descriptions for PBIs
    def generate_html_description(row):
        return f"""
        <h2>Finding Details</h2>
        <ul>
            <li><b>Resource:</b> {row['Resource']}</li>
            <li><b>Severity:</b> {row['Severity']}</li>
            <li><b>Description:</b> {row['Description']}</li>
        </ul>
        """
    
    pbis['HTML Description'] = pbis.apply(generate_html_description, axis=1)

    # Generate chunks of PBIs if over 1000 entries (Azure DevOps limit)
    pbi_chunks = [pbis[i:i+1000] for i in range(0, len(pbis), 1000)]

    # Save PBI CSVs
    pbi_csv_files = []
    for i, chunk in enumerate(pbi_chunks):
        file_name = f'pbis_chunk_{i+1}.csv'
        chunk.to_csv(file_name, index=False)
        pbi_csv_files.append(file_name)

    return pbi_csv_files
