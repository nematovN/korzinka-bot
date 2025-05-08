from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any

def main_menu() -> ReplyKeyboardMarkup:
    """Main menu keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="🛍 Mahsulotlar"))
    keyboard.add(KeyboardButton(text="🧺 Savatni ko'rish"))
    return keyboard

def product_list(products: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Product list as inline keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    for product in products:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']} so'm",
                callback_data=f"product:{product['id']}"
            )
        )
    return keyboard

def quantity_keyboard() -> ReplyKeyboardMarkup:
    """Quantity selection keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [KeyboardButton(text=str(i)) for i in range(1, 10)]
    keyboard.add(*buttons)
    return keyboard

def after_adding_to_cart() -> ReplyKeyboardMarkup:
    """Keyboard after adding product to cart"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="🛍 Mahsulotlar"))
    keyboard.add(KeyboardButton(text="🧺 Savatni ko'rish"))
    return keyboard

def cart_keyboard(cart_items: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Cart management keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for item in cart_items:
        keyboard.add(
            InlineKeyboardButton(
                text=f"❌ {item['name']}",
                callback_data=f"remove:{item['id']}"
            )
        )
    
    keyboard.add(InlineKeyboardButton(text="💰 Hisob-kitob", callback_data="checkout"))
    return keyboard
