import ccxt

def try_login(exchange,apikey,apisecret):
    exchange_id = exchange
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'apiKey': apikey,
        'secret': apisecret,
        'nonce': ccxt.Exchange.milliseconds
    })
    print(apikey)
    print(apisecret)
    ans = exchange.fetchBalance()
    print(ans)
    return 200,'success'