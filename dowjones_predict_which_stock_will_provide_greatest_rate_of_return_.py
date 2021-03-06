
""" The Dow Jones Index Data Set

      Dow Jones Index Data Set


Predict which stock will provide greatest rate of return

## Background into the data set

First we'll start by importing all the necessary libraries.
"""

# Importing libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

"""Now we can read in the data set. We will have to remove the dollar sign from the data set as the dollar sign causes pandas to interpret these as strings. """

# Reading in the data set

from google.colab import files
uploaded = files.upload()

import io
df = pd.read_csv(io.BytesIO(uploaded['dow_jones_index.data']))
# Dataset is now stored in a Pandas Dataframe

# Showing the first 5 rows
df.head(5)

# Showing how many rows and columns are in the dataset
rows, columns = df.shape

print(f"There are {rows} rows and {columns} columns")

# Setting the max number of rows and columns that are displayed
pd.options.display.max_rows = rows # Set max rows to number of rows in df (from https://pandas.pydata.org/pandas-docs/stable/options.html)
pd.options.display.max_columns = columns # Set max columns to number of columns in df (from https://pandas.pydata.org/pandas-docs/stable/options.html)

# Converting the date column into datetime format
df["date"] = pd.to_datetime(df["date"])

df.head()

# Removing dollar sign
dfStrip = df.loc[:,['open', 'high', 'low', 'close', 'next_weeks_open', 'next_weeks_close']].apply(lambda x : x.str.strip('$'))

# Checking first 5 rows
dfStrip.head(5)

# Replacing the values with the dollar sign with the stripped versions
df.loc[:,['open', 'high', 'low', 'close', 'next_weeks_open', 'next_weeks_close']] = dfStrip.astype(float)

# Viewing dataset
df

df.loc[:, ['stock','close']].groupby(by='stock').describe()

sns.set(rc={'figure.figsize':(15, 10)})

lineplot = sns.lineplot(data=df, x='date', y='close', hue='stock')

lineplot.set_xticklabels(df['date'],rotation=45)

plt.show()

AAQuotes = df.loc[df["stock"] == "AA", ["date", "open", "high", "low", "close"]]

!pip install https://github.com/matplotlib/mpl_finance/archive/master.zip

!pip install --upgrade mplfinance

from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates


AAQuotes["date"] = mdates.date2num(AAQuotes["date"].values)

fig, ax = plt.subplots()
candlestick_ohlc(ax, 
                 quotes = AAQuotes.values, 
                 width=3,
                 colorup='g',
                 colordown='r',
                 alpha=1)

plt.show()

"""## Making Predictions

Every Dow Jones Index stock lost money in the week ending 5/27/2011. We will attempt to predict this fall.

### Predicting values for AA
"""

from statsmodels.tsa.api import VAR

# Creating the model
model = VAR(AAQuotes[["open", "high", "low", "close"]].iloc[:14])

# Fitting the model
model_fit = model.fit()

# Predicting one step ahead
prediction = model_fit.forecast(model_fit.y, steps=1)
print(prediction)

# Viewing the true values
AAQuotes[["open", "high", "low", "close"]].iloc[15]

# Variation from the true values
AAQuotes[["open", "high", "low", "close"]].iloc[15].values - np.array(prediction)

"""### Predicting opening values for all stocks for the week of 05/27/2011"""

pivotedDF = df[["date", "stock", "open", "high", "low", "close"]].pivot(index='date', values=["open", "high", "low", "close"], columns='stock')

pivotedDF

model = VAR(pivotedDF.loc[:'5/20/2011'].values)

# Fitting the model
model_fit = model.fit()

# Predicting one step ahead (in this case, the week of 05/27/2020)
prediction = model_fit.forecast(model_fit.y, steps=1)
print(prediction)

# Viewing the true values
pivotedDF.loc['5/27/2011']

# Variation from the true values
prediction - pivotedDF.loc['5/27/2011'].values

"""### How much do the predicted open values vary from the true values?"""

(prediction[0][:30] - pivotedDF.loc['5/27/2011', 'open'].values)

# Predicted move down
(np.array(prediction)[0][:30] - pivotedDF.loc['5/20/2011', 'close'].values)

# Actual move down
(pivotedDF.loc['5/27/2011', 'open'].values - pivotedDF.loc['5/20/2011', 'close'].values)

"""As we can see from the above, the model doesn't accurately predict that the opening value on week 05/27/2011 is down on each stock from the closing week previously. Improvements could be made with better feature selection or a different model. A grid search algorithm or a genetic algorithm could be used to select the features and/or hyperparameters. A RNN model may work better than a VAR."""

