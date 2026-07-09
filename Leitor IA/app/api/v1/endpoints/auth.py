from fastapi import APIRouter, Depends
from app.schemas.all_schemas import UserRegister, UserLogin, TokenResponse, TokenRefreshRequest
from app.services.auth_service import AuthService
from app.api.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", status_code=201)
def register(data: UserRegister, service: AuthService = Depends(get_auth_service)):
    service.register_user(data)
    return {"message": "Registrado com sucesso."}

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, service: AuthService = Depends(get_auth_service)):
    return service.authenticate_user(data)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: TokenRefreshRequest, service: AuthService = Depends(get_auth_service)):
    return service.refresh_session(data.refresh_token)