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

def prob_buy(value):
    if value == V_HIGH:
        return MU + (1 - MU) / 2
    else:
        return (1 - MU) / 2

def belief_after(order, belief):
    if order == "buy":
        like_high = prob_buy(V_HIGH)
        like_low = prob_buy(V_LOW)
    else:
        like_high = 1 - prob_buy(V_HIGH)
        like_low = 1 - prob_buy(V_LOW)
    top = belief * like_high
    bottom = belief * like_high + (1 - belief) * like_low
    return top / bottom

ask = expected_value(belief_after("buy", p))
bid = expected_value(belief_after("sell", p))
print("Bid:", bid, "Ask:", ask)

N_ROUNDS = 200

for t in range(N_ROUNDS):
    ask = expected_value(belief_after("buy", p))
    bid = expected_value(belief_after("sell", p))
    order = trader_order(true_value)
    if t % 20 == 0:
        print(t, round(bid, 2), round(ask, 2), round(p, 3))
    p = belief_after(order, p)
