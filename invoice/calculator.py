import pandas as pd

url = "Google Sheets Link Here"
df = pd.read_csv(url)

df = df[['Date', 'Start Time', 'End Time', 'Session Taken By']]
df['Date'] = pd.to_datetime(df['Date'])

df = df.dropna()

hourly_rate = input("Enter the hourly rate: ")

month = input("Enter the month in numeric format, (11 for November, etc): ")
print(month)

df_hashim = df[df['Session Taken By'] == 'Hashim']
df_huzaifa = df[df['Session Taken By'] == 'Huzaifa']

df_hashim['Start Time'] = df_hashim['Start Time'].astype(str)
df_hashim['End Time'] = df_hashim['End Time'].astype(str)

df_hashim['Start Time'] = df_hashim['Date'].dt.strftime('%d-%m-%Y') + ' ' + df_hashim['Start Time']
df_hashim['End Time'] = df_hashim['Date'].dt.strftime('%d-%m-%Y') + ' ' + df_hashim['End Time']
df_hashim['Start Time'] = pd.to_datetime(df_hashim['Start Time'])
df_hashim['End Time'] = pd.to_datetime(df_hashim['End Time'])

df_huzaifa['Start Time'] = df_huzaifa['Date'].dt.strftime('%d-%m-%Y') + ' ' + df_huzaifa['Start Time']
df_huzaifa['End Time'] = df_huzaifa['Date'].dt.strftime('%d-%m-%Y') + ' ' + df_huzaifa['End Time']
df_huzaifa['Start Time'] = pd.to_datetime(df_huzaifa['Start Time'])
df_huzaifa['End Time'] = pd.to_datetime(df_huzaifa['End Time'])

df_hashim = df_hashim[(df_hashim['Date'].dt.month == int(month))]
df_hashim['Hours'] = (df_hashim['End Time'] - df_hashim['Start Time']).dt.total_seconds() / 3600
df_hashim['Hours'] = df_hashim['Hours'].round(2)

total_hours_hashim = df_hashim['Hours'].sum()
print(f"Total hours worked by Hashim in month of {month} is {total_hours_hashim}")

df_huzaifa = df_huzaifa[(df_huzaifa['Date'].dt.month == int(month))]
df_huzaifa['Hours'] = (df_huzaifa['End Time'] - df_huzaifa['Start Time']).dt.total_seconds() / 3600
df_huzaifa['Hours'] = df_huzaifa['Hours'].round(2)

total_hours_huzaifa = df_huzaifa['Hours'].sum()
print(f"Total hours worked by Huzaifa in month of {month} is {total_hours_huzaifa}")

invoice_hashim = total_hours_hashim * hourly_rate
invoice_huzaifa = total_hours_huzaifa * hourly_rate
print(f"Total invoice for Hashim in month of {month} is PKR {invoice_hashim}")
print(f"Total invoice for Huzaifa in month of {month} is PKR {invoice_huzaifa}")

total_amount = invoice_hashim + invoice_huzaifa
print(f"Total amount payable for month of {month} is PKR {total_amount} ")
