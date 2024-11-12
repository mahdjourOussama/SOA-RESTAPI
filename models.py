from pydantic import BaseModel
from typing import Optional


class InformationsModel(BaseModel):
    address: str
    email: str
    phone_number: str
    loan_amount: str
    loan_duration: str
    property_description: str
    monthly_income: str
    monthly_expenses: str
    client_name: str
    credit_score: Optional[float] = None
    properity_value: Optional[float] = None
