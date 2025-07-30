# Strategy Development Challenge: Stock Trading Bot

Your task is to design a stock trading strategy class in Python that can be plugged into our simulation framework.

## Requirements

### File Naming

Save your strategy in a file named:  
`YourSchoolName_Strategy.py`  
(replace `YourSchoolName` with your actual school or team name).

### Class Structure

Define a class named `YourStrategyName` (e.g., `AggressiveStrategy`, `PatientStrategy`, etc.).

The class must have:

- `__init__(self, available_stocks)` method that takes a list of stock objects.
- `decide_action(self, bot)` method that:
  - Takes a bot instance.
  - Returns the action your strategy wants the bot to take on each step.

### Available Tools

You may only use Python's built-in `random` module for randomness.

### Stock Objects

The `available_stocks` list contains stock objects with at least these attributes:

- `current_price`: the current price of the stock.
- `volatility_type`: a string such as `"stable"`, `"speculative"`, `"consistent"`, `"slow_growth"`, or `"inconsistent"`.

### Bot Instance

The bot instance has:

- `cash`: available cash.
- `portfolio`: a dictionary with stocks as keys and owned amount as values.

#### Bot Methods

- `buy(stock, amount)`: attempts to buy the given amount of stock.
- `sell(stock, amount)`: attempts to sell the given amount of stock.
- `calculate_total_value()`: returns total value of cash + stocks.

## Strategy Behavior

Your strategy should decide actions like:

- `"buy"` — purchase some amount of a stock.
- `"sell"` — sell some amount of a stock.
- `"hold"` — do nothing.

### Important

The return value of `decide_action` must follow this format:

- For buy or sell actions, return a tuple:  
  `("buy", stock, amount)` or `("sell", stock, amount)`  
  where `stock` is a stock object and `amount` is an integer.

- For hold, return the string:  
  `"hold"`  

(Do **not** return tuples containing `None` or zero amounts for hold; just return the string `"hold"`.)

Keep trading amounts and stock choices consistent with your strategy type.

You can take inspiration from the examples shared but using exact same logic will lead to disqualification.

In the simulations, you'll face off only against other school's logics, not the examples.

## How We Use Your Strategy

We will import your strategy class in our simulation environment and pit it against other strategies to see which performs best.
