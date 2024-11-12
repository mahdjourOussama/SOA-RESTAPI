import logging
import requests
from fastapi import FastAPI, HTTPException
from models import ResponseModel, LoanRequest
from TextMiningService import API_HOST as text_mining_host, API_PORT as text_mining_port
from SolvapilityVerificationService import (
    API_HOST as solvability_check_host,
    API_PORT as solvability_check_port,
)
from ProperityEvaluationService import (
    API_HOST as properity_evaluation_host,
    API_PORT as properity_evaluation_port,
)
from DecisionApprovalService import (
    API_HOST as decision_approval_host,
    API_PORT as decision_approval_port,
)

logging.basicConfig(level=logging.DEBUG)
API_HOST = "127.0.0.1"
API_NAME = "Morgage Loan Application"
API_PORT = 8000
API_DESCRIPTION = f"A simple API for {API_NAME}"

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
            f"http://{text_mining_host}:{text_mining_port}/extract",
            json={"text": request.text},
        )

        solvability_check_response = requests.post(
            f"http://{solvability_check_host}:{solvability_check_port}/verify-credit-score",
            json=text_mining_response.json(),
        )
        properity_evaluation_response = requests.post(
            f"http://{properity_evaluation_host}:{properity_evaluation_port}/properity-evaluation",
            json=solvability_check_response.json(),
        )
        decision_approval_response = requests.post(
            f"http://{decision_approval_host}:{decision_approval_port}/loan-decision",
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
