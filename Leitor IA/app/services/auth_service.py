from fastapi import HTTPException, status
from app.repositories.specific_repositories import UserRepository
from app.schemas.all_schemas import UserRegister, UserLogin, TokenResponse
from app.models.all_models import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, schema: UserRegister) -> User:
        if self.user_repo.get_by_email(schema.email):
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        user = User(email=schema.email, hashed_password=get_password_hash(schema.password))
        return self.user_repo.add(user)

    def authenticate_user(self, schema: UserLogin) -> TokenResponse:
        user = self.user_repo.get_by_email(schema.email)
        if not user or not verify_password(schema.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Credenciais incorretas.")
        return TokenResponse(access_token=create_access_token({"sub": str(user.id)}), refresh_token=create_refresh_token({"sub": str(user.id)}))

    def refresh_session(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or not payload.get("refresh"):
            raise HTTPException(status_code=401, detail="Token inválido.")
        uid = payload.get("sub")
        return TokenResponse(access_token=create_access_token({"sub": uid}), refresh_token=create_refresh_token({"sub": uid}))