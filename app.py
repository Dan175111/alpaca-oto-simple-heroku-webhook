from flask import Flask, request
import alpaca_trade_api as tradeapi
import config, json, requests

app = Flask(__name__)

api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url='https://paper-api.alpaca.markets')


@app.route('/webhook', methods=['POST'])
def webhook():
    webhook_message = json.loads(request.data)

    if webhook_message['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            'code': 'error',
            'message': 'nice try buddy'
        }
    
    symbol = webhook_message['ticker']
    price = webhook_message['price']   
    qty = webhook_message['quantity']
                             
    order = api.submit_order(symbol, qty, 'buy', 'limit', 'gtc', limit_price=price, order_class="oto", take_profit={'limit_price': price * webhook_message['profit']})
      

    return webhook_message
