from ..cache import RedisQueue, MyRedis
import random
from ..cache import MyRedis
from app.util import common
def goodluck_creat(rqname,item):
    """
    抽奖算法
    """
    try:
        myredis = MyRedis()
        rq = RedisQueue(rqname)
        lucklist =[]
        luckdict = {}
        for ward in item.awards:
            luckdict[ward.id] = ward.total
            for i in range(ward.total):
                lucklist.append(ward.id)
        random.shuffle(lucklist)
        for luck in lucklist:
            rq.put(luck)
        myredis.hmset(str(item.id),luckdict)
        myredis.set('lotterykey'+str(item.id),item.lotterykey)
    except Exception as e:
        rsp = common.falseReturn(msg="抽奖创建失败")
        return rsp
