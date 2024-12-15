import logging
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
API_NAME = "Client Loan Deciecion Service"
API_PORT = 8003
API_DESCRIPTION = f"A simple API for {API_NAME}"

app = FastAPI(title=API_NAME, description=API_DESCRIPTION)


@app.get("/")
def read_root():
    return {
        "API": API_NAME,
        "Description": API_DESCRIPTION,
        "Port": API_PORT,
    }


@app.post("/loan-decision")
def evaluationScore(LoanInformation: InformationsModel) -> ResponseModel:
    try:
        logging.debug(f"Evaluating {LoanInformation}")

        montant_pret = float(LoanInformation.loan_amount.replace("EUR", "").strip())
        duree = int(LoanInformation.loan_duration.replace("ans", "").strip())
        revenu_mensuel = float(
            LoanInformation.monthly_income.replace("EUR", "").strip()
        )
        depense = float(LoanInformation.monthly_expenses.replace("EUR", "").strip())
        score = (
            LoanInformation.credit_score
            if LoanInformation.properity_value is not None
            else 0
        )
        properity_score = (
            LoanInformation.properity_value * duree * 12
            if LoanInformation.properity_value is not None
            else 0
        )
        # Calculer le remboursement et le taux d'endettement
        taux_interet = 0.03
        remboursement = (montant_pret * taux_interet * (1 + taux_interet) ** duree) / (
            (1 + taux_interet) ** (duree - 1)
        )
        taux_endettement = (remboursement / revenu_mensuel) * 100

        # Évaluer la décision
        if (
            remboursement + depense < revenu_mensuel
            and score > 50
            and taux_endettement < 40
            and properity_score > montant_pret
        ):
            description = (
                "Vous correspondez à tous les critères. Nous acceptons votre crédit."
            )
            response = ResponseModel(decision="Approved", description=description)
        else:
            description = "Nous ne pouvons pas accepter le crédit car "
            if remboursement + depense >= revenu_mensuel:
                description += "vos dépenses mensuelles sont trop élevées."
            if score <= 50:
                description += " Votre score de crédit est trop faible."
            if taux_endettement >= 40:
                description += " Le ratio de remboursement est trop risqué."
            if taux_endettement <= montant_pret:
                description += " la valeur de la propriété est inférieure au prêt demandé est trop risqué."
            response = ResponseModel(decision="Rejected", description=description)

        return response

    except Exception as e:
        logging.error(f"error: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de conversion JSON : {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=API_HOST, port=API_PORT)
