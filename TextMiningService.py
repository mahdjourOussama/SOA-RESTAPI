import logging
import re
from fastapi import FastAPI
from models import InformationsModel

logging.basicConfig(level=logging.DEBUG)

API_NAME = "Client Information Extraction Service"
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


@app.get("/extract")
def extraire_informations(texte: str) -> InformationsModel:
    """
    Fonction pour extraire les informations du texte donné
    :param texte: texte contenant les informations
    :return: InformationsModel
    """
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
        match = re.search(pattern, texte, re.DOTALL)
        if match:
            informations[key] = match.group(1).strip()

    # Affichage pour débogage
    logging.debug("Informations extraites :", informations)

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

    uvicorn.run(app, port=API_PORT)
