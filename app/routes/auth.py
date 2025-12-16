from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Diz ao Swagger que existe autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint de login (didático).
    Apenas demonstra autenticação no Swagger.
    """
    return {
        "access_token": "token-fake-apresentacao",
        "token_type": "bearer"
    }
