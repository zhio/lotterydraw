from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import Session, relationship,backref
from sqlalchemy import ForeignKey
from app.database import Base
from pydantic import BaseModel
from typing import Optional
import datetime
import pytz

# Pydantic model
class Luckman(BaseModel):
    id: Optional[int] = None
    userid : int
    username: str
    awardid: int
    awardname : str
    create_date: Optional[int] = None

    class Config:
        orm_mode = True


# DB model
class Luckmans(Base):
    __tablename__ = 'luckmans'

    id = Column(INTEGER(64), primary_key=True, comment='中奖编号')
    user_id = Column(INTEGER(11), comment='用户ID')
    username = Column(String(100), comment='用户名称')
    winornot = Column(INTEGER(1), comment='是否中奖')
    item_id = Column(INTEGER(11), comment="项目id")
    award_id = Column(INTEGER(11),  ForeignKey('awards.id'), server_default=text("'0'"),comment='奖品id')
    award = relationship("Awards", backref="luckmans")
    redeem = Column(INTEGER(1), server_default=text("'0'"), comment='是否兑换')
    redeem_time = Column(DateTime,comment='兑换时间', nullable=False, default=datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai")), onupdate=datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai")))
    create_date = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai")))
  
    
    @classmethod
    def add(cls, db: Session, data):
        db.add(data)
        db.commit()
        # db.refresh(data)

    @classmethod
    def get_by_user_id(cls, db: Session, user_id):
        data = db.query(cls).filter_by(id=user_id).first()
        return data

    @classmethod
    def get_by_username(cls, db: Session, username):
        data = db.query(cls).filter_by(username=username).first()
        return data

    @classmethod
    def get_by_itemid(cls, db: Session, itemid):
        data = db.query(cls).filter_by(item_id=itemid).first()
        return data
    @classmethod
    def edit_status(cls, db: Session, id):
        data = db.query(cls).filter_by(id=id).update({"redeem": 1 })
        db.commit()
        return data

    @classmethod
    def get_user_winornot(cls,db: Session,userid):
        data = db.query(cls).filter_by(user_id=userid,winornot=1).all()
        return data
