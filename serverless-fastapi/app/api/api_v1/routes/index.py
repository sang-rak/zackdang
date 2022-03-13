from datetime import datetime

from fastapi import APIRouter
from starlette.responses import Response
from starlette.requests import Request
from inspect import currentframe as frame

router = APIRouter()


@router.get("/")
async def index():
    """
    ELB 상태 체크용 API
    :return:
    """
    current_time = datetime.utcnow()
    return Response(f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")


@router.get("/test")
async def test(request: Request):
    """
    ELB 상태 체크용 API
    a = 1/0
    :return:
    """
    print("state.user", request.state.user)
    try:
        a = 1/0
    # 핸들링 되지않을 에러가있을경우 사용
    except Exception as e:
        raise e
    current_time = datetime.utcnow()
    return Response(f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")

