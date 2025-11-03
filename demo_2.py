from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
#--------------
#1. cau hinh database
#---------------
DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
#--------------
#2. Định nghĩa Model SQLAlchemy (Bảng User)
#---------------
class User(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# -----------------------------
#3. Tạo bảng trong database
# -----------------------------
Base.metadata.create_all(bind=engine)
# -----------------------------
# 4. Schema (dùng cho API)
# -----------------------------
class UserCreate(BaseModel):
    name: str
    email: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# -----------------------------
# 5. Khởi tạo FastAPI
# -----------------------------
app = FastAPI(title="FastAPI CRUD with SQLite")

# -----------------------------
# 6. Dependency (Session)
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# 7. Các API CRUD
# -----------------------------

# them nguoi dung
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name,email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Xem danh sách người dùng
@app.get("/users/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
# Xem chi tiết 1 người dùng
@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Cập nhật người dùng
@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, updated: UserCreate, db: Session = Depends(get_db)):
    user= db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = updated.name
    user.email = updated.email
    db.commit()
    db.refresh(user)
    return user
# Xóa người dùng
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}