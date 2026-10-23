from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Not(Base):
    __tablename__ = "notlar"

    id: Mapped[int] = mapped_column(primary_key=True)
    baslik: Mapped[str] = mapped_column(String(200))
    icerik: Mapped[str] = mapped_column(Text)