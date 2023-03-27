import pandas as pd
import yfinance as yf
from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from statsmodels.tools.eval_measures import rmse
import warnings

warnings.filterwarnings('ignore')

pd.options.display.float_format = '${:,.2f}'.format

today = datetime.today().strftime('%Y-%m-%d')
start_date = '2016-01-01'

eth_df = yf.download('ETH-USD', start_date, today)

eth_df.tail()

eth_df.info()

# print(eth_df.isnull().sum())

print(eth_df)

m = Prophet(
    seasonality_mode="multiplicative" 
)
m.fit(train)
future = m.make_future_dataframe(periods = 365)
print(future.tail())

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

print(test.tail())

next_day = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
print(forecast[forecast['ds'] == next_day]['yhat'].item())

eth_df.reset_index(inplace=True)
# eth_df.columns <-- used this to see the columns 

df = eth_df[["Date", "Open"]]
new_names = {
    "Date": "ds", 
    "Open": "y",
}
df.rename(columns=new_names, inplace=True)

print(df.tail())

train = df.iloc[:len(df)-365]
test = df.iloc[len(df)-365:]

# plot the open price
x = df["ds"]
y = df["y"]
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y))
# Set title
fig.update_layout(
    title_text="Time series plot of Ethereum Open Price",
)
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
        rangeslider=dict(visible=True),
        type="date",
    )
)
fig.show(renderer="notebook")



plot_plotly(m, forecast)
plot_components_plotly(m, forecast)

predictions = forecast.iloc[-365]['yhat']
print("Root mean squared error between actual and predicted values: ", rmse(predictions, test['y']))
print("Mean value of test dataset: ", test['y'].mean())