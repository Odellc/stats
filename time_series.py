import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
try:
	from statsmodels.diagnostic import acorr_ljungbox
except Exception:
	from statsmodels.stats.diagnostic import acorr_ljungbox

random_white_noise = np.random.normal(loc=0, scale=1, size=1000)

fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].plot(random_white_noise)
ax[0].axhline(0, color='red', linestyle='--')
ax[0].set_title('Random White Noise Time Series')
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
ax[1].stem(range(len(cross_corr)), cross_corr, basefmt=" ")
ax[1].set_title('Cross-Correlation: Real Investment vs Real DPI')
ax[1].axhline(0, color='red', linestyle='--')
ax[1].set_xlabel('Lag')
ax[1].set_ylabel('Cross-Correlation')

plt.tight_layout()
plt.show()


# ----------------------
# Multivariate ARIMAX example
# ----------------------

# We'll use 'realinv' as the endogenous series and 'realdpi' as an exogenous predictor.
data = df_mod.copy().dropna()

# Optionally create a lagged exogenous variable if you want to test predictive power
data['realdpi_lag1'] = data['realdpi'].shift(1)
data = data.dropna()

# Endog and exog
endog = data['realinv']
exog = data[['realdpi', 'realdpi_lag1']]

# Train/test split (last 20% for testing)
split_idx = int(len(data) * 0.8)
endog_train, endog_test = endog.iloc[:split_idx], endog.iloc[split_idx:]
exog_train, exog_test = exog.iloc[:split_idx], exog.iloc[split_idx:]

# Fit a SARIMAX model (ARIMAX) with a basic order — you can grid-search p,d,q for better fit
model = sm.tsa.SARIMAX(endog_train, exog=exog_train, order=(1,0,1), enforce_stationarity=False, enforce_invertibility=False)
res = model.fit(disp=False)

print('\nARIMAX model summary:')
print(res.summary())

# Forecast on test set using exogenous values for the horizon
n_forecast = len(endog_test)
forecast_res = res.get_forecast(steps=n_forecast, exog=exog_test)
pred_mean = forecast_res.predicted_mean
conf_int = forecast_res.conf_int()

# Performance metrics
def rmse(a, b):
	return np.sqrt(np.mean((a - b) ** 2))

def mae(a, b):
	return np.mean(np.abs(a - b))

def mape(a, b):
	return np.mean(np.abs((a - b) / a)) * 100

metrics = {
	'RMSE': rmse(endog_test.values, pred_mean.values),
	'MAE': mae(endog_test.values, pred_mean.values),
	'MAPE(%)': mape(endog_test.values, pred_mean.values),
	'AIC': res.aic,
	'BIC': res.bic
}

print('\nModel performance on test set:')
for k, v in metrics.items():
	print(f"{k}: {v:.4f}")

# Plot actual vs forecast with confidence intervals
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(endog, label='Observed', color='black')
ax.plot(pred_mean.index, pred_mean, label='Forecast', color='tab:orange')
ax.fill_between(conf_int.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='tab:orange', alpha=0.2)
ax.axvline(endog_test.index[0], color='red', linestyle='--', label='Forecast start')
ax.set_title('ARIMAX Forecast vs Observed')
ax.legend()
plt.show()

# Residual diagnostics
resid = res.resid

fig, ax = plt.subplots(1, 3, figsize=(15, 4))
ax[0].plot(resid)
ax[0].set_title('Residuals')
plot_acf(resid, ax=ax[1], lags=40)
ax[1].set_title('ACF of Residuals')
plot_pacf(resid, ax=ax[2], lags=40)
ax[2].set_title('PACF of Residuals')
plt.tight_layout()
plt.show()

# Ljung-Box test for residual autocorrelation
lb_test = acorr_ljungbox(resid, lags=[10, 20], return_df=True)
print('\nLjung-Box test results (residuals):')
print(lb_test)

# If you want to iterate on model orders, try a simple grid search for p,d,q
def simple_grid_search(endog, exog, p_values=(0,1,2), d_values=(0,1), q_values=(0,1,2)):
	best_aic = np.inf
	best_order = None
	best_res = None
	for p in p_values:
		for d in d_values:
			for q in q_values:
				try:
					m = sm.tsa.SARIMAX(endog, exog=exog, order=(p,d,q), enforce_stationarity=False, enforce_invertibility=False)
					r = m.fit(disp=False)
					if r.aic < best_aic:
						best_aic = r.aic
						best_order = (p,d,q)
						best_res = r
				except Exception:
					continue
	return best_order, best_aic, best_res

# Run a small grid search on training data to find a better (p,d,q)
best_order, best_aic, best_r = simple_grid_search(endog_train, exog_train, p_values=(0,1,2), d_values=(0,1), q_values=(0,1,2))
print('\nGrid-search result:')
print('Best order by AIC:', best_order, 'AIC:', best_aic)

if best_r is not None:
	# Forecast using the tuned model
	tuned_forecast = best_r.get_forecast(steps=n_forecast, exog=exog_test)
	tuned_pred = tuned_forecast.predicted_mean
	tuned_ci = tuned_forecast.conf_int()

	tuned_metrics = {
		'RMSE': rmse(endog_test.values, tuned_pred.values),
		'MAE': mae(endog_test.values, tuned_pred.values),
		'MAPE(%)': mape(endog_test.values, tuned_pred.values),
		'AIC': best_r.aic,
		'BIC': best_r.bic
	}

	print('\nTuned model performance on test set:')
	for k, v in tuned_metrics.items():
		print(f"{k}: {v:.4f}")

	# Plot tuned forecast vs observed
	fig, ax = plt.subplots(figsize=(12, 6))
	ax.plot(endog, label='Observed', color='black')
	ax.plot(tuned_pred.index, tuned_pred, label=f'Tuned Forecast {best_order}', color='tab:green')
	ax.fill_between(tuned_ci.index, tuned_ci.iloc[:, 0], tuned_ci.iloc[:, 1], color='tab:green', alpha=0.2)
	ax.axvline(endog_test.index[0], color='red', linestyle='--', label='Forecast start')
	ax.set_title('Tuned ARIMAX Forecast vs Observed')
	ax.legend()
	plt.show()
