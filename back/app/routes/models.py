from pydantic import BaseModel, EmailStr, field_validator, Field

class EmailSchema(BaseModel):
    email: EmailStr

    @field_validator("email")
    def validate_email(cls, v: str) -> str:
        v = v.lower()
        return v

class LoginSchema(EmailSchema):
    password: str

    @field_validator("password")
    def validate_email(cls, v: str) -> str:
        if len(v.strip()) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")
        return v

class RegisterUser(EmailSchema):
    password: str = Field(min_length=8)
    name: str
    
class ProductModel(BaseModel):
    name: str
    mark: str
    value: float = Field(gt=0.1)
    
    @field_validator("name", "mark")
    def validate_email(cls, v: str) -> str:
        if len(v.strip()) < 1:
            raise ValueError("name e mark devem ter mais de 1 caracter")
        return v

