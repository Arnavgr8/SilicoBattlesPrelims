import random

class GamblerStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks

    def decide_action(self, bot):
        # Risky strategy: Randomly buy/sell with high amounts, favoring speculative stocks
        stock = random.choice([s for s in self.available_stocks if s.volatility_type == "speculative"])
        action = random.choice(["buy", "sell", "buy"])  # More likely to buy
        amount = random.randint(3, 8)  # Higher amounts
        if action == "buy" and bot.cash >= stock.current_price * amount:
            bot.buy(stock, amount)
        elif action == "sell" and bot.portfolio[stock] >= amount:
            bot.sell(stock, amount)
        return action


class ClassicStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks

    def decide_action(self, bot):
        # Balanced approach: Focus on consistent stocks with moderate amounts
        stock = random.choice([s for s in self.available_stocks if s.volatility_type in ["consistent", "stable"]])
        action = random.choice(["buy", "hold", "hold"])  # More likely to hold
        amount = random.randint(1, 3)  # Moderate amounts
        if action == "buy" and bot.cash >= stock.current_price * amount:
            bot.buy(stock, amount)
        elif action == "sell" and bot.portfolio[stock] >= amount:
            bot.sell(stock, amount)
        return action


class PatientStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks

    def decide_action(self, bot):
        # Long-term strategy: Buy low-volatility stocks and rarely sell
        stock = random.choice([s for s in self.available_stocks if s.volatility_type in ["consistent", "slow_growth"]])
        action = random.choice(["buy", "hold", "hold", "hold"])  # Much more likely to hold
        if action == "buy" and bot.cash >= stock.current_price:
            bot.buy(stock, 1)  # Small, consistent purchases
        return action


class AggressiveStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks

    def decide_action(self, bot):
        # High-risk: Focus on speculative and inconsistent stocks with large trades
        stock = random.choice([s for s in self.available_stocks if s.volatility_type in ["speculative", "inconsistent"]])
        action = random.choice(["buy", "sell"])  # Always active trading
        amount = random.randint(4, 10)  # Large amounts
        if action == "buy" and bot.cash >= stock.current_price * amount:
            bot.buy(stock, amount)
        elif action == "sell" and bot.portfolio[stock] >= amount:
            bot.sell(stock, amount)
        return action


class ConservativeStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks

    def decide_action(self, bot):
        # Ultra-conservative: Only stable stocks with minimal trading
        stock = random.choice([s for s in self.available_stocks if s.volatility_type == "stable"])
        action = random.choice(["buy", "hold", "hold", "hold", "hold"])  # Mostly holding
        if action == "buy" and bot.cash >= stock.current_price:
            bot.buy(stock, 1)  # Minimal purchases
        return action


class TrendFollowerStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks
        self.price_history = {stock: [] for stock in available_stocks}

    def decide_action(self, bot):
        # Follow price trends: Buy rising stocks, sell falling ones
        stock = random.choice(self.available_stocks)
        self.price_history[stock].append(stock.current_price)
        if len(self.price_history[stock]) > 3:
            self.price_history[stock].pop(0)
            
        action = "hold"
        if len(self.price_history[stock]) >= 3:
            if self.price_history[stock][-1] > self.price_history[stock][-2] > self.price_history[stock][-3]:
                action = "buy"
            elif self.price_history[stock][-1] < self.price_history[stock][-2] < self.price_history[stock][-3]:
                action = "sell"
                
        amount = random.randint(1, 3)
        if action == "buy" and bot.cash >= stock.current_price * amount:
            bot.buy(stock, amount)
        elif action == "sell" and bot.portfolio[stock] >= amount:
            bot.sell(stock, amount)
        return action


class RiskAverseStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks

    def decide_action(self, bot):
        # Extremely risk-averse: Only consistent stocks, never speculative
        stock = random.choice([s for s in self.available_stocks if s.volatility_type == "consistent"])
        action = "hold"
        if bot.cash > bot.calculate_total_value() * 0.3:  # Only buy if cash is >30% of portfolio
            action = "buy"
        if action == "buy" and bot.cash >= stock.current_price:
            bot.buy(stock, 1)
        return action


class OpportunisticStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks
        self.price_tracking = {stock: stock.current_price for stock in available_stocks}

    def decide_action(self, bot):
        # Buy dips, sell peaks based on initial price
        stock = random.choice(self.available_stocks)
        action = "hold"
        price_change = ((stock.current_price - self.price_tracking[stock]) / self.price_tracking[stock]) * 100
        
        if price_change < -15:  # Buy on 15% dip
            action = "buy"
        elif price_change > 20:  # Sell on 20% gain
            action = "sell"
            
        amount = random.randint(1, 4)
        if action == "buy" and bot.cash >= stock.current_price * amount:
            bot.buy(stock, amount)
        elif action == "sell" and bot.portfolio[stock] >= amount:
            bot.sell(stock, amount)
        return action


class DiversificationStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks
        self.max_per_stock = 0.2  # Maximum 20% in any one stock

    def decide_action(self, bot):
        # Maintain a diversified portfolio
        total_value = bot.calculate_total_value()
        for stock in self.available_stocks:
            stock_value = bot.portfolio[stock] * stock.current_price
            if stock_value / total_value > self.max_per_stock:
                bot.sell(stock, 1)
                return "sell"
        
        stock = random.choice(self.available_stocks)
        if bot.cash >= stock.current_price:
            bot.buy(stock, 1)
            return "buy"
        return "hold"


class BlueChipStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks
        self.blue_chips = [s for s in available_stocks if s.current_price > 100]  # Consider high-priced stocks as blue chips

    def decide_action(self, bot):
        # Focus exclusively on blue chip stocks
        if not self.blue_chips:
            return "hold"
            
        stock = random.choice(self.blue_chips)
        action = random.choice(["buy", "hold", "hold", "hold"])
        
        if action == "buy" and bot.cash >= stock.current_price:
            bot.buy(stock, 1)
        return action


class CounterTrendStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks
        self.price_history = {stock: [] for stock in available_stocks}

    def decide_action(self, bot):
        # Trade against the trend (contrarian)
        stock = random.choice(self.available_stocks)
        self.price_history[stock].append(stock.current_price)
        if len(self.price_history[stock]) > 5:
            self.price_history[stock].pop(0)
            
        action = "hold"
        if len(self.price_history[stock]) >= 5:
            # Buy if price has been consistently falling
            if all(self.price_history[stock][i] > self.price_history[stock][i+1] for i in range(3)):
                action = "buy"
            # Sell if price has been consistently rising
            elif all(self.price_history[stock][i] < self.price_history[stock][i+1] for i in range(3)):
                action = "sell"
                
        amount = random.randint(1, 2)
        if action == "buy" and bot.cash >= stock.current_price * amount:
            bot.buy(stock, amount)
        elif action == "sell" and bot.portfolio[stock] >= amount:
            bot.sell(stock, amount)
        return action


class SmallCapStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks
        self.small_caps = [s for s in available_stocks if s.current_price < 50]

    def decide_action(self, bot):
        # Focus on small cap stocks with high growth potential
        if not self.small_caps:
            return "hold"
            
        stock = random.choice(self.small_caps)
        action = random.choice(["buy", "sell", "buy"])
        amount = random.randint(2, 5)
        
        if action == "buy" and bot.cash >= stock.current_price * amount:
            bot.buy(stock, amount)
        elif action == "sell" and bot.portfolio[stock] >= amount:
            bot.sell(stock, amount)
        return action


class HedgingStrategy:
    def __init__(self, available_stocks):
        self.available_stocks = available_stocks
        self.volatile_stocks = [s for s in available_stocks if s.volatility_type == "speculative"]
        self.stable_stocks = [s for s in available_stocks if s.volatility_type == "stable"]

    def decide_action(self, bot):
        # Balance risky positions with stable ones
        total_value = bot.calculate_total_value()
        volatile_value = sum(bot.portfolio[s] * s.current_price for s in self.volatile_stocks)
        
        if volatile_value > total_value * 0.3:  # If too much in volatile stocks
            if self.stable_stocks:
                stock = random.choice(self.stable_stocks)
                if bot.cash >= stock.current_price:
                    bot.buy(stock, 1)
                    return "buy"
        else:
            if self.volatile_stocks:
                stock = random.choice(self.volatile_stocks)
                if bot.cash >= stock.current_price:
                    bot.buy(stock, 1)
                    return "buy"
        return "hold"

strategies = [PatientInvestor, GamblerStrategy, ClassicStrategy, PatientStrategy, AggressiveStrategy, ConservativeStrategy, TrendFollowerStrategy, RiskAverseStrategy, OpportunisticStrategy, DiversificationStrategy, BlueChipStrategy, CounterTrendStrategy, SmallCapStrategy, HedgingStrategy]
