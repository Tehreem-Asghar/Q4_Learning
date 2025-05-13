from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

# JSON body model
class User(BaseModel):
    name: str
    email: str
    age: int

app = FastAPI()

@app.put("/users/update/{user_id}")
async def update_user(
    user_id: int = Path(..., title="User ID", ge=1),
    active: bool = Query(True, description="Is the user active?"),
    user: User = Body(..., description="User data")
):
    return {
        "user_id": user_id,
        "active": active,
        "user_data": user.model_dump()
    }





# from fastapi import FastAPI, Path, Query, Body
# from pydantic import BaseModel

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float

# app = FastAPI()

# @app.put("/items/validated/{item_id}")
# async def update_item(
#     item_id: int = Path(..., title="Item ID", ge=1),
#     q: str | None = Query(None, min_length=3),
#     item: Item | None = Body(None, description="Optional item data (JSON body)")
# ):
#     result = {"item_id": item_id}
#     if q:
#         result.update({"q": q})
#     if item:
#         result.update({"item": item.model_dump()})
#     return result