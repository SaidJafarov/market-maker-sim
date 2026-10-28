import random

random.seed(42)

V_LOW = 90
V_HIGH = 110

true_value = random.choice([V_LOW, V_HIGH])
print("True value:", true_value)

p = 0.5  # dealer's belief that the true value is V_HIGH

def expected_value(p):
    return p * V_HIGH + (1 - p) * V_LOW

print("Dealer's best guess:", expected_value(p))
