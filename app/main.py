import time 
import logging
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from .routers import users, lucks, draws
from app.auth.auths import Auth 
from .database import Base, engine
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

logger = logging.getLogger('fastapi')



app.include_router(users.router)
app.include_router(lucks.router)
app.include_router(
    draws.router,
    prefix="/draws",
    tags = ['draws'],
)

# @app.middleware("http")
# async def process_authorization(request: Request, call_next):
#     """
#         在这个函数里统一对访问做权限token校验。
#         1、如果是用户注册、登陆，那么不做token校验，由路径操作函数具体验证
#         2、如果是其他操作，则需要从header或者cookie中取出token信息，解析出内容
#             然后对用户身份进行验证，如果用户不存在则直接返回
#             如果用户存在则将用户信息附加到request中，这样在后续的路径操作函数中可以直接使用。
#     """
#     start_time = time.time()

#     if request.url.path == "/login" or request.url.path == '/register' or request.url.path == "/luck":
#         logger.info(' no jwt verify.')
#     else:
#         logger.info("jwt verify.")

#         result = Auth.identifyAll(request)
#         if result['status'] and result['data']:
#             user = result['data']['user']

#             logger.info(f"jwt verify success. user:{user.username}")

#             request.state.user = user
#         else:
#             return JSONResponse(content=result)
    
#     response = await call_next(request)

#     process_time = time.time() - start_time
#     response.headers['X-Process-Time'] = str(process_time)
#     return response


