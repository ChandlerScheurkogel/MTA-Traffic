import pandas as pd

# Load the provided CSV file
file_path = 'MTATotalData.csv'
df = pd.read_csv(file_path)

# Rename columns to make life easier
df.rename(columns={
    'Plaza ID': 'Plaza',
    'Hour': 'Hour',
    'Date': 'Date',
    '# Vehicles - E-ZPass': 'E_ZPass',
    '# Vehicles - VToll': 'VToll'
}, inplace=True)

# Create a new column "TotalCars" by summing E-ZPass and VToll columns as I don't think we care about that breakout 
df['TotalCars'] = df['E_ZPass'] + df['VToll']

# Convert the Date column to datetime format instead of the stupid thing they use
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Filter data from 12/1/2017 to the latest available date in the dataset
start_date = pd.to_datetime('2017-12-01')
end_date = df['Date'].max()
filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Used to show what plaza # is in English
plaza_name_mapping = {
    21: 'RFK Bridge Bronx Plaza and Queens Plaza',
    22: 'RFK Bridge Manhattan Plaza',
    23: 'Bronx-Whitestone Bridge',
    24: 'Henry Hudson Bridge',
    25: 'Marine Parkway-Gil Hodges Memorial Bridge',
    26: 'Cross Bay Veterans Memorial Bridge',
    27: 'Queens Midtown Tunnel',
    28: 'Hugh L. Carey Tunnel',
    29: 'Throgs Neck Bridge',
    30: 'Verrazano-Narrows Bridge'
}

# Add the PlazaName column based on the Plaza column
filtered_df['PlazaName'] = filtered_df['Plaza'].map(plaza_name_mapping)

# Reorder columns to place PlazaName between Plaza and Date
filtered_df = filtered_df[['Plaza', 'PlazaName', 'Date', 'Hour', 'TotalCars']]

# Group by Plaza, PlazaName, and Date, then sum TotalCars for each day within the specified period
daily_summary_with_latest_df = (
    filtered_df.groupby(['Plaza', 'PlazaName', 'Date'])
    .agg({'TotalCars': 'sum'})
    .reset_index()
)

# Save the daily summary with PlazaName to a new CSV file
daily_output_path_with_latest = 'MTATotalData_DailySummary_WithLatestDate.csv'
daily_summary_with_latest_df.to_csv(daily_output_path_with_latest, index=False)

print(f"Daily summary with PlazaName saved to {daily_output_path_with_latest}")
