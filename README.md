# TradingBot

## Description
This application is designed to automate the buying and selling of stocks using a machine learning model.
The intent of the TradingBot will be find the most efficient strategies of trading by improving the model over time.
The model will be trained with a dataset that is derived from multiple sources and the overall fit will determine if the model is improving
or not.

It should be noted that while the goal for the TradingBot will be to create a viable solution for real capital investment,
it will be limited to medium and long term trading strategy. For example, due to resource limitations 
this app will not be used to intraday trades as it requires much higher throughput.

## Basic Design

### Ingestion Pipeline
The ingestion pipeline will be comprised of several components that will pull data from APIs and other sources (tbd)
with the overall goal of combining the data into a single aggregate dataset.

To start I will be pulling basic trading data from the Alpaca API as this will be part of the core dataset
moving forward. Eventually, I want to be able to add more and more data to this pipeline and track to see which
data points are the most impactful to the model.

Once the data is aggregated, it will be stored in a database so that we can use it in our model.

### Storage API
The storage API will act as the intermediary between the machine learning model and the underlying data.
The ML model will call this API routinely as more data is stored in the database and use it to update itself.
This should be relatively simple consisting of a single endpoint for pulling in the data by passing a few paramaters.

### ML Data Poller
This component will actually pull the data from the storage API and push it through to the ML Processor.
It should only pull in the data that is required to update the model so it will need to store state information
as to ensure that the model does not become polluted.

## ML Model Processor
The ML Model Processor will be responsible for building the ML model using the data that was provided by the poller.
This app should be highly configurable so we can easily make changes to as needed. It should also have a backfeed functionality
whereby we can re-ingest data as needed. Performance considerations are important here as we want the model to be able
to respond quick enough to market events.

## Trading System
The trading system will be the mechanism by which the trades will be executed. Using the model output, it will continuously
evaluate a subset of tickers for trading opportunities. To start, I want to use a list of 20 tickers that the system will
be configured to evaluate. As the model improves, I may consider expanding this list.



# Planned Design

## Ingestion Pipeline (container-tb-extractor) (in progress)
The ingestion pipeline will pull in bars which is aggregated stock data over a certain period of time. For large scale systems, it would make sense to use individual trades and quotes to get a more accurate model but for this project we will target aggregations of that data over the course of 1 hour.

The pipeline will have 2 services attached to it.
### HistoricalCollectionService
The HCS will allow us to pull historical data such as bars from the Alpaca API. Since we want to build the most accurate model possible it will be configured to pull data from any ticker and any timeframe.

### LiveStreamCollectionService
The LSCS will be responsible for ingesting live data into the pipeline so that it can be stored and used during the next model build. For example, using a subscription to the Alpaca API, we are able to stream bars into the database as they become available.



## ML Modeler (container-tb-modeler)
The modeler is an application that trains and test the GRU and LSTM models so that they can be used to predict
future stock prices based on its exponential moving average (EMA).

### Training
The model needs to be trained periodically so that the it learns from the existing dataset collected in the extractor.
As the extractor pulls data into the database, the modeler will load the new data into a training dataset, load the model,
and train the model using an optimizer. While this is happening, the modeler will collect statistics on model performance to
ensure that the loss is minimized. After training, the modeler will save the performance metrics back to the database for future
reference.

### Testing






___

## Training Data
The training data will consist of data consistent with the hourly extraction.
Besides the stock bars, data that is generally collected multiple times a day will be accepted.
For example, # of mentions on twitter for specific ticker could be paired.

## Testing Data
The testing data will include all variables included in the training set as well as target variable. 

For this project we want to evaluate medium (~3-6 months) and long term (1+ years) trading opportunities. Typically, I've seen higher returns implementing a medium-term strategy so we will start with a target variable equal to the avg price within 3 to 6 months after the current price. To extrapolate a number the model will can understand, we will calculate the avg ROI over the course of the timeframe and feed that into model.



## Variables
| Variable    | Type      | Description                                                           |
|-------------|-----------|-----------------------------------------------------------------------|
| bar_ts      | timestamp | The timestamp for when the window of stock quotes was aggregated      |
| symbol      | string    | The ticker symbol                                                     |
| open_price  | float     | The price at the beginning of the aggregation window (every 1 minute) |
| high_price  | float     | The price ceiling within the window                                   |
| low_price   | float     | The price floor within the window                                     |
| close_price | float     | The price at the end of the aggregation window                        |
| volume      | integer   | The total volume over the window                                      |

### Potential New Variables
- twitter_sentiment - an general indicator of either positive or negative sentiment from Twitter API
- news_sentiment - a general indicator of sentiment from Alpaca News API
- eps_estimate - earnings estimate
- eps_actual - earnings actual
- number_of_employees - the number of employees
- ebitda_yield
- pe_ratio

