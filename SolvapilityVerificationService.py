import logging
import json
from fastapi import FastAPI, HTTPException
from models import InformationsModel

logging.basicConfig(level=logging.DEBUG)
API_HOST = "127.0.0.1"
API_NAME = "Client Solvablity Checking Service"
API_PORT = 8001
API_DESCRIPTION = f"A simple API for {API_NAME}"

app = FastAPI(title=API_NAME, description=API_DESCRIPTION)


@app.get("/")
def read_root():
    return {
        "API": API_NAME,
        "Description": API_DESCRIPTION,
        "Port": API_PORT,
    }


DATA_SOURCE = "db/credit.json"


def get_client_data(client_name: str) -> dict:
    with open(DATA_SOURCE, "r") as file:
        data = json.load(file)
        return data.get(
            client_name,
            {"paiements_retard": 0, "montant_credit": 0, "faillite": False},
        )


def scoring_credit(
    paiements_retard: float,
    montant_credit: float,
    faillite: bool,
    revenu_mensuel: float,
) -> float:
    logging.debug("Calculating credit score")

    # Factor 1: Late payments
    score_paiements_retard = (
        100
        if paiements_retard == 0
        else 70
        if paiements_retard <= 2
        else 40
        if paiements_retard <= 5
        else 10
    )

    # Factor 2: Credit amount ratio
    ratio_endettement = montant_credit / revenu_mensuel if revenu_mensuel else 0
    score_credit = (
        100 if ratio_endettement < 0.2 else 70 if ratio_endettement < 0.5 else 40
    )

    # Factor 3: Bankruptcy
    score_faillite = 0 if faillite else 100

    # Weighted total score
    score_total = (
        score_paiements_retard * 0.40 + score_credit * 0.30 + score_faillite * 0.30
    )
    logging.debug(f"Credit score calculated: {score_total}")
    return score_total


@app.post("/verify-credit-score")
def solvencyVerif(LoanInformation: InformationsModel) -> InformationsModel:
    logging.debug(f"Raw LoanInformation received: {LoanInformation}")

    # JSON parsing with error handling
    try:
        # Fetching and validating required data
        revenu_mensuel = LoanInformation.monthly_income
        if not revenu_mensuel:
            logging.error("Missing 'Revenu Mensuel'")
            raise HTTPException(status_code=500, value="Revenu Mensuel manquant")

        name = LoanInformation.client_name
        if not name:
            logging.error("Missing 'Nom du Client'")
            raise HTTPException(status_code=500, value="Nom du Client manquant")

        logging.debug(f"Client name: {name}")
        revenu_mensuel = float(revenu_mensuel.replace("EUR", "").strip())
        data_client = get_client_data(name)

        logging.debug(f"Client data: {data_client}")

        # Calculating score
        score = scoring_credit(
            data_client.get("paiements_retard", 0),
            data_client.get("montant_credit", 0),
            data_client.get("faillite", False),
            revenu_mensuel,
        )
        LoanInformation.credit_score = score

        logging.debug(f"Final score: {score}")

        return LoanInformation

    except json.JSONDecodeError as e:
        logging.error(f"JSON conversion error: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de conversion JSON : {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=API_HOST, port=API_PORT)
