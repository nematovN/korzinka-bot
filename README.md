# KorzinkaBot

A Telegram bot for Korzinka supermarket that allows users to browse products, add them to a cart, and checkout. The bot also includes admin functionality for managing products.

![KorzinkaBot](https://github.com/nematovN/korzinka-bot/blob/main/image.png)

## Features

### User Features
- 🛍 Browse products from menu
- ➕ Add products to cart with quantity selection
- 🧺 View cart contents with total price
- ❌ Remove products from cart
- 💰 Checkout and receive a detailed receipt
- 👤 Each user has their own cart

### Admin Features
- ➕ Add new products with name and price
- ✏️ Edit existing product names or prices
- ❌ Delete products from the system

## Technologies Used

- Python 3.9+
- Aiogram 3.x (Telegram Bot API framework)
- PostgreSQL (Database)
- asyncpg (Asynchronous PostgreSQL client)
- python-dotenv (Environment variable management)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nematovN/korzinka-bot.git
   cd korzinka-bot
