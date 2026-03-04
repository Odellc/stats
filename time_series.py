import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.diagnostic import acorr_ljungbox

random_white_noise = np.random.normal(loc=0, scale=1, size=1000)

fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].plot(random_white_noise)
ax[0].axhline(0, color='red', linestyle='--')
ax[0].set_title('Random White Noise Time Series', ax=ax[1])
plot_acf(random_white_noise, ax=ax[1])

acorr_ljungbox(random_white_noise, lags =[50], return_df=True)

df = sm.datasets.macrodata.load().data

df['realinv'] = round(df['realinv'].astype('float32'), 2)
df['realdpi'] = round(df['realdpi'].astype('float32'), 2)

df_mod = df[['realinv', 'realdpi']].copy()

