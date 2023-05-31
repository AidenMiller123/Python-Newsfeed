from datetime import datetime
from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import select, func
from .Vote import Vote

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    post_url = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user = relationship('User')
    comments = relationship('Comment', cascade='all,delete')
    votes = relationship('Vote', cascade='all,delete')
    vote_count = Column(Integer, default=0)

    def __init__(self, title, post_url, user_id):
        self.title = title
        self.post_url = post_url
        self.user_id = user_id
        self.vote_count = 0

    def update_vote_count(self, session):
        self.vote_count = session.query(func.count(Vote.id)).filter(Vote.post_id == self.id).scalar()
        session.commit()
