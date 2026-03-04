from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models
# verify() imported directly from utils to check plain password against stored bcrypt hash
from ..utils import verify

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    # Step 1: Check if a user with this email exists
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        # Same error message as wrong password to prevent user enumeration
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Step 2: Verify the provided password against the stored bcrypt hash
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Step 3: Create and return a JWT token (placeholder - real JWT coming next)
    return {"token": "example-jwt-token"}