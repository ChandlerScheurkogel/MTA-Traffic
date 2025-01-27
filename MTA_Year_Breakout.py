import pandas as pd

# Load the data from the provided CSV file
file_path = 'MTATotalData_DailySummary_WithLatestDate.csv'
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime for easier filtering
df['Date'] = pd.to_datetime(df['Date'])

# Extract year and month-day for filtering
df['Year'] = df['Date'].dt.year
df['MonthDay'] = df['Date'].dt.strftime('%m-%d')

# Filter data for the period Jan 1 to Jan 18 
filtered_df = df[df['MonthDay'].between('01-01', '01-18')]

# Group by PlazaName and Year, then calculate the average TotalCars
result = filtered_df.groupby(['PlazaName', 'Year'])['TotalCars'].mean().reset_index()

# Save the output to a new CSV file
output_file = 'Average_TotalCars_Jan1_Jan18.csv'
result.to_csv(output_file, index=False)

print(f"Processing complete. The results have been saved to {output_file}.")