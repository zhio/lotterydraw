from sqlalchemy import Column, DateTime, String, text, Float
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import Session, relationship,backref
from sqlalchemy import ForeignKey
from app.database import Base
from pydantic import BaseModel
from typing import Optional
import datetime
import pytz

class Items(Base):
    __tablename__ = "items"

    id = Column(INTEGER(64),primary_key=True,comment="编号")
    name = Column(String(100), comment='项目名称')
    total = Column(INTEGER(11), comment='奖品总数')
    lotterykey = Column(Float ,default=0.00, comment='综合中奖率')
    create_date = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai")))
    # create_date = Column(DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    @classmethod
    def add(cls, db: Session, data):
        db.add(data)
        db.commit()
        db.refresh(data)
        

    @classmethod
    def get_by_id(cls, db: Session, id):
        data = db.query(cls).filter_by(id=id).first()
        return data

    @classmethod
    def get_by_name(cls, db: Session, name):
        data = db.query(cls).filter_by(name=name).first()
    
        return data

    @classmethod
    def changekey(cls, db: Session, id,key):
        data = db.query(cls).filter_by(id=id).update({"lotterykey": key })
        db.commit()
        return data

    
    
