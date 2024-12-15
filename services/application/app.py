import streamlit as st
import os
import requests

API_HOST = "127.0.0.1"
API_PORT = 8000


# Fonction pour interagir avec le service SOAP
def clientFunction(message):
    try:
        # Créez un client SOAP pour appeler le service LoanDemand
        response = requests.post(
            f"http://{API_HOST}:{API_PORT}/loan-demand",
            json={"text": message},
        )
        results = response.json()
        # Affiche et enregistre la réponse du service
        print(f"response {results}")
        for key, value in results.items():
            st.success(f"{key}: {value}")
        with open("upload_log.txt", "a") as log_file:
            log_file.write(f"Response for message '{message}': {results}\n")

    except Exception as e:
        print("An error occurred:", str(e))


# Fonction pour traiter le fichier détecté par Watchdog
def process_file(file_path):
    print(f"Processing file: {file_path}")
    try:
        # Lire le contenu du fichier
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            print(f"File content: {content}")
            for line in content.split("\n"):
                st.write(line)
            # Appeler la fonction clientFunction avec le contenu du fichier
            clientFunction(content)

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")


# Chemin du dossier à surveiller
upload_folder = "data/upload/"
# Ensure the directory exists
os.makedirs(upload_folder, exist_ok=True)


# Function to save the uploaded file
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(upload_folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


# web application
st.title("Loan Processing App")
st.write("This is a simple loan processing app built by Oussama MAHDJOUR-Sarra BRAHEM.")


# Upload file
# Upload file
uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])

if uploaded_file is not None:
    # Save the uploaded file
    file_path = save_uploaded_file(uploaded_file)
    st.success(f"File saved successfully at {file_path}")
    process_file(file_path)
