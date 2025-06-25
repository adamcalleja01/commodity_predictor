def should_alert(current_price: float, predicted_price: float, threshold: float = 0.015) -> str:
    """
    Generate an alert based on the current and predicted prices.
    
    Parameters:
    current_price (float): The current price of the commodity.
    predicted_price (float): The predicted next price of the commodity.
    threshold (float): The percentage change threshold to trigger an alert.
    
    Returns:
    str: Alert message if the price change exceeds the threshold, otherwise an empty string.
    """
    change = (predicted_price - current_price) / current_price
    abs_change = abs(change)

    if abs_change >= threshold:
        signal = "BUY" if change > 0 else "SELL"
        return True, signal, change * 100
    return False, "", change * 100
