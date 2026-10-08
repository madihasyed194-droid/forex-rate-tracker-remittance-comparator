from flask import Flask, render_template, request

from calculator import compare_providers
from forex_api import get_exchange_rates

from database import (
    create_database,
    save_rate,
    get_rate_history
)

app = Flask(__name__)

create_database()


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    rates = get_exchange_rates()

    return render_template(
        "index.html",
        rates=rates
    )


# ==================================================
# COMPARE
# ==================================================

@app.route("/compare", methods=["GET", "POST"])
def compare():

    results = None
    amount = None
    base_rate = None
    best_provider = None
    message = None

    if request.method == "POST":

        try:

            amount = float(request.form["amount"])

            # Validate amount
            if amount <= 0:

                message = "Please enter an amount greater than zero."

            else:

                rates = get_exchange_rates()

                if rates:

                    base_rate = rates["USD/INR"]

                    results = compare_providers(
                        amount,
                        base_rate
                    )

                    # Find highest received amount
                    best_provider = max(
                        results,
                        key=lambda x: x["received_amount"]
                    )

                    # Save USD/INR
                    save_rate(
                        "USD/INR",
                        rates["USD/INR"],
                        rates["date"]
                    )

                    # Save EUR/INR
                    save_rate(
                        "EUR/INR",
                        rates["EUR/INR"],
                        rates["date"]
                    )

                else:

                    message = "Unable to fetch exchange rates."

        except (ValueError, TypeError):

            message = "Please enter a valid amount."

    return render_template(
        "compare.html",
        results=results,
        amount=amount,
        base_rate=base_rate,
        best_provider=best_provider,
        message=message
    )


# ==================================================
# HISTORY
# ==================================================

@app.route("/history")
def history():

    rates = get_rate_history()

    return render_template(
        "history.html",
        rates=rates
    )

# ==================================================
# RUN
# ==================================================

if __name__ == "__main__":

    app.run(debug=True)