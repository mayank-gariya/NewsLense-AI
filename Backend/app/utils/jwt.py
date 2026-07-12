from datetime import datetime , timedelta , timezone
from jose import JWTError , jwt 
from app.config.settings import settings
from fastapi import HTTPException , status

def create_access_token(data:dict):
    to_encode = data.copy()  # copying the data not passing any refernce changes do not affect real one 
    
    # creates the expire of jwt token 
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode['exp'] = expire # setting expire 

    encoded_jwt = jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm) # create the token
    
    return encoded_jwt 

def verify_access_token(token:str):
    
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        ) # returns python dictonary 
        
        email = payload.get('sub')
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return email
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )