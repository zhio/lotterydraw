import datetime
from app.util import common
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auths import Auth
from app.models.items import Items
from app.models.awards import Awards
from app.models.luckmans import Luckmans
from pydantic import BaseModel,Field
from typing import Optional,List
from ..cache import MyRedis
from app.util.goodluck import goodluck_creat
from fastapi.encoders import jsonable_encoder

router = APIRouter()
myredis = MyRedis()
write2sqltime = datetime.datetime.now() + datetime.timedelta()

class Award(BaseModel):
    name: str
    count: int

class Item(BaseModel):
    luckname: str = Field(...,title="抽奖规则名称",max_lenght = 300)
    total: int = Field(...,title="抽奖总人数",gt=0)
    award: Optional[List[Award]] = Field(None,title="奖品列表")
    lotterykey: float = Field(...,title="中奖率")

 
@router.post(
    '/creat',
    summary="创建抽奖规则"
)
async def creat(datas: Item, db: Session = Depends(get_db)):
    """
    通过该接口可以创建一个抽奖规则
    """
    item_id = 0
    olddata = Items.get_by_name(db,datas.luckname)
    if olddata:
        json_compatible_item_data = jsonable_encoder(olddata)
        rsp = common.falseReturn(data =json_compatible_item_data, msg='项目已存在')
        return rsp
    try:
        items = Items(name=datas.luckname,total=datas.total,lotterykey=datas.lotterykey)
        awardlist = [Awards(awardname=data.name,total=data.count,count=data.count) for data in datas.award]
        items.awards = awardlist
        Items.add(db,items)
        item_id = items.id
    except Exception as e:
        raise e
    if not item_id:
        rsp = common.falseReturn(msg='创建抽奖失败')
        return rsp
    rqname = "goodluck" + str(items.id)
    #抽奖算法
    goodluck_creat(rqname,items)
    json_compatible_item_data = jsonable_encoder(items)
    rsp = common.trueReturn(data=json_compatible_item_data,msg="创建抽奖成功")
    return rsp

@router.get('/luckman',tags = ["draws"],summary="查看中奖名单")
def luckman(items_id: int, db: Session = Depends(get_db)):
    result = Awards.get_all_items_award(db,items_id)
    json_compatible_item_data = jsonable_encoder(result)
    rsp = common.trueReturn(data=json_compatible_item_data)
    return rsp


@router.get('/remain',tags = ["draws"],summary="查看剩余奖品")
def Remaining(items_id: int, db: Session = Depends(get_db)):
    result = Awards.get_remaining(db,items_id)
    json_compatible_item_data = jsonable_encoder(result)
    rsp = common.trueReturn(data=json_compatible_item_data)
    return rsp
  
@router.get('/edit')
def edit(luckmanid:int, db:Session = Depends(get_db)):
    affect = Luckmans.edit_status(db,luckmanid)
    if affect:
        rsp = common.trueReturn(msg="更新成功，已标记完成")
    else:
        rsp = common.falseReturn(msg="更新失败，请稍后重试")
    return rsp

@router.get('/changekey')
def edit(items_id:int, newkey: float, db:Session = Depends(get_db)): 
    myredis.set('lotterykey'+str(items_id))
    Items.changekey(db,items_id,newkey)
    rsp = common.falseReturn(msg="更新KEY成功")
    return rsp