from sqlalchemy import text
from app.models.database import DBConnection
from app.models.entities import User

def find_user_by_email(email: str):
    try:
        with DBConnection() as db:
            selected_user = db.execute(
                text("SELECT * FROM users WHERE email = :email"),
                {"email": f"{email}"}
            ).first()
        
            if not selected_user:
                return None  
        
            return User(**selected_user._mapping)
    except Exception as e:
        raise e
    
def insert_user(email: str, name: str, password: str):
    try:
        with DBConnection() as db:
            user = User(
                email=email,
                name=name,
                password=password,
                session_code=""
            )

            db.add(user)
    except Exception as e:
        raise e