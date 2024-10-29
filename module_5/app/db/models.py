import datetime
import uuid
from enum import Enum as PyEnum
from sqlalchemy import BigInteger, DateTime, Boolean, func, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base


class ToDo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    uuid: Mapped[str] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True,
                                      nullable=False)  # Новое поле uuid
    description: Mapped[str] = mapped_column()  # Явно указываем mapped_column() для строки
    completed: Mapped[bool] = mapped_column(Boolean, default=False)  # Добавляем тип Boolean для столбца completed
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

class UserRole(PyEnum):
    """Создания enum типа для роли пользователя"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    uuid: Mapped[str] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True,
                                      nullable=False, index=True)
    name: Mapped[str] = mapped_column()
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.GUEST)