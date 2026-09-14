from pydantic import EmailStr, ConfigDict, BaseModel

from schemas.base_model import CamelCaseBaseModel

class UserRegister(CamelCaseBaseModel):
    username:str
    email:str
    password: str

class UserLogin(CamelCaseBaseModel):
    email: str 
    password: str

class ForgotPassword(CamelCaseBaseModel):
    email: EmailStr

class ResetPassword(CamelCaseBaseModel):
    token: str
    password: str

class SendVerificationCode(CamelCaseBaseModel):
    email: EmailStr

class AccountVerification(CamelCaseBaseModel):
    email: EmailStr
    code: str

class UserRegisterOut(CamelCaseBaseModel):
    id: int
    email: EmailStr
    is_email_verified: bool

    model_config = ConfigDict(from_attributes=True)

#
class UserLoginOut(BaseModel):
    access_token: str = ""
    expires_in: int = -1
    token_type: str = "bearer"

    model_config = ConfigDict(validate_default=True)


