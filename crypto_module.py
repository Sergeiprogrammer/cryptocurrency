import requests

class Crypto:
    def fetch_crypto_prices(self,number):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        api_key = "your api key"
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": api_key,
        }
        if number:
            parameters = {
                "start": "1",
                "limit": number,  # Number of cryptocurrencies to fetch (adjust as needed)
                "convert": "USD"
            }

        response = requests.get(url, headers=headers, params=parameters)

        if response.status_code!= 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        data = response.json()

        # Collect the fetched data
        crypto_prices = []
        for crypto in data['data']:
            name = crypto['name']
            symbol = crypto['symbol']
            price = crypto['quote']['USD']['price']
            enter = " "
            crypto_prices.append(f"{name} {enter} ({symbol}): {enter} ${price:.2f}")

        return crypto_prices

    def fetch_specific_crypto_prices(self, target):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        api_key = "da4025ce-dad9-4122-8df1-6c9bf4fa4183"
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": api_key,
        }
        parameters = {"symbol": target, "convert": "USD"}
        response = requests.get(url, headers=headers, params=parameters)

        if response.status_code != 200:
            return response.json()

        data = response.json()
        prices = {}
        price = data['data'][target]['quote']['USD']['price']
        prices[target] = price
        return prices