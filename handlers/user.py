from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from states import UserStates
from keyboards import user_kb
from database.db import (
    get_all_products,
    get_product_by_id,
    add_to_cart,
    get_cart_items,
    remove_from_cart,
    clear_cart
)

# Initialize router
user_router = Router()

@user_router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle the /start command"""
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}!\n"
        f"Korzinka botiga xush kelibsiz. Mahsulotlarni ko'rish uchun quyidagi tugmani bosing:",
        reply_markup=user_kb.main_menu()
    )

@user_router.message(Text(text="🛍 Mahsulotlar"))
async def show_products(message: Message):
    """Show all available products"""
    products = await get_all_products()
    if not products:
        await message.answer("Hozircha mahsulotlar mavjud emas.")
        return
    
    await message.answer(
        "Mahsulotlar ro'yxati:",
        reply_markup=user_kb.product_list(products)
    )

@user_router.callback_query(F.data.startswith("product:"))
async def product_selected(callback: CallbackQuery, state: FSMContext):
    """Handle product selection"""
    product_id = int(callback.data.split(':')[1])
    product = await get_product_by_id(product_id)
    
    if not product:
        await callback.answer("Mahsulot topilmadi")
        return
    
    # Save product_id to state
    await state.update_data(selected_product_id=product_id)
    
    # Show product details with quantity selection
    await callback.message.answer(
        f"📦 {product['name']}\n"
        f"💰 Narxi: {product['price']} so'm\n\n"
        f"Miqdorni tanlang yoki kiriting:",
        reply_markup=user_kb.quantity_keyboard()
    )
    
    await state.set_state(UserStates.selecting_quantity)
    await callback.answer()

@user_router.message(UserStates.selecting_quantity)
async def quantity_selected(message: Message, state: FSMContext):
    """Handle quantity selection"""
    try:
        quantity = int(message.text)
        if quantity <= 0:
            await message.answer("Iltimos, musbat son kiriting.")
            return
    except ValueError:
        await message.answer("Iltimos, raqam kiriting.")
        return
    
    # Get product_id from state
    user_data = await state.get_data()
    product_id = user_data.get('selected_product_id')
    
    if not product_id:
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
        await state.clear()
        return
    
    # Add to cart
    product = await get_product_by_id(product_id)
    await add_to_cart(message.from_user.id, product_id, quantity)
    
    await message.answer(
        f"{product['name']} savatga qo'shildi. Miqdori: {quantity}",
        reply_markup=user_kb.after_adding_to_cart()
    )
    
    await state.clear()

@user_router.message(Text(text="🧺 Savatni ko'rish"))
async def show_cart(message: Message):
    """Show user's cart"""
    cart_items = await get_cart_items(message.from_user.id)
    
    if not cart_items:
        await message.answer("Savatingiz bo'sh.", reply_markup=user_kb.main_menu())
        return
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    cart_text = "🧺 Savatingizdagi mahsulotlar:\n\n"
    for i, item in enumerate(cart_items, 1):
        cart_text += (
            f"{i}. {item['name']} - {item['quantity']} dona\n"
            f"   {item['price']} x {item['quantity']} = {item['price'] * item['quantity']} so'm\n\n"
        )
    
    cart_text += f"\n💰 Jami: {total} so'm"
    
    await message.answer(
        cart_text,
        reply_markup=user_kb.cart_keyboard(cart_items)
    )

@user_router.callback_query(F.data.startswith("remove:"))
async def remove_cart_item(callback: CallbackQuery):
    """Remove item from cart"""
    item_id = int(callback.data.split(':')[1])
    user_id = callback.from_user.id
    
    await remove_from_cart(user_id, item_id)
    
    await callback.answer("Mahsulot savatdan olib tashlandi")
    
    # Show updated cart
    cart_items = await get_cart_items(user_id)
    
    if not cart_items:
        await callback.message.edit_text(
            "Savatingiz bo'sh.",
            reply_markup=None
        )
        await callback.message.answer("Savatingiz bo'sh.", reply_markup=user_kb.main_menu())
        return
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    cart_text = "🧺 Savatingizdagi mahsulotlar:\n\n"
    for i, item in enumerate(cart_items, 1):
        cart_text += (
            f"{i}. {item['name']} - {item['quantity']} dona\n"
            f"   {item['price']} x {item['quantity']} = {item['price'] * item['quantity']} so'm\n\n"
        )
    
    cart_text += f"\n💰 Jami: {total} so'm"
    
    await callback.message.edit_text(
        cart_text,
        reply_markup=user_kb.cart_keyboard(cart_items)
    )

@user_router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery):
    """Process checkout"""
    user_id = callback.from_user.id
    cart_items = await get_cart_items(user_id)
    
    if not cart_items:
        await callback.answer("Savatingiz bo'sh.")
        return
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    receipt = "🧾 CHEK 🧾\n\n"
    receipt += f"Mijoz: {callback.from_user.full_name}\n"
    receipt += f"Sana: {callback.message.date.strftime('%Y-%m-%d %H:%M')}\n\n"
    receipt += "Mahsulotlar:\n"
    
    for i, item in enumerate(cart_items, 1):
        receipt += (
            f"{i}. {item['name']} - {item['quantity']} dona\n"
            f"   {item['price']} x {item['quantity']} = {item['price'] * item['quantity']} so'm\n\n"
        )
    
    receipt += f"\n💰 Jami: {total} so'm\n"
    receipt += "\nXaridingiz uchun rahmat!"
    
    await callback.message.answer(receipt)
    
    # Clear the cart
    await clear_cart(user_id)
    
    await callback.answer("Xaridingiz uchun rahmat!")
    await callback.message.answer(
        "Boshqa mahsulotlar xarid qilishni xohlaysizmi?",
        reply_markup=user_kb.main_menu()
    )
