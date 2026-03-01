from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.envs import envs
 
Base = declarative_base()

class DBConnection():
    def __init__(self):
        self.__engine = self.__create_engine()
        self.__session = None
        
    def __create_engine(self):
        engine = create_engine(f"postgresql+psycopg2://{envs['DATABASE_USER_SQL']}:{envs['DATABASE_PASSWORD_SQL']}@db:5432/{envs['DATABASE_NAME_SQL']}", echo=False)
        
        return engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        
        self.__session = session_make()
        
        return self.__session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.commit()
        self.__session.close()