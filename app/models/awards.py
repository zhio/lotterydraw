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
class Award(BaseModel):
    id: Optional[int] = None
    userid : int
    username: str
    awardid: int
    awardname : str
    create_date: Optional[int] = None

    class Config:
        orm_mode = True

class Award2Man(BaseModel):
    pass  
# DB model

class Awards(Base):
    __tablename__ = 'awards'

    id = Column(INTEGER(64), primary_key=True, comment='编号')
    awardname = Column(String(100), comment='奖品名称')
    total = Column(INTEGER(11), comment='奖品总数')
    count = Column(INTEGER(11), comment='剩余数量')
    itemid = Column(INTEGER(11), ForeignKey('items.id'), comment='从属项目',)
    item = relationship("Items", backref="awards")
    create_date = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai")))
  

    @classmethod
    def add(cls, db: Session, data):
        db.add(data)
        db.commit()
        # db.refresh(data)

    @classmethod
    def get_by_id(cls, db: Session,id):
        data = db.query(cls).filter_by(id=id).first()

        return data

    @classmethod
    def get_by_name(cls, db: Session, name):
        data = db.query(cls).filter_by(name=name).first()

        return data

    @classmethod
    def update_one(cls, db: Session,id):
        award = db.query(cls).with_lockmode("update").get(id)
        award.count -=1
        db.commit()

    @classmethod
    def get_all_items_award(cls, db: Session, id):
        datas = db.query(cls).filter_by(itemid=id).all()
        for data in datas:
            for man in data.luckmans:
                pass
        return datas

    @classmethod
    def get_remaining(cls, db: Session, id):
        datas = db.query(cls).filter_by(itemid=id).all()
        return datas