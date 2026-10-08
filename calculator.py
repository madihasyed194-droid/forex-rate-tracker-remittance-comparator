# Remittance provider fee slabs

providers = {

    "Provider A": {
        "fee_slabs": [
            (500, 5),
            (1000, 8),
            (5000, 12),
            (float("inf"), 20)
        ],
        "rate_markup": 0.50
    },

    "Provider B": {
        "fee_slabs": [
            (500, 4),
            (1000, 7),
            (5000, 11),
            (float("inf"), 18)
        ],
        "rate_markup": 0.30
    },

    "Provider C": {
        "fee_slabs": [
            (500, 6),
            (1000, 9),
            (5000, 13),
            (float("inf"), 22)
        ],
        "rate_markup": 0.20
    }
}


# Find the correct fee according to amount
def get_fee(amount, slabs):

    for maximum_amount, fee in slabs:

        if amount <= maximum_amount:
            return fee

    return 0


# Calculate money received
def calculate_remittance(amount, base_rate, fee, rate_markup):

    effective_rate = base_rate - rate_markup

    amount_after_fee = amount - fee

    received_amount = amount_after_fee * effective_rate

    return {
        "fee": fee,
        "effective_rate": effective_rate,
        "received_amount": received_amount
    }


# Compare all providers
def compare_providers(amount, base_rate):

    results = []

    for provider, details in providers.items():

        fee = get_fee(
            amount,
            details["fee_slabs"]
        )

        result = calculate_remittance(
            amount,
            base_rate,
            fee,
            details["rate_markup"]
        )

        results.append({
            "provider": provider,
            "fee": fee,
            "effective_rate": result["effective_rate"],
            "received_amount": result["received_amount"]
        })

    return results


# Test the calculator
if __name__ == "__main__":

    amount = 1000

    base_rate = 95.80

    results = compare_providers(
        amount,
        base_rate
    )

    print("\nREMItTANCE COMPARISON")
    print("-" * 50)

    for result in results:

        print("Provider:", result["provider"])
        print("Fee: $", result["fee"])
        print("Effective Rate: ₹", result["effective_rate"])
        print("Amount Received: ₹", result["received_amount"])
        print("-" * 50)