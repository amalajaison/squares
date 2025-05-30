# Draw map of single coils
# Derek Fujimoto
# April 2025

import pandas as pd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

filename = 'allcoils_Apr14.csv'
os.makedirs('figures', exist_ok=True)

# assumes gain 1000x and Mag13S-100 fluxgate

# read file
df = pd.read_csv(filename, comment='#')

coils = df.coil.unique()
df.set_index('coil', inplace=True)
plt.figure()

for coil in tqdm(coils):
    df_coil = df.loc[coil, :]

    # to nT
    for i in 'xyz':
        df_coil[f'B{i} (V)'] *= 10
        df_coil[f'dB{i} (V)'] *= 10
        df_coil[f'dB{i} (V)'] = df_coil[f'dB{i} (V)']**2
        df_coil[f'B{i} (V)'] *= df_coil.state

    # average positions
    df_coil = df_coil.groupby('position').mean()

    # draw
    for i in 'xyz':
        df_coil[f'dB{i} (V)'] = df_coil[f'dB{i} (V)']**0.5
        plt.errorbar(df_coil.index, df_coil[f'B{i} (V)'], df_coil[f'dB{i} (V)'], fmt='.', label=f'$B_{i}$')

    # plot elements
    plt.title(f'Coil {coil}')
    plt.xlabel('Position (cm)')
    plt.ylabel('Field (nT)')
    plt.grid(which='both', visible=True)
    plt.legend()
    plt.savefig(f'figures/coil{coil}.png')
    plt.gca().clear()
plt.close('all')
