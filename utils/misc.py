def format_price(price):
    """Format price with thousand separators"""
    return f"{price:,.0f}".replace(",", " ")
