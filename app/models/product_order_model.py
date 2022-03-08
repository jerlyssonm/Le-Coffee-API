""" from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey

products_orders = db.Table('products_orders',
    Column('product_order_id', Integer, primary_key=True),
    Column('quantity', Integer, nullable=False),
    Column('product_id', Integer, ForeignKey('products.product_id')),
    Column('order_id', Integer,  ForeignKey('orders.order_id'))
) """
from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey
from dataclasses import dataclass
from sqlalchemy.orm import relationship

@dataclass
class ProductsOrderModel(db.Model):
    product_order_id: int
    quantity: int
    product_id: int
    order_id: int

    __tablename__ = "products_orders"

    product_order_id = Column('product_order_id', Integer, primary_key=True)
    quantity = Column('quantity', Integer, nullable=False)
    product_id = Column('product_id', Integer, ForeignKey('products.product_id'))
    order_id = Column('order_id', Integer,  ForeignKey('orders.order_id'))

    """ user = relationship("UserModel", back_populates="order")
    products = relationship("ProductsOrdersModel") """