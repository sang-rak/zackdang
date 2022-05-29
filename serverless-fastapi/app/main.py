
import os
from dataclasses import asdict
from typing import Optional, List

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from app.api.api_v1.api import router as api_router
from app.api.api_v1.database.conn import db
from app.api.api_v1.common.config import conf
from app.api.api_v1.middlewares.token_validator import access_control
from app.api.api_v1.middlewares.trusted_hosts import TrustedHostMiddleware

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from mangum import Mangum
"""
앱 함수 실행
:return:
"""
c = conf()
app = FastAPI(
    title="serverless-fastapi",
    version=0.1,
    # 운영에서는 활성화
    # root_path="/dev"

    ) 
conf_dict = asdict(c)
db.init_app(app, **conf_dict)

# 미들웨어 정의

app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control) # token_validator.py class 호출
app.add_middleware(
    CORSMiddleware,
    allow_origins=conf().ALLOW_SITE,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=["/health"])

@app.get("/")
async def root():
    return {"message`": "Hello World!"}

app.include_router(api_router, prefix="/v1")
handler = Mangum(app)


html = ""
with open('app/templates/index.html', 'r') as f:
    html = f.read()

@app.get("/roomid/{room_id}")
async def get():
    return HTMLResponse(html)

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()


@app.websocket("/roomid/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await manager.broadcast(f"Client {client_id}: {data}")