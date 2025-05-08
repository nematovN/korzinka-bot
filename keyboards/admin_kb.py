from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any

def admin_menu() -> ReplyKeyboardMarkup:
    """Admin menu keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="➕ Mahsulot qo'shish"))
    keyboard.add(KeyboardButton(text="✏️ Mahsulotni o'zgartirish"))
    keyboard.add(KeyboardButton(text="❌ Mahsulotni o'chirish"))
    keyboard.add(KeyboardButton(text="🔙 Asosiy menyu"))
    return keyboard

def product_list_for_edit(products: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Product list for editing"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    for product in products:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']} so'm",
                callback_data=f"edit:{product['id']}"
            )
        )
    return keyboard

def product_list_for_delete(products: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Product list for deletion"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    for product in products:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']} so'm",
                callback_data=f"delete:{product['id']}"
            )
        )
    return keyboard

def edit_options() -> InlineKeyboardMarkup:
    """Edit options keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Nomini o'zgartirish", callback_data="option:name"),
        InlineKeyboardButton(text="Narxini o'zgartirish", callback_data="option:price")
    )
    return keyboard
