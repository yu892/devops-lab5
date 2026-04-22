from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/users", tags=["users"])

class User(BaseModel):
    id: int
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

users_db = {
    1: {"id": 1, "name": "John Doe", "email": "john@example.com"}
}
next_id = 2

@router.get("/", response_model=List[User])
async def get_users():
    return list(users_db.values())

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    global next_id
    new_user = {"id": next_id, "name": user.name, "email": user.email}
    users_db[next_id] = new_user
    next_id += 1
    return new_user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    if user.name is not None:
        users_db[user_id]["name"] = user.name
    if user.email is not None:
        users_db[user_id]["email"] = user.email
    return users_db[user_id]

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return None
EOF
