import boto3
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image
import matplotlib.pyplot as plt

# Initialize Security Hub client
securityhub_client = boto3.client('securityhub')

# Function to fetch security hub findings
def fetch_security_scores(accounts):
    data = []
    for account_id in accounts:
        response = securityhub_client.describe_standards_controls(
            StandardsSubscriptionArn=f"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
        )
        for control in response['Controls']:
            data.append({
                'Account': account_id,
                'ControlId': control['ControlId'],
                'Title': control['Title'],
                'SeverityRating': control.get('SeverityRating', 'N/A'),
                'Status': control['ControlStatus'],
                'ComplianceStatus': control['ControlStatusReason'][0]['Reason'] if 'ControlStatusReason' in control else 'N/A',
            })
    return data

# Accounts to fetch data for
aws_accounts = ['123456789012', '098765432109']  # Replace with your AWS account IDs
security_scores = fetch_security_scores(aws_accounts)

# Create a DataFrame
df = pd.DataFrame(security_scores)

# Create Excel workbook
wb = Workbook()
ws1 = wb.active
ws1.title = "Security Hub Data"

# Write data to Excel
for row in dataframe_to_rows(df, index=False, header=True):
    ws1.append(row)

# Create meaningful graphs
def create_graphs(df):
    # Graph 1: Control Status Count
    status_count = df['Status'].value_counts()
    plt.figure(figsize=(8, 6))
    status_count.plot(kind='bar', color='skyblue', title='Control Status Count')
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('control_status_count.png')

    # Graph 2: Compliance Status Distribution
    compliance_count = df['ComplianceStatus'].value_counts()
    plt.figure(figsize=(8, 6))
    compliance_count.plot(kind='pie', autopct='%1.1f%%', title='Compliance Status Distribution')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('compliance_status_distribution.png')

    return ['control_status_count.png', 'compliance_status_distribution.png']

graph_images = create_graphs(df)

# Add graphs to a new sheet in Excel
ws2 = wb.create_sheet("Graphs")

for i, graph_image in enumerate(graph_images):
    img = Image(graph_image)
    img.anchor = f'A{i * 20 + 1}'  # Positioning graphs
    ws2.add_image(img)

# Save the workbook
wb.save("SecurityHub_Report.xlsx")

print("Report generated: SecurityHub_Report.xlsx")
