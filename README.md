<img width="892" alt="Screenshot 2023-11-14 at 10 13 34 PM" src="https://github.com/cpf006/stock-visualizer/assets/5445886/05f4685c-92df-466c-95bf-edb7235fb766">

<img width="892" alt="Screenshot 2023-11-14 at 10 18 30 PM" src="https://github.com/cpf006/stock-visualizer/assets/5445886/7cd8badd-4dc0-4a45-bfb6-1a4704fe569c">


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

# Running tests
```
pytest
```

# Access URL
```
http://localhost:8000/
```

### Stopping the App
CTRL+C
