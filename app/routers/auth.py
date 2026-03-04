from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2
from ..utils import verify

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Create a signed JWT with user_id in the payload
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # OAuth2 standard response: access_token + token_type="bearer"
    return {"access_token": access_token, "token_type": "bearer"}