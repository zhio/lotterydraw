from typing import Optional,List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from redisqueue import RedisQueue,MyRedis
import random

class Award(BaseModel):
    name: str
    count: int

class Item(BaseModel):
    luckname: str = Field(...,title="抽奖规则名称",max_lenght = 300)
    total: int = Field(...,title="抽奖总人数",gt=0)
    award: Optional[List[Award]] = Field(None,title="奖品列表")
    other: str = Field(...,title="参与奖或者未中奖")
app = FastAPI()

class ResSuccess(BaseModel):
    ret: int = 0
    data

@app.get('/')
def read_root():
    return {"Hello":"World"}

@app.post(
    '/delect', 
    tags = ["抽奖接口"],
    summary = "删除抽奖规则"
    )
def delect(name:str):
    rq = RedisQueue(name)
    if rq.qsize:
        rq.lpop(name)
    return {
        'ret':0,
        'msg':"删除成功"
    }

@app.post(
    '/creat',
    tags = ['抽奖接口'],
    summary="创建抽奖规则"
)
def creat(item: Item):
    """
    通过该接口可以创建一个抽奖规则
    """
    myredis = MyRedis()
    rq = RedisQueue(item.luckname)
    print("ok")
    if rq.qsize():
        return {
            "ret":500,
            "msg":"该抽奖已经存在，请删除后重试"
        }
    result = {"ret":0, "item":item}
    awardlist = item.award
    lucklist =[]
    luckdict = {}
    for ward in awardlist:
        luckdict[ward.name] = ward.count
        for i in range(ward.count):
            lucklist.append(ward.name)
    othercount = item.total - len(lucklist)

    if othercount:
        luckdict[item.other] = othercount
        others = [item.other] * othercount
    
    lucklist = lucklist + others
    random.shuffle(lucklist)
    print(lucklist)
    for luck in lucklist:
        rq.put(luck)
    
    myredis.hmset(item.luckname,luckdict)

    result = {
        'ret': 0,
        'msg': "succses"
    }
    return result

@app.get('/luck', tags = ["抽奖接口"], summary="抽奖接口")
def luck(id: int,luckname: str):
    """
    开始抽奖
    """
    rd = RedisQueue(luckname)
    myredis = MyRedis()
    winner = luckname+"_winner"
    if myredis.hexists(winner,id):
        return {
            "ret":0,
            "msg":"您已经抽过了，不能再抽了"
        }
    award = rd.get_nowait()
    if award:
        myredis.hset(winner,id,award)
        myredis.hincrby(luckname,award,-1)
        
        result = {
            "ret":0,
            'data':{
                "flag":1,
                "msg":"恭喜你中奖了",
                "award":award
            }
        }
    else:
          result = {
            "ret":0,
            'data':{
                "flag":0,
                "msg":"奖抽完了",
            }
        }
    
    return result

@app.get('/luckman',tags = ["抽奖接口"],summary="查看中奖名单")
def luckman(luckname: str):
    myredis = MyRedis()
    winner = luckname + "_winner"
    winnerlist = myredis.hgetall(winner)
    print(winnerlist)
    return {
        "ret":0,
        "data":winnerlist
    }

@app.get('/remaining',tags = ["抽奖接口"],summary="查看剩余奖品列表")
def Remaining(luckname: str):
    myredis = MyRedis()
    remainlist = myredis.hgetall(luckname)
    print(remainlist)
    return {
        "ret":0,
        "data":remainlist
    }
