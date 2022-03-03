from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey

products_orders = db.Table('products_orders',
    Column('product_order_id', Integer, primary_key=True),
    Column('quantity', Integer, nullable=False),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('order_id', Integer,  ForeignKey('orders.id'))
)