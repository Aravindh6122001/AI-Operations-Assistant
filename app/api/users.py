from fastapi import Depends , APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.users import UserCreate,UserResponse,UserUpdate
from app.services import user_service

router = APIRouter(prefix='/users',tags=["Users"])

#Post
@router.post("/",response_model=UserResponse)
def create_user(user:UserCreate, db:Session = Depends(get_db)):
    return user_service.create_user(db,user.name,user.email)

#Get all  
@router.get("/",response_model=list[UserResponse])
def get_users(db:Session = Depends(get_db)):    
    return user_service.get_users(db)   

#Get one
@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id:int,db:Session = Depends(get_db)):
    
    return user_service.get_user(db,user_id) 

#Delete one
@router.delete("/{user_id}",response_model=UserResponse)
def delete_user(user_id:int,db:Session = Depends(get_db)):
    return user_service.delete(db,user_id)


#Update one
@router.patch("/{user_id}",response_model=UserResponse)
def update_user(user_id:int,user_input:UserUpdate,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404,detail="User Not Found")
    
    if user_input.name is not None:
        user.name = user_input.name
        
    if user_input.email is not None:
             user.email = user_input.email   
        

    db.commit()
    db.refresh(user);
    
    return user
 
    