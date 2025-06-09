from fastapi import FastAPI, Depends
from schemas import UserCreate

app = FastAPI()

@app.post("/users")
def create_user(user: UserCreate):
    # You can now access validated data directly:
    return {"message": f"User created: {user.name}, email: {user.email}"}
