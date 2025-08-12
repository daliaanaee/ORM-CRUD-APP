from sqlmodel import SQLModel, Field, create_engine, Session

class Customer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    product_id: int = Field(foreign_key="product.id")
    status: str
    quantity: int

sqlite_url = "sqlite:///hw5.db"
engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    c1 = Customer(first_name="Daniel", last_name="Brown")
    c2 = Customer(first_name="Kevin", last_name="Anderson")
    c3 = Customer(first_name="Sophia", last_name="Hall")

    p1 = Product(name="Smartphone", price=170.26)
    p2 = Product(name="Laptop", price=360.82)
    p3 = Product(name="LED Television", price=665.00)
    p4 = Product(name="Gaming Console", price=460.67)
    p5 = Product(name="Smartwatch", price=892.68)

    session.add_all([c1, c2, c3, p1, p2, p3, p4, p5])
    session.commit()

    o1 = Order(customer_id=c1.id, product_id=p5.id, status="Shipped", quantity=2)
    o2 = Order(customer_id=c3.id, product_id=p1.id, status="Delivered", quantity=1)
    o3 = Order(customer_id=c1.id, product_id=p4.id, status="Delivered", quantity=2)
    o4 = Order(customer_id=c2.id, product_id=p5.id, status="Delivered", quantity=3)

    session.add_all([o1, o2, o3, o4])
    session.commit()
