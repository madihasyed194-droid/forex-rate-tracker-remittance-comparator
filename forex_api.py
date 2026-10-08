import requests
from datetime import date


def get_exchange_rates():

    url = "https://api.frankfurter.app/latest"

    params = {
        "from": "USD",
        "to": "INR,EUR"
    }

    response = requests.get(
        url,
        params=params
    )

    if response.status_code != 200:
        return None

    data = response.json()

    usd_inr = data["rates"]["INR"]

    usd_eur = data["rates"]["EUR"]

    # Calculate EUR/INR
    eur_inr = usd_inr / usd_eur

    return {
        "USD/INR": usd_inr,
        "EUR/INR": eur_inr,
        "date": date.today().isoformat()
    }


if __name__ == "__main__":

    rates = get_exchange_rates()

    print(rates)