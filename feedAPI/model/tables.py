from datetime import datetime
from typing import Optional
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    def as_dict(self):
        # Return itself as a dict
        return {c.name: getattr(self, c.name)
                for c in self.__table__.columns}



class Feedback(Base):
    # Declarative description of the feedback table
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(15))
    text: Mapped[Optional[str]] = mapped_column(String(250))
    grade: Mapped[int] = mapped_column()
    datetime: Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self):
        # Represents a feedback as a string for logging
        return '<Feedback(id={self.id} ip={self.source} datetime={self.datetime})>'.format(self=self)


class Comment(Base):
    # Declarative description of comments table
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[int] = mapped_column(ForeignKey("feedbacks.id"))
    source: Mapped[str] = mapped_column(String(15))
    text: Mapped[Optional[str]] = mapped_column(String(250))
    score: Mapped[int] = mapped_column()
    datetime: Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self):
        # Represents a comment as a string for logging
        return '<Comment(id={self.id} source={self.ip} target={self.target} datetime={self.datetime})>'.format(self=self)


class Reaction(Base):
    # Declarative description of reactions table
    __tablename__ = "reactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[int] = mapped_column(ForeignKey("comments.id"))
    source: Mapped[str] = mapped_column(String(15))
    value: Mapped[int] = mapped_column() #+1 -1 or 0
    datetime: Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self):
        # Represents a reaction as a string for logging
        return '<Reaction(id={self.id} source={self.ip} target={self.target} datetime={self.datetime})>'.format(self=self)
