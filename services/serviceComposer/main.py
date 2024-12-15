import logging
import requests
from fastapi import FastAPI, HTTPException

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


class ResponseModel(BaseModel):
    decision: str
    description: str


class LoanRequest(BaseModel):
    text: str


logging.basicConfig(level=logging.DEBUG)
API_HOST = "127.0.0.1"
API_NAME = "Morgage Loan Application"
API_PORT = 8000
API_DESCRIPTION = f"A simple API for {API_NAME}"
text_mining_port = 8004
solvability_check_port = 8001
properity_evaluation_port = 8002
decision_approval_port = 8003

app = FastAPI(title=API_NAME, description=API_DESCRIPTION)


@app.get("/")
def read_root():
    return {
        "API": API_NAME,
        "Description": API_DESCRIPTION,
        "Port": API_PORT,
    }


@app.post("/loan-demand")
def loanDemand(request: LoanRequest) -> ResponseModel:
    try:
        text_mining_response = requests.post(
            f"http://{API_HOST}:{text_mining_port}/extract",
            json={"text": request.text},
        )

        solvability_check_response = requests.post(
            f"http://{API_HOST}:{solvability_check_port}/verify-credit-score",
            json=text_mining_response.json(),
        )
        properity_evaluation_response = requests.post(
            f"http://{API_HOST}:{properity_evaluation_port}/properity-evaluation",
            json=solvability_check_response.json(),
        )
        decision_approval_response = requests.post(
            f"http://{API_HOST}:{decision_approval_port}/loan-decision",
            json=properity_evaluation_response.json(),
        )
        return decision_approval_response.json()
    except Exception as e:
        logging.error(f"Error during service call: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error during service call: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=API_HOST, port=API_PORT)
