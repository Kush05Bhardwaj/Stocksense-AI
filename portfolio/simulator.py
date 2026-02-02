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