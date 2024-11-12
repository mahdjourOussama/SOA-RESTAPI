import logging
import json
from fastapi import FastAPI, HTTPException
from models import InformationsModel

logging.basicConfig(level=logging.DEBUG)
API_HOST = "127.0.0.1"
API_NAME = "Client Properity Checking Service"
API_PORT = 8002
API_DESCRIPTION = f"A simple API for {API_NAME}"

app = FastAPI(title=API_NAME, description=API_DESCRIPTION)


@app.get("/")
def read_root():
    return {
        "API": API_NAME,
        "Description": API_DESCRIPTION,
        "Port": API_PORT,
    }


DATA_SOURCE = "db/properity.json"


def get_properity_data(prop_desc: str) -> dict:
    with open(DATA_SOURCE, "r") as file:
        data = json.load(file)
        return {des: data.get(des, 0) for des in prop_desc}


def scoring_properity(desc_score: dict) -> float:
    logging.debug("Calculating Properity score")
    score_total = 0
    for value in desc_score.values():
        if value:
            score_total += value
    # Factor 1: Late payments

    logging.debug(f"Properity score calculated: {score_total}")
    return score_total


@app.post("/properity-evaluation")
def ProperityVerify(LoanInformation: InformationsModel) -> InformationsModel:
    logging.debug(f"Raw LoanInformation received: {LoanInformation}")

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

        properity_description = [
            t.strip().replace(",", "").replace(".", "")
            for t in LoanInformation.property_description.lower().split(" ")
        ]
        properity_data = get_properity_data(properity_description)

        logging.debug(f"Properity data: {properity_data}")

        # Calculating score
        score = scoring_properity(properity_data)
        LoanInformation.properity_value = score

        logging.debug(f"Final score: {score}")
        return LoanInformation
    except Exception as e:
        logging.error(f"error: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de conversion JSON : {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=API_HOST, port=API_PORT)
