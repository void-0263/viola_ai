# main.py
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, SessionLocal
from models import User

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for testing; tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

@app.post("/register")
def register_user(
    username: str = Form(...),
    email: str = Form(...),
    vehicle_plate: str = Form(None),
    phone_number: str = Form(...)
):
    db = SessionLocal()
    user = User(
        username=username,
        email=email,
        vehicle_plate=vehicle_plate,
        phone_number=phone_number
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"message": "User registered successfully!", "user_id": user.id}
