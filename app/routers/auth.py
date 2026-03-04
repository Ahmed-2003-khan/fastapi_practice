from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models

router = APIRouter(tags=['Authentication'])

# POST /login - authenticates a user with email and password
# Uses 403 Forbidden (not 404) to avoid revealing whether the email exists
@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    # Look up the user by email in the database
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        # 403 used intentionally - generic "Invalid Credentials" hides whether email exists
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
