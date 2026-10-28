# Simulates a Glosten-Milgrom dealer who quotes a bid and an ask to a mix of
# informed traders (who know the true value) and noise traders (who buy or
# sell at random), updating their belief with Bayes' rule after each trade.
import matplotlib.pyplot as plt
import random
import statistics

V_LOW = 90
V_HIGH = 110

N_ROUNDS = 200

def expected_value(belief):
    return belief * V_HIGH + (1 - belief) * V_LOW

def trader_order(true_value, mu):
    if random.random() < mu:
        return "buy" if true_value == V_HIGH else "sell"
    return random.choice(["buy", "sell"])

def prob_buy(value, mu):
    if value == V_HIGH:
        return mu + (1 - mu) / 2
    else:
        return (1 - mu) / 2

def belief_after(order, belief, mu):
    if order == "buy":
        like_high = prob_buy(V_HIGH, mu)
        like_low = prob_buy(V_LOW, mu)
    else:
        like_high = 1 - prob_buy(V_HIGH, mu)
        like_low = 1 - prob_buy(V_LOW, mu)
    top = belief * like_high
    bottom = belief * like_high + (1 - belief) * like_low
    return top / bottom

def run_sim(mu, seed):
    random.seed(seed)
    true_value = random.choice([V_LOW, V_HIGH])
    p = 0.5  # dealer's belief that the true value is V_HIGH

    total_pnl = 0
    bids = []
    asks = []
    cum_pnl = []

    for t in range(N_ROUNDS):
        ask = expected_value(belief_after("buy", p, mu))
        bid = expected_value(belief_after("sell", p, mu))
        order = trader_order(true_value, mu)
        if order == "buy":
            pnl = ask - true_value   # dealer sold at the ask
        else:
            pnl = true_value - bid   # dealer bought at the bid
        total_pnl += pnl
        bids.append(bid)
        asks.append(ask)
        cum_pnl.append(total_pnl)
        p = belief_after(order, p, mu)

    return true_value, bids, asks, cum_pnl

def average_pnl(mu, n_runs):
    final_pnls = []
    for seed in range(n_runs):
        _, _, _, cum_pnl = run_sim(mu, seed)
        final_pnls.append(cum_pnl[-1])
    avg = sum(final_pnls) / n_runs
    std_err = statistics.stdev(final_pnls) / n_runs ** 0.5
    return avg, std_err

true_value, bids, asks, cum_pnl = run_sim(0.3, 42)

fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True)
ax_top.plot(bids, label="Bid")
ax_top.plot(asks, label="Ask")
ax_top.axhline(true_value, linestyle="--", color="gray", label="True value")
ax_top.legend()
ax_bottom.plot(cum_pnl)
ax_bottom.set_ylabel("Cumulative P&L")
ax_bottom.set_xlabel("Round")
fig.savefig("quotes_and_pnl.png")

fig, ax = plt.subplots()
for mu in [0.1, 0.3, 0.6]:
    _, bids, asks, _ = run_sim(mu, 42)
    spreads = [a - b for a, b in zip(asks, bids)]
    ax.plot(spreads, label=f"mu = {mu}")
ax.set_xlabel("Round")
ax.set_ylabel("Spread")
ax.legend()
fig.savefig("spread_vs_mu.png")

for mu in [0.1, 0.3, 0.6]:
    avg, std_err = average_pnl(mu, 2000)
    print(f"mu = {mu}: average P&L over 2000 runs = {avg:.2f} (standard error {std_err:.2f})")
