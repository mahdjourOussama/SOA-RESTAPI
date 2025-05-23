import logging
import re
from fastapi import FastAPI
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
API_NAME = "Client Information Extraction Service"
API_PORT = 8004
API_DESCRIPTION = f"A simple API for {API_NAME}"

app = FastAPI(title=API_NAME, description=API_DESCRIPTION)


@app.get("/")
def read_root():
    return {
        "API": API_NAME,
        "Description": API_DESCRIPTION,
        "Port": API_PORT,
    }


@app.post("/extract")
def extraire_informations(request: LoanRequest) -> InformationsModel:
    """
    Fonction pour extraire les informations du texte donné
    :param texte: texte contenant les informations
    :return: InformationsModel
    """
    logging.info("Informations extraites :", request.text)

    # Dictionnaire pour stocker les informations extraites
    informations = {}
    # Liste des clés à extraire
    keys = [
        "Adresse",
        "Email",
        "Numéro de Téléphone",
        "Montant du Prêt Demandé",
        "Durée du Prêt",
        "Description de la Propriété",
        "Revenu Mensuel",
        "Dépenses Mensuelles",
        "Nom du Client",
    ]

    # Utilisation d'expressions régulières pour extraire chaque information
    for key in keys:
        pattern = rf"{key}:\s*(.*?)\s*(?=\b(?:{'|'.join(keys)})|$)"
        match = re.search(pattern, request.text, re.DOTALL)
        if match:
            informations[key] = match.group(1).strip()

    # Affichage pour débogage

    # Retourne les informations en JSON
    informationObject = InformationsModel(
        address=informations.get("Adresse", ""),
        email=informations.get("Email", ""),
        phone_number=informations.get("Numéro de Téléphone", ""),
        loan_amount=informations.get("Montant du Prêt Demandé", ""),
        loan_duration=informations.get("Durée du Prêt", ""),
        property_description=informations.get("Description de la Propriété", ""),
        monthly_income=informations.get("Revenu Mensuel", ""),
        monthly_expenses=informations.get("Dépenses Mensuelles", ""),
        client_name=informations.get("Nom du Client", ""),
    )
    logging.debug(f"Extracted information: {informationObject}")
    return informationObject


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=API_HOST, port=API_PORT)
