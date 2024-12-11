import numpy as np
import pandas as pd

# Import the information of Maduo earthquake fissure
df_Maduo = pd.read_csv('Maduo earthquake fissure information.csv')
# Import the information of earthquakes
df_earthquake = pd.read_csv('Earthquake information.csv')

# Calculate the length of earthquake fissure
slM = df_Maduo['Fissure length (max)'].sum() / df_Maduo.shape[0]  # Length of single Maduo earthquake fissure (m)
lM = slM * df_Maduo['Number of earthquake fissures'].sum()  # Total length of Maduo earthquake fissure (m)
lrM = 170  # Length of Maduo earthquake rupture (km)
df_earthquake['Rupture length'] = df_earthquake.apply(
    lambda row: row['Rupture length'] if pd.notna(row['Rupture length']) else np.power(10, (row['Magnitude'] - 5.92) / 0.88),  # Length of earthquake rupture (km)
    axis=1)
df_earthquake['Fissure length'] = df_earthquake['Rupture length'] / lrM * lM  # Length of earthquake fissure (m)

# Calculate the average width of earthquake fissure
df_earthquake['Fissure width'] = np.power(10, (df_earthquake['Magnitude'] - 6.81) / 0.78)  # Width of earthquake fissure (m)

# Set the average depth of earthquake fissure
df_earthquake['Fissure depth'] = 3  # Considering that soil organic matter is distributed in the 0~3m soil layer

# Set the recovery rate of earthquake fissure
rrl = -0.49  # Recovery rate of earthquake fissure length (m/year)
rrw = 0.05  # Recovery rate of earthquake fissure width (m/year)

# Calculate the average area of earthquake fissure
df_earthquake['Time interval'] = 2022 - df_earthquake['Year']  # Time interval (year)
df_earthquake['Sidewall area'] = 0
df_earthquake['Bottom area'] = 0
for i in range(df_earthquake.shape[0]):
    length = df_earthquake['Fissure length'][i]
    width = df_earthquake['Fissure width'][i]
    depth = df_earthquake['Fissure depth'][i]
    if df_earthquake['Time interval'][i] == 0:
        df_earthquake.loc[i, 'Sidewall area'] = length * depth  # Area of earthquake fissure sidewall (m^2)
        df_earthquake.loc[i, 'Bottom area'] = length * width  # Area of earthquake fissure bottom (m^2
    else:
        sidewall_area = 0
        bottom_area = 0
        for t in range(df_earthquake['Time interval'][i]):
            length += rrl
            width += rrw
            sidewall_area += length * depth
            bottom_area += length * width
        df_earthquake.loc[i, 'Sidewall area'] = sidewall_area / df_earthquake['Time interval'][i]  # Average area of earthquake fissure sidewall (m^2)
        df_earthquake.loc[i, 'Bottom area'] = bottom_area / df_earthquake['Time interval'][i]  # Average area of earthquake fissure bottom (m^2)
df_earthquake['Area'] = df_earthquake['Sidewall area'] * 2 + df_earthquake['Bottom area']  # Average area of earthquake fissure (m^2)

# Calculate the total area of earthquake fissure
total_sidewall_area = df_earthquake['Sidewall area'].sum() * 2  # Total area of earthquake fissure sidewall (m^2)
total_bottom_area = df_earthquake['Bottom area'].sum()  # Total area of earthquake fissure bottom (m^2)
total_area = df_earthquake['Area'].sum()  # Total area of earthquake fissure (m^2)

# Calculate the carbon emission of earthquake fissure
ers = 968.53  # Carbon emission of earthquake fissure sidewall (g CO2 m^-2·a^-1)
erb = 514.79  # Carbon emission of earthquake fissure bottom (g CO2 m^-2·a^-1)
qtp_area = 2.57e12  # Area of Qinghai-Tibet Plateau (m^2)
total_carbon_emission_sidewall = total_sidewall_area * ers  # Total carbon emission of earthquake fissure sidewall (g CO2 a^-1)
total_carbon_emission_bottom = total_bottom_area * erb  # Total carbon emission of earthquake fissure bottom (g CO2 a^-1)
total_carbon_emission = total_carbon_emission_sidewall + total_carbon_emission_bottom  # Total carbon emission of earthquake fissure (g CO2 a^-1)
total_carbon_emission_per_area = total_carbon_emission / qtp_area  # Carbon emission of earthquake fissure per unit area of Qinghai-Tibet Plateau (g CO2 m^-2·a^-1)

# Output the results
print('The total area of earthquake fissure sidewall is', total_sidewall_area, 'm^2.')
print('The total area of earthquake fissure bottom is', total_bottom_area, 'm^2.')
print('The total area of earthquake fissure is', total_area, 'm^2.')
print('The total carbon emission of earthquake fissure sidewall is', total_carbon_emission_sidewall, 'g CO2 a^-1.')
print('The total carbon emission of earthquake fissure bottom is', total_carbon_emission_bottom, 'g CO2 a^-1.')
print('The total carbon emission of earthquake fissure is', total_carbon_emission, 'g CO2 a^-1.')
print('The carbon emission of earthquake fissure per unit area of Qinghai-Tibet Plateau is', total_carbon_emission_per_area, 'g CO2 m^-2·a^-1.')