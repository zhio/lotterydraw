import datetime
from app.util import common
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auths import Auth
from app.models.items import Items
from app.models.awards import Awards
from app.models.luckmans import Luckmans
from ..cache import RedisQueue,MyRedis
from fastapi.encoders import jsonable_encoder
import random
import numpy as np

router = APIRouter()
myredis = MyRedis()
write2sqltime = datetime.datetime.now() + datetime.timedelta()

@router.get('/luck', tags = ["draws"], summary="抽奖接口")
def luck(userid: int, username: str, itemsid: int, db: Session = Depends(get_db)):
    """
    开始抽奖
    userid: 用户id
    username: 用户昵称
    itemsid: 奖池id
    """
    item_redis_key = "goodluck" + str(itemsid)
    rq = RedisQueue(item_redis_key) 
    winner_redis_key ="WINNER_" + str(itemsid)

    if myredis.hexists(winner_redis_key,userid):
        rsp = common.trueReturn(msg='您已经抽过了，不能再抽了')
        return rsp

    lotterykey = myredis.get('lotterykey'+str(itemsid))
    print(lotterykey)
    if lotterykey != 1:
        if not lotteryfunc(lotterykey):
            rsp = common.trueReturn(msg="很遗憾你没有中奖")
            myredis.hset(winner_redis_key,userid,0)
            luckman = Luckmans(user_id=userid,username=username,winornot=0,item_id=itemsid)
            Luckmans.add(db,luckman)
            return rsp

    award = rq.get_nowait()
    
    if award is not None:
        #缓存到redis
        myredis.hset(winner_redis_key,userid,award)
        myredis.hincrby(item_redis_key,award,-1)
        count = myredis.hget(item_redis_key,award)
        #查询当前奖品剩余数量
        luckman = Luckmans(user_id=userid,username=username,winornot=1,item_id=itemsid,award_id=award)
        Luckmans.add(db,luckman)
        Awards.update_one(db,luckman.award_id)
        awardname = Awards.get_by_id(db,luckman.award_id).awardname
        # #定时更新mysql
        
        # if write2sqltime >= datetime.datetime.now():
        #     write2sql(userid,username,award)
        #     write2sqltime = datetime.datetime.now() + datetime.timedelta(minutes=5)
        data = {
            'award':awardname,
            'awardid':luckman.award_id
        }
        rsp = common.trueReturn(data, '恭喜你中奖啦')
    else:
        rsp = common.falseReturn(msg="很遗憾，没有奖品了")
    return rsp

@router.get('/luckbmf', tags = ["draws"], summary="抽奖BFM接口")
def luckbmf(userid: int, username: str, itemsid: int, db: Session = Depends(get_db)):
    """
    开始抽奖
    userid: 用户id
    username: 用户昵称
    itemsid: 奖池id
    """
    item_redis_key = "goodluck" + str(itemsid)
    rq = RedisQueue(item_redis_key) 
    winner_redis_key ="WINNER_BMF"

    if myredis.hexists(winner_redis_key,userid):
        rsp = common.trueReturn(msg='您已经抽过了，不能再抽了')
        return rsp

    lotterykey = myredis.get('lotterykey'+str(itemsid))
    if lotterykey != 1:
        if not lotteryfunc(lotterykey):
            rsp = common.trueReturn(msg="很遗憾你没有中奖")
            luckman = Luckmans(user_id=userid,username=username,winornot=0,item_id=itemsid)
            Luckmans.add(db,luckman)
            return rsp

    award = rq.get_nowait()
    
    if award is not None:
        #缓存到redis
        myredis.hset(winner_redis_key,userid,award)
        myredis.hincrby(item_redis_key,award,-1)
        count = myredis.hget(item_redis_key,award)
        #查询当前奖品剩余数量
        luckman = Luckmans(user_id=userid,username=username,winornot=1,item_id=itemsid,award_id=award)
        Luckmans.add(db,luckman)
        Awards.update_one(db,luckman.award_id)
        awardname = Awards.get_by_id(db,luckman.award_id).awardname
        data = {
            'award':awardname,
            'awardid':luckman.award_id
        }
        rsp = common.trueReturn(data, '恭喜你中奖啦')
    else:
        rsp = common.falseReturn(msg="很遗憾，没有奖品了")
    return rsp

@router.get('/mybmf', tags = ["draws"], summary="查看用户是否中奖")
def mybmf(userid: int,db: Session = Depends(get_db)):
    win_or_not = Luckmans.get_user_winornot(db,userid)
    if win_or_not:
        json_compatible_item_data = jsonable_encoder(win_or_not)
        rsp = common.trueReturn(data=json_compatible_item_data,msg="恭喜你中奖啦")
    else:
        rsp = common.trueReturn(msg="很遗憾你还没有中奖")
    return rsp

#综合中奖率
def lotteryfunc(lotterykey):
    lotterykey = float(lotterykey)
    lottery = np.random.choice(2,1,p=[1-lotterykey,lotterykey])[0]
    return lottery

