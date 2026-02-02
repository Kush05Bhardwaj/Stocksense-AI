# Portfolio Simulation and Management
class Portfolio:
    def __init__(self,initial_cash= 100000):
        self.cash = initial_cash
        self.holdings = {} # stock_symbol -> number_of_shares

    def buy(self, symbol, price, quantity):
        cost = price * quantity
        if cost > self.cash:
            raise ValueError("Insufficient cash to complete purchase.")
        if symbol in self.holdings:
            total_qty = self.holdings[symbol]["qty"] + quantity
            avg_price = (
                (self.holdings[symbol]["avg_price"] * self.holdings[symbol]["qty"] + price * quantity) / total_qty
            )
            self.holdings[symbol] = {
                "qty": total_qty, 
                "avg_price": avg_price
            }
        else:
            self.holdings[symbol] = {
                "qty": quantity,
                "avg_price": price
            }
        
        self.cash -= cost
        return f"Bought {quantity} shares of {symbol} at ${price} each."
    
    def sell(self, symbol, price, quantity):
        if symbol not in self.holdings:
            raise ValueError("You do not own any shares of this stock.")
        if quantity > self.holdings[symbol]["qty"]:
            raise ValueError("Insufficient shares to complete sale.")
        
        self.holdings[symbol]["qty"] -= quantity
        self.cash += price * quantity

        if self.holdings[symbol]["qty"] == 0:
            del self.holdings[symbol]

        return f"Sold {quantity} shares of {symbol} at ${price} each."
    
    def get_portfolio_value(self, current_prices):
        value = self.cash
        for symbol, info in self.holdings.items():
            if symbol in current_prices:
                value += info["qty"] * current_prices[symbol]
        return round(value, 2)
    
    def profit_loss(self, current_prices):
        pl = 0
        for symbol, info in self.holdings.items():
            market_price = current_prices.get(symbol, 0)
            pl += (market_price - info["avg_price"]) * info["qty"]
        return round(pl, 2)
    
    def ai_decision(self, symbol, predicted_price, current_price, threshold=0.05):
        price_diff = predicted_price - current_price
        price_change_pct = price_diff / current_price

        if price_change_pct >= threshold:
            return "buy"
        elif price_change_pct <= -threshold:
            return "sell"
        else:
            return "hold"
        
        