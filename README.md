# Asset Sentiment + TA indicator

A Streamlit application that combines **sentiment analysis of financial news** with **technical analysis** (TA) indicators to provide a richer picture of an asset's sentiment and potential market movement.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Python 3.8+  
- `pip` or `poetry` / `venv`  
- Internet connection (to fetch news and price data)

### Installing

A step by step series of examples that tell you how to get a development env running

1. Clone the repository:  
   ```bash
   git clone https://github.com/oliverAnderson18/asset-sentiment-indicator.git  
   cd asset-sentiment-indicator

2. Create the virtual enviroment and install dependencies: 

   ```bash
   python -m venv .venv  
   source .venv/bin/activate  # Linux / Mac  
   .venv\Scripts\activate     # Windows  
   pip install -r requirements.txt

## Deployment

Deploy on streamlit

Go to the [streamlit app](https://asset-sentiment-indicator.streamlit.app/)

*Note: It may take a few minutes to deploy. This is due to heavy dependencies used.

## Built With

* Streamlit – For the interactive dashboard
* Pandas / NumPy – Data manipulation
* transformers / torch – Text processing and keyword extraction
* yfinance – Fetching price data
* TA-Lib / custom indicators – Technical analysis calculations
* PLotly – Plotting charts and sentiment visuals

## Authors

* Oliver Anderson Llorens

## Improvements that could be done

* Due to budget restrictions, the project works on a base of 100 news articles. If the budget was greater, more news articles could be fetch and therefore more accuracy could be obtained.

* Speed of deploiment could be reduced with a better optimization.
