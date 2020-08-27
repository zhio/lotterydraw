import redis
pool = redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
#pool = redis.ConnectionPool(host='localhost',port=6379, passwd='wksrong5678',decode_responses=True)


class MyRedis(object):
    def __init__(self):
        self.db = redis.Redis(connection_pool=pool)
    
    def set(self, key, value,ex = None):
        return self.db.set(key,value,ex)
    
    def get(self,key):
        return self.db.get(key)

    def hset(self,name,key,value):
        name = name + "_hash"
        return self.db.hset(name,key,value)

    def hget(self,name,key):
        name = name + "_hash"
        return self.db.hget(name,key)
    def hmset(self,name,mapping):
        name = name + "_hash"
        return self.db.hmset(name,mapping)
    
    def hgetall(self,name):
        name = name + "_hash"
        return self.db.hgetall(name)
    
    #判断是否存在
    def hexists(self,name,key):
        name = name + "_hash"
        return self.db.hexists(name,key)

    def delete(self,name):
        name = name + "_hash"
        return self.db.delete(name)

    #自增自减
    def hincrby(self, name, key, amout=1):
        name = name + "_hash"
        return self.db.hincrby(name,key,amout)
    
    #删除list并返回
    def lpop(self, name):
        return self.db.lpop(name)

class RedisQueue(object):
    def __init__(self, name, namespace="queue"):
        self.__db = redis.Redis(connection_pool=pool)
        self.key = f"{namespace}:{name}"

    
    def qsize(self):
        return self.__db.llen(self.key)

    def lpop(self):
        return self.__db.lpop(self.key)
    def put(self, item):
        self.__db.rpush(self.key, item)
    
    def get_wait(self, timeout=None):
        item = self.__db.blpop(self.key, timeout=timeout)
        return item
    
    def get_nowait(self):
        item = self.__db.lpop(self.key)
        return item
    
# a = RedisQueue('ps')
# for i in range(10):
#     a.put(i)
#     print(a.qsize())
# print(a.get_wait())