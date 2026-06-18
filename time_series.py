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

# Continue from where your code ends
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Plot the 'realinv' time series
ax[0].plot(df_mod['realinv'])
ax[0].set_title('Real Investment Time Series')
ax[0].axhline(0, color='red', linestyle='--')

# Plot the ACF for 'realinv' with lag=50 and alpha=0.03
plot_acf(df_mod['realinv'], ax=ax[1], lags=50, alpha=0.03)
ax[1].set_title('Autocorrelation Function (ACF)')

plt.tight_layout()
plt.show() 


# Cross-correlation evaluation between 'realinv' and 'realdpi'
cross_corr = sm.tsa.stattools.ccf(df_mod['realinv'], df_mod['realdpi'])

# Plot the cross-correlation
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Plot the ACF for 'realinv'
plot_acf(df_mod['realinv'], ax=ax[0], lags=50, alpha=0.05)
ax[0].set_title('ACF of Real Investment')

# Plot the cross-correlation
ax[1].stem(range(len(cross_corr)), cross_corr, basefmt=" ", use_line_collection=True)
ax[1].set_title('Cross-Correlation: Real Investment vs Real DPI')
ax[1].axhline(0, color='red', linestyle='--')
ax[1].set_xlabel('Lag')
ax[1].set_ylabel('Cross-Correlation')

plt.tight_layout()
plt.show()