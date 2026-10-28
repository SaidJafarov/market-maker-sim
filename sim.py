import random

random.seed(42)

V_LOW = 90
V_HIGH = 110

true_value = random.choice([V_LOW, V_HIGH])
print("True value:", true_value)

p = 0.5  # dealer's belief that the true value is V_HIGH

def expected_value(belief):
    return belief * V_HIGH + (1 - belief) * V_LOW

print("Dealer's best guess:", expected_value(p))

MU = 0.3  # probability a trader is informed

def trader_order(true_value):
    if random.random() < MU:
        return "buy" if true_value == V_HIGH else "sell"
    return random.choice(["buy", "sell"])

print("Trader order:", trader_order(true_value))
