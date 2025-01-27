import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the uploaded file
file_path = 'Average_TotalCars_Jan1_Jan18.csv'
df = pd.read_csv(file_path)

# Convert year to numeric for plotting
df['Year'] = pd.to_numeric(df['Year'])

# Get unique plaza names
plaza_names = df['PlazaName'].unique()

# Create a single figure for all ten plots
fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(20, 25))
axes = axes.flatten()

for i, plaza in enumerate(plaza_names):
    plaza_df = df[df['PlazaName'] == plaza]
    
    # Scatter plot of TotalCars over the years
    axes[i].scatter(plaza_df['Year'], plaza_df['TotalCars'], label='Total Cars', color='blue')

    # Fit a linear regression line
    coefficients = np.polyfit(plaza_df['Year'], plaza_df['TotalCars'], 1)
    poly_fit = np.poly1d(coefficients)
    axes[i].plot(plaza_df['Year'], poly_fit(plaza_df['Year']), color='red', label='Best Fit Line')

    # Plot details
    axes[i].set_title(f'Total Cars Over Time - {plaza}')
    axes[i].set_xlabel('Year')
    axes[i].set_ylabel('Total Cars')
    axes[i].grid(True)
    axes[i].legend()

# Adjust layout and save the figure
plt.tight_layout()
output_png_path = 'total_cars_plots_combined.png'
plt.savefig(output_png_path)
plt.close(fig)

output_png_path
