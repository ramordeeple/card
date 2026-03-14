import asyncio
import logging

from sqlalchemy import select

from src.core.config import settings
from src.core.security.hashing import hash_password
from src.db.models.card import Card
from src.db.models.user import User
from src.db.session import SessionLocal
from src.domain.enums.user_role import UserRole

async def create_admin():
    async with SessionLocal() as db:
        try:
            result = await db.execute(
                select(User).where(User.role == UserRole.ADMIN)
            )
            admin_exists = result.scalar_one_or_none()

            if admin_exists:
                logging.info(f'Admin ({admin_exists.username}) already exists')
                return

            admin = User(
                username=settings.ADMIN,
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
                role=UserRole.ADMIN
            )

            db.add(admin)
            await db.commit()
            logging.info(f'Admin ({admin.username}) created successfully')

        except Exception as e:
            await db.rollback()
            logging.error(f'Error creating admin ({e})', exc_info=True)
            await db.rollback()

if __name__ == '__main__':
    asyncio.run(create_admin())