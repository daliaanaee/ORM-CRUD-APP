from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from contextlib import asynccontextmanager

class Customer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str

class CustomerCreate(SQLModel):
    first_name: str
    last_name: str

class CustomerRead(SQLModel):
    id: int
    first_name: str
    last_name: str

class CustomerUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None

sqlite_url = "sqlite:///hw5.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/customers/", response_model=int)
def create_customer(customer: CustomerCreate, session: Session = Depends(get_session)):
    db_customer = Customer.model_validate(customer)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer.id

@app.get("/customers/", response_model=list[CustomerRead])
def read_customers(session: Session = Depends(get_session)):
    return session.exec(select(Customer)).all()

@app.get("/customers/{id}", response_model=CustomerRead)
def read_customer(id: int, session: Session = Depends(get_session)):
    customer = session.get(Customer, id)
    if customer is None:
        raise HTTPException(404, f"Customer {id} not found")
    return customer

@app.put("/customers/{id}", response_model=CustomerRead)
def update_customer(id: int, data: CustomerCreate, session: Session = Depends(get_session)):
    customer = session.get(Customer, id)
    if customer is None:
        raise HTTPException(404, f"Customer {id} not found")
    customer.sqlmodel_update(data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.delete("/customers/{id}")
def delete_customer(id: int, session: Session = Depends(get_session)):
    customer = session.get(Customer, id)
    if customer is None:
        raise HTTPException(404, f"Customer {id} not found")
    session.delete(customer)
    session.commit()
