# Stock Visualizer
Example of a stock data visualization app built using Dash

# Running the app with docker-compose
```
docker-compose up --build
```

# Running the app manually
### Install Dependencies
```
pip install -r requirements.txt
```
### Run servers
Make sure the quotes_publisher server is running (in a seperate terminal)
```
python quotes_publisher.py 
```
Run the Dash app
```
python app.py
```

### Access URL
```
http://localhost:8000/
```

### Stopping the App
CTRL+C