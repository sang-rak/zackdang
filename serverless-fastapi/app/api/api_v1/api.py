from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader


from app.api.api_v1.routes import index, auth, users, services

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

router = APIRouter()

router.include_router(index.router)
router.include_router(auth.router, tags=["Authentication"])
router.include_router(services.router, tags=["Services"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)]) # 토큰 검사가 필요한경우 사용
router.include_router(users.router, tags=["Users"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)]) 

