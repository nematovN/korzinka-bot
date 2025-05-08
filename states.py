from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    """User states for FSM"""
    selecting_quantity = State()

class AdminStates(StatesGroup):
    """Admin states for FSM"""
    # Add product states
    add_product_name = State()
    add_product_price = State()
    
    # Edit product states
    edit_product_name = State()
    edit_product_price = State()
