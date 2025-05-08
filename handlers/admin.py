from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from config import ADMIN_IDS
from states import AdminStates
from keyboards import admin_kb, user_kb
from database.db import (
    add_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product
)

# Initialize router
admin_router = Router()

# Admin filter
def is_admin(message: Message):
    return message.from_user.id in ADMIN_IDS

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Handle the /admin command"""
    if not is_admin(message):
        await message.answer("Bu buyruq faqat adminlar uchun.")
        return
    
    await message.answer(
        "Admin panelga xush kelibsiz!",
        reply_markup=admin_kb.admin_menu()
    )

@admin_router.message(Text(text="➕ Mahsulot qo'shish"))
async def add_product_start(message: Message):
    """Start adding a new product"""
    if not is_admin(message):
        return
    
    await message.answer("Yangi mahsulot nomini kiriting:")
    await AdminStates.add_product_name.set()

@admin_router.message(Text(text="🔙 Asosiy menyu"))
async def back_to_main_menu(message: Message):
    """Return to main menu"""
    await message.answer(
        "Asosiy menyuga qaytdingiz.",
        reply_markup=user_kb.main_menu()
    )

@admin_router.message(AdminStates.add_product_name)
async def add_product_name(message: Message, state: FSMContext):
    """Process product name input"""
    await state.update_data(name=message.text)
    await message.answer("Mahsulot narxini kiriting (faqat raqam):")
    await state.set_state(AdminStates.add_product_price)

@admin_router.message(AdminStates.add_product_price)
async def add_product_price(message: Message, state: FSMContext):
    """Process product price input"""
    try:
        price = float(message.text)
        if price <= 0:
            await message.answer("Narx musbat son bo'lishi kerak. Qaytadan kiriting:")
            return
    except ValueError:
        await message.answer("Iltimos, faqat raqam kiriting. Qaytadan urinib ko'ring:")
        return
    
    user_data = await state.get_data()
    name = user_data.get('name')
    
    # Add product to database
    await add_product(name, price)
    
    await message.answer(
        f"Mahsulot qo'shildi:\nNomi: {name}\nNarxi: {price} so'm",
        reply_markup=admin_kb.admin_menu()
    )
    
    await state.clear()

@admin_router.message(Text(text="✏️ Mahsulotni o'zgartirish"))
async def edit_product_start(message: Message):
    """Start editing a product"""
    if not is_admin(message):
        return
    
    products = await get_all_products()
    if not products:
        await message.answer("Hozircha mahsulotlar mavjud emas.")
        return
    
    await message.answer(
        "O'zgartirish uchun mahsulotni tanlang:",
        reply_markup=admin_kb.product_list_for_edit(products)
    )

@admin_router.callback_query(F.data.startswith("edit:"))
async def edit_product_selected(callback: CallbackQuery, state: FSMContext):
    """Handle product selection for editing"""
    product_id = int(callback.data.split(':')[1])
    product = await get_product_by_id(product_id)
    
    if not product:
        await callback.answer("Mahsulot topilmadi")
        return
    
    await state.update_data(product_id=product_id)
    
    await callback.message.answer(
        f"Mahsulot: {product['name']}, Narxi: {product['price']} so'm\n\n"
        f"Nimani o'zgartirmoqchisiz?",
        reply_markup=admin_kb.edit_options()
    )
    
    await callback.answer()

@admin_router.callback_query(F.data.startswith("option:"))
async def edit_option_selected(callback: CallbackQuery, state: FSMContext):
    """Handle edit option selection"""
    option = callback.data.split(':')[1]
    
    if option == 'name':
        await callback.message.answer("Yangi nomni kiriting:")
        await state.set_state(AdminStates.edit_product_name)
    elif option == 'price':
        await callback.message.answer("Yangi narxni kiriting (faqat raqam):")
        await state.set_state(AdminStates.edit_product_price)
    
    await callback.answer()

@admin_router.message(AdminStates.edit_product_name)
async def edit_product_name(message: Message, state: FSMContext):
    """Process new product name input"""
    new_name = message.text
    user_data = await state.get_data()
    product_id = user_data.get('product_id')
    
    product = await get_product_by_id(product_id)
    await update_product(product_id, name=new_name, price=product['price'])
    
    await message.answer(
        f"Mahsulot nomi o'zgartirildi:\nYangi nomi: {new_name}",
        reply_markup=admin_kb.admin_menu()
    )
    
    await state.clear()

@admin_router.message(AdminStates.edit_product_price)
async def edit_product_price(message: Message, state: FSMContext):
    """Process new product price input"""
    try:
        new_price = float(message.text)
        if new_price <= 0:
            await message.answer("Narx musbat son bo'lishi kerak. Qaytadan kiriting:")
            return
    except ValueError:
        await message.answer("Iltimos, faqat raqam kiriting. Qaytadan urinib ko'ring:")
        return
    
    user_data = await state.get_data()
    product_id = user_data.get('product_id')
    
    product = await get_product_by_id(product_id)
    await update_product(product_id, name=product['name'], price=new_price)
    
    await message.answer(
        f"Mahsulot narxi o'zgartirildi:\nMahsulot: {product['name']}\nYangi narxi: {new_price} so'm",
        reply_markup=admin_kb.admin_menu()
    )
    
    await state.clear()

@admin_router.message(Text(text="❌ Mahsulotni o'chirish"))
async def delete_product_start(message: Message):
    """Start deleting a product"""
    if not is_admin(message):
        return
    
    products = await get_all_products()
    if not products:
        await message.answer("Hozircha mahsulotlar mavjud emas.")
        return
    
    await message.answer(
        "O'chirish uchun mahsulotni tanlang:",
        reply_markup=admin_kb.product_list_for_delete(products)
    )

@admin_router.callback_query(F.data.startswith("delete:"))
async def delete_product_selected(callback: CallbackQuery):
    """Handle product selection for deletion"""
    product_id = int(callback.data.split(':')[1])
    product = await get_product_by_id(product_id)
    
    if not product:
        await callback.answer("Mahsulot topilmadi")
        return
    
    await delete_product(product_id)
    
    await callback.message.answer(
        f"Mahsulot o'chirildi: {product['name']}",
        reply_markup=admin_kb.admin_menu()
    )
    
    await callback.answer()
