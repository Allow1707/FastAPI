import datetime
import uuid
from sqlalchemy import BigInteger, DateTime, Boolean, func, String
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


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    uuid: Mapped[str] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True,
                                      nullable=False, index=True)
    name: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(String(10), nullable=False, default='guest')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(),
                                                          onupdate=func.now())
