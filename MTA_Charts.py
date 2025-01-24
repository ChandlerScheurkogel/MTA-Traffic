import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the provided CSV file
file_path = 'MTATotalData_DailySummary_WithLatestDate.csv'
df = pd.read_csv(file_path)

# Convert the Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Used to show what plaza # is in English
plaza_name_mapping = {
    21: 'Catskill',
    22: 'Selkirk',
    23: 'Albany (I-787)',
    24: 'Albany (I-87)',
    25: 'Schenectady (I-890)',
    26: 'Schenectady (I-890 & Rt 5s)',
    27: 'Amsterdam',
    28: 'Fulltonville',
    29: 'Canajoharie',
    30: 'Herkimer'
}

# Plot line charts for each plaza with two best fit lines
plt.figure(figsize=(15, 20))

for i, plaza in enumerate(plaza_name_mapping.values(), 1):
    plaza_data = df[df['PlazaName'] == plaza]
    
    # Prepare data for overall best fit line
    x_all = (plaza_data['Date'] - plaza_data['Date'].min()).dt.days.values
    y_all = plaza_data['TotalCars'].values
    slope_all, intercept_all = np.polyfit(x_all, y_all, 1)
    best_fit_all = slope_all * x_all + intercept_all

    # Prepare data for best fit line from January 5th onward
    jan_5_date = pd.to_datetime('2025-01-05')
    recent_data = plaza_data[plaza_data['Date'] >= jan_5_date]
    x_recent = (recent_data['Date'] - plaza_data['Date'].min()).dt.days.values
    y_recent = recent_data['TotalCars'].values
    if len(x_recent) > 1:
        slope_recent, intercept_recent = np.polyfit(x_recent, y_recent, 1)
        best_fit_recent = slope_recent * x_recent + intercept_recent

    # Plot the data and both lines
    plt.subplot(5, 2, i)
    plt.plot(plaza_data['Date'], plaza_data['TotalCars'], marker='o', linestyle='-', label='TotalCars')
    plt.plot(plaza_data['Date'], best_fit_all, color='red', linestyle='--', label='Overall Best Fit')
    if len(x_recent) > 1:
        plt.plot(recent_data['Date'], best_fit_recent, color='blue', linestyle='--', label='Best Fit (Jan 5 Onward)')
    plt.title(plaza)
    plt.xlabel('Date')
    plt.ylabel('Total Cars')
    plt.xticks(rotation=45)
    plt.legend()

plt.tight_layout()

# Save the updated plot with best fit lines in the same folder
output_image_path = os.path.join(os.getcwd(), 'MTATotalData_Analysis.png')
plt.savefig(output_image_path, dpi=300)
plt.close()

print(f"Analysis chart saved as {output_image_path}")
