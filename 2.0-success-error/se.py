import pandas as pd
import matplotlib.pyplot as plt
from google.colab import files

# Upload CSV
print("Upload operation_logs.csv")
uploaded = files.upload()
filename = list(uploaded.keys())[0]
print("\nUploaded File:", filename)

# Load Dataset
df = pd.read_csv(filename)
print("\nDataset Preview")
display(df.head())

# Data Validation
print("\nDataset Information")
print(df.info())
print("\nMissing Values")
print(df.isnull().sum())
print("\nTotal Records:")
print(len(df))

# Convert timestamp
df['created_at'] = pd.to_datetime(
    df['created_at']
)

#HTTP Response classification
# Success responses
df['success'] = df['status_code'].between(200,299)

# Client-side errors
df['client_error'] = df['status_code'].between(400,499)

# Server-side errors
df['server_error'] = df['status_code'].between(500,599)

# Performance Metrics
total_operations = len(df)
successful_operations = df['success'].sum()
client_errors = df['client_error'].sum()
server_errors = df['server_error'].sum()
total_errors = client_errors + server_errors
success_rate = (successful_operations/total_operations)*100
error_rate = (total_errors/total_operations)*100

print("\n====================================")
print("CRUD SYSTEM PERFORMANCE SUMMARY")
print("====================================")
print("Total Operations:",total_operations)
print("Successful Operations:",successful_operations)
print("Client Errors (4xx):",client_errors)
print("Server Errors (5xx):",server_errors)
print("Total Errors:",total_errors)
print(f"Success Rate: {success_rate:.2f}%")
print(f"Error Rate: {error_rate:.2f}%")


# Time series data


daily_metrics = df.groupby(df['created_at'].dt.date).agg(
    total_operations=('id','count'),
    successful=('success','sum'),
    client_errors=('client_error','sum'),
    server_errors=('server_error','sum')
)

daily_metrics['total_errors'] = (daily_metrics['client_errors'] + daily_metrics['server_errors'])
daily_metrics['success_rate'] = (daily_metrics['successful']/daily_metrics['total_operations']) * 100
daily_metrics['error_rate'] = (daily_metrics['total_errors']/daily_metrics['total_operations']) * 100
print("\nDaily Time-Series Metrics")
display(daily_metrics)

# Success vs Error line chart


plt.figure(figsize=(12,5))
plt.plot(
    daily_metrics.index,
    daily_metrics['success_rate'],
    marker='o',
    label="Success Rate (%)"
)

plt.plot(
    daily_metrics.index,
    daily_metrics['error_rate'],
    marker='o',
    label="Error Rate (%)"
)

plt.title("CRUD Operation Success and Error Rate Trend")
plt.xlabel("Date")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# CRUD Count
crud_metrics = df.groupby('operation_type').agg(
    total_operations=('id','count'),
    successful_operations=('success','sum')
)

crud_metrics['success_rate'] = (crud_metrics['successful_operations']/crud_metrics['total_operations']) * 100
crud_metrics['error_rate'] = (100-crud_metrics['success_rate'])

print("\nCRUD Performance Breakdown")
display(crud_metrics)

# CRUD Success rate bar chart
plt.figure(figsize=(8,5))
plt.bar(crud_metrics.index,crud_metrics['success_rate'])
plt.title("CRUD Operation Success Rate")
plt.xlabel("Operation Type")
plt.ylabel("Success Rate (%)")
plt.ylim(0,100)
plt.grid(axis='y')
plt.show()

# HTTP response code distribution
http_distribution = df.groupby('status_code').size()
print("\nHTTP Response Code Distribution")
display(http_distribution)
plt.figure(figsize=(10,5))
plt.bar(http_distribution.index.astype(str),http_distribution.values)
plt.title("HTTP Response Code Frequency")
plt.xlabel("HTTP Status Code")
plt.ylabel("Frequency")
plt.show()

# Export
daily_metrics.to_csv("daily_performance_report.csv")
crud_metrics.to_csv("crud_performance_report.csv")
http_distribution.to_csv("http_response_distribution.csv")
print("\nReports successfully generated:")
print("- daily_performance_report.csv")
print("- crud_performance_report.csv")
print("- http_response_distribution.csv")