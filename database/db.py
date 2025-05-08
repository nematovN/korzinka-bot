import logging
import asyncpg
from typing import List, Dict, Any, Optional
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Connection pool
pool = None

async def init_db():
    """Initialize the database connection pool"""
    global pool
    try:
        # Create a connection pool
        pool = await asyncpg.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logging.info("Database connection pool created successfully")
    except Exception as e:
        logging.error(f"Error creating connection pool: {e}")
        raise e

async def create_tables():
    """Create necessary tables if they don't exist"""
    async with pool.acquire() as conn:
        try:
            # Create products table
            await conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                price NUMERIC(10, 2) NOT NULL
            )
            ''')
            
            # Create cart table
            await conn.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            )
            ''')
            
            logging.info("Tables created successfully")
        except Exception as e:
            logging.error(f"Error creating tables: {e}")
            raise e

# Product operations
async def add_product(name: str, price: float) -> int:
    """Add a new product"""
    async with pool.acquire() as conn:
        try:
            product_id = await conn.fetchval(
                "INSERT INTO products (name, price) VALUES ($1, $2) RETURNING id",
                name, price
            )
            return product_id
        except Exception as e:
            logging.error(f"Error adding product: {e}")
            raise e

async def get_all_products() -> List[Dict[str, Any]]:
    """Get all products"""
    async with pool.acquire() as conn:
        try:
            products = await conn.fetch("SELECT * FROM products ORDER BY id")
            return [dict(product) for product in products]
        except Exception as e:
            logging.error(f"Error getting products: {e}")
            raise e

async def get_product_by_id(product_id: int) -> Optional[Dict[str, Any]]:
    """Get product by ID"""
    async with pool.acquire() as conn:
        try:
            product = await conn.fetchrow("SELECT * FROM products WHERE id = $1", product_id)
            return dict(product) if product else None
        except Exception as e:
            logging.error(f"Error getting product: {e}")
            raise e

async def update_product(product_id: int, name: str, price: float) -> None:
    """Update product information"""
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                "UPDATE products SET name = $1, price = $2 WHERE id = $3",
                name, price, product_id
            )
        except Exception as e:
            logging.error(f"Error updating product: {e}")
            raise e

async def delete_product(product_id: int) -> None:
    """Delete a product"""
    async with pool.acquire() as conn:
        try:
            await conn.execute("DELETE FROM products WHERE id = $1", product_id)
        except Exception as e:
            logging.error(f"Error deleting product: {e}")
            raise e

# Cart operations
async def add_to_cart(user_id: int, product_id: int, quantity: int) -> None:
    """Add product to cart"""
    async with pool.acquire() as conn:
        try:
            # Check if product already in cart
            existing_item = await conn.fetchrow(
                "SELECT * FROM cart WHERE user_id = $1 AND product_id = $2",
                user_id, product_id
            )
            
            if existing_item:
                # Update quantity
                new_quantity = existing_item['quantity'] + quantity
                await conn.execute(
                    "UPDATE cart SET quantity = $1 WHERE id = $2",
                    new_quantity, existing_item['id']
                )
            else:
                # Add new item
                await conn.execute(
                    "INSERT INTO cart (user_id, product_id, quantity) VALUES ($1, $2, $3)",
                    user_id, product_id, quantity
                )
        except Exception as e:
            logging.error(f"Error adding to cart: {e}")
            raise e

async def get_cart_items(user_id: int) -> List[Dict[str, Any]]:
    """Get user's cart items with product details"""
    async with pool.acquire() as conn:
        try:
            cart_items = await conn.fetch('''
            SELECT c.id, c.product_id, c.quantity, p.name, p.price
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = $1
            ''', user_id)
            
            return [dict(item) for item in cart_items]
        except Exception as e:
            logging.error(f"Error getting cart items: {e}")
            raise e

async def remove_from_cart(user_id: int, cart_id: int) -> None:
    """Remove item from cart"""
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                "DELETE FROM cart WHERE id = $1 AND user_id = $2",
                cart_id, user_id
            )
        except Exception as e:
            logging.error(f"Error removing from cart: {e}")
            raise e

async def clear_cart(user_id: int) -> None:
    """Clear user's cart"""
    async with pool.acquire() as conn:
        try:
            await conn.execute("DELETE FROM cart WHERE user_id = $1", user_id)
        except Exception as e:
            logging.error(f"Error clearing cart: {e}")
            raise e
