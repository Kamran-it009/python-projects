from contextlib import asynccontextmanager
from typing import Annotated, Union, Optional
from fastapi_neon.database import connection_string
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import Depends, FastAPI
from fastapi import HTTPException


engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

def get_db():
    db  = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(index=True)  

class TodoCreate(SQLModel):
      description: str = Field(index=True)

class TodoResponse(SQLModel):
      id : int
      description : str


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# The first part of the function, before the yield, will
# be executed before the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="Kamran Todos API")


@app.post("/todos/", response_model= TodoResponse)
def create_todo(db: db_dependency, todo: TodoCreate):
        # Remove the id field from the dictionary
        todo_dict = todo.dict()
        # todo_dict.pop("id", None)
        # Create a new Todo object without the id field
        new_todo = Todo(**todo_dict)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo

@app.get("/todos/")
def read_todos(db: db_dependency):
        todos = db.exec(select(Todo)).all()
        if not todos:
            raise HTTPException(status_code=404, detail="Todos are empty")
        return todos

@app.get("/todos/{id}")
def read_todo(db: db_dependency, id: int):
        todo = db.exec(select(Todo).where(Todo.id == id)).first()
        if not todo:
             raise HTTPException(status_code=404, detail="Todo not found")
        return todo



@app.put("/todos/{id}")
def update_todo(db: db_dependency, id: int, todo: TodoCreate):
    todo2: Todo | None = db.exec(select(Todo).where(Todo.id == id)).first()
    if not todo2:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo2.description = todo.description
    db.commit()
    db.refresh(todo2)
    return {"message": "Todo updated successfully"}
    
@app.delete("/todos/{id}")
def delete_todo(db: db_dependency, id: int):
        todo = db.exec(select(Todo).where(Todo.id == id)).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        db.delete(todo)
        db.commit()
        return {"message": "Todo deleted successfully"}
    


