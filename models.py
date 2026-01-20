from pydantic import BaseModel, Field

class CreateAccount(BaseModel):
    owner: str = Field(..., example="Alice")
    initial_deposit: float = Field(0.0, ge=0)

class Amount(BaseModel):
    amount: float = Field(..., gt=0)