from sqlalchemy import Column, VARCHAR, Enum, Boolean
from .basemodel import BaseModel, Base


class Users(BaseModel, Base):
    __tablename__ = 'users'

    email = Column(VARCHAR(255), unique=True, nullable=False)
    password_hash = Column(VARCHAR(255), nullable=False)

    status = Column(
        Enum('ACTIVE', 'INACTIVE', 'BANNED', name='user_status_enum'),
        nullable=False,
        default='INACTIVE'
    )

    is_verified = Column(Boolean, default=False, nullable=False)

    role = Column(
        Enum("SUPER ADMIN", "USER", name='user_role_enum'),
        default="USER",
        nullable=False
    )
