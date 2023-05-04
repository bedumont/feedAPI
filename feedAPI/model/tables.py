from datetime import datetime
from typing import Optional
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func, select, update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    """ Base table
    """
    def as_dict(self):
        """ Return table entry as dict
        Used to jsonify the tables
        """
        return {c.name: getattr(self, c.name)
                for c in self.__table__.columns}

    def __init__(self, data=None):
        # Init from dict {columname: value}
        """ Init an object instance from data in a dict
        If no data provided create an instance with no data
        """
        if data is not None:
            for key in data:
                if key in self.__table__.columns:
                    setattr(self, key, data[key]) # Prevent from :

class Feedback(Base):
    """ Declarative description of the feedbacks table
    Table has 6 fields:
        id [int]: the primary key (assumed unique)
        source [str]: the ip adress of the source
        text [str, optional]: the text of the feedback
        grade [int]: the grave of the feedback
        score [int]: the sum of all upvotes and downvotes of the feedback
        datetime [datetime]: the timestamp of when the feedback was sent (client side)
    Inherit from Base
    """
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(15))
    text: Mapped[Optional[str]] = mapped_column(String(250))
    grade: Mapped[int] = mapped_column()
    score: Mapped[int] = mapped_column(default=1)
    datetime: Mapped[datetime]

    def __repr__(self):
        """ Represents a feedback as a string for logging
        """
        return '<Feedback(id={self.id} source={self.source} datetime={self.datetime})>'.format(self=self)

    def compute_score(session):
        """ Update the score of all the feedbacks that were affected by reactions.
        Should be run asynchronuously (for example by a cron job) to provide 
        eventual consistency.
        """
        subq = (
                select(1+func.sum(Reaction.value).label("total"))
                .where(Reaction.fb_id==Feedback.id)
                .group_by(Reaction.fb_id)
                .scalar_subquery()
                )

        exist_subq = (
                select(Feedback.id)
                .where(Reaction.fb_id == Feedback.id)
                .exists()
                )

        stmt = (
                update(Feedback)
                .values(score=subq)
                .where(exist_subq)
                )
        session.execute(stmt)
        session.commit()


class Comment(Base):
    """ Declarative description of the comments table
    Table has 6 fields:
        id [int]: the primary key (assumed unique)
        target [int]: the id of the feedback the entry is related to (ForeignKey)
        source [str]: the ip adress of the source
        text [str, optional]: the text of the comment
        score [int]: the sum of all upvotes and downvotes of the comment
        datetime [datetime]: the timestamp of when the comment was sent (client side)
    Inherit from Base
    """
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[int] = mapped_column(ForeignKey("feedbacks.id"))
    source: Mapped[str] = mapped_column(String(15))
    text: Mapped[Optional[str]] = mapped_column(String(250))
    score: Mapped[int] = mapped_column(default=1)
    datetime: Mapped[datetime]

    def __repr__(self):
        """ Represents a comment as a string for logging
        """
        return '<Comment(id={self.id} source={self.source} target={self.target} datetime={self.datetime})>'.format(self=self)

    def compute_score(session):
        """ Update the score of all the comments that were affected by reactions.
        Should be run asynchronuously (for example by a cron job) to provide
        eventual consistency.
        """
        subq = (
                select(func.sum(Reaction.value).label("total"))
                .where(Reaction.cmt_id==Comment.id)
                .group_by(Reaction.cmt_id)
                .scalar_subquery()
                )

        exist_subq = (
                select(Comment.id)
                .where(Reaction.cmt_id == Comment.id)
                .exists()
                )

        stmt = (
                update(Comment)
                .values(score=subq)
                .where(exist_subq)
                )
        session.execute(stmt)
        session.commit()


class Reaction(Base):
    """ Declarative description of the reactions table
    Table has 6 fields:
        id [int]: the primary key (assumed unique)
        fb_id [int]: the id of the feedback the entry is related to (ForeignKey)
            Null if the reaction is not related to a feedback
        cmt_id [int]: the id of the comment the entry is related to (ForeignKey)
            Null if the reaction is not related to a comment
        source [str]: the ip adress of the source
        value [int]: the value of the reaction (+1 or -1)
        datetime [datetime]: the timestamp of when the reaction was sent (client side)
    Inherit from Base
    """
    __tablename__ = "reactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    fb_id: Mapped[Optional[int]] = mapped_column(ForeignKey("feedbacks.id"))
    cmt_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comments.id"))
    source: Mapped[str] = mapped_column(String(15))
    value: Mapped[int] = mapped_column()  # +1 -1 or 0
    datetime: Mapped[datetime]

    feedback: Mapped["Feedback"] = relationship()
    comment: Mapped["Comment"] = relationship()

    def __repr__(self):
        """ Represents a reaction as a string for logging
        """
        return '<Reaction to feedback(id={self.id} source={self.source} fb_id={self.fb_id} cmt_id={self.cmt_id} datetime={self.datetime})>'.format(self=self)
