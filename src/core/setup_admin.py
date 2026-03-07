import logging

from sqlalchemy import select

from src.core.config import settings
from src.db.models.user import User
from src.db.session import SessionLocal
from src.domain.enums.user_role import UserRole


def create_admin():
    db = SessionLocal()
    try:
        admin_exists = db.execute(
            select(User).where(User.role == UserRole.ADMIN)
        ).scalar_one_or_none()

        if admin_exists:
            logging.info(f'Admin ({admin_exists.username}) already exists') 
            return

        admin = User(
            username=settings.ADMIN,
            hashed_password=settings.ADMIN_PASSWORD,
            role=UserRole.ADMIN
        )
        
        db.add(admin)
        db.commit()
        logging.info(f'Admin ({admin}) created')
        
        
    except:
        logging.error(f'Error creating admin ({Exception})')
        db.rollback()
        
if __name__ == '__main__':
    create_admin()