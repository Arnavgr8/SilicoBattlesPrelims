import random

class WorstPossibleStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks
        self.history = {stock: [] for stock in available_stocks}

    def decide_action(self, bot):
        stock = random.choice(self.available_stocks)
        self.history[stock].append(stock.current_price)
        if len(self.history[stock]) > 5:
            self.history[stock].pop(0)

        if len(self.history[stock]) >= 3:
            if self.history[stock][-1] > self.history[stock][-2] > self.history[stock][-3]:
                action = "buy"
            elif self.history[stock][-1] < self.history[stock][-2] < self.history[stock][-3]:
                action = "sell"
            else:
                action = random.choice(["buy", "sell"])
        else:
            action = random.choice(["buy", "sell"])

        if stock.volatility_type == "speculative":
            amount = random.randint(5, 10)
        elif stock.volatility_type in ["inconsistent", "slow_growth"]:
            amount = random.randint(3, 6)
        else:
            amount = random.randint(2, 4)

        if stock.current_price > 100:
            amount = min(amount + 2, 10)

        if action == "buy":
            max_affordable = int(bot.cash // stock.current_price)
            if max_affordable > 0:
                actual_amount = min(amount, max_affordable)
                bot.buy(stock, actual_amount)
        elif action == "sell":
            held = bot.portfolio.get(stock, 0)
            if held > 0:
                actual_amount = min(amount, held)
                bot.sell(stock, actual_amount)

        return action
