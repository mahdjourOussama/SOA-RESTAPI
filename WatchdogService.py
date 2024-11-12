import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
from ServiceComposer import API_HOST, API_PORT
import streamlit as st


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
        with open("log.txt", "a") as log_file:
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

        # Déplacer le fichier traité vers un dossier d'archivage
        archive_folder = "data/processed/"
        os.makedirs(archive_folder, exist_ok=True)
        new_file_path = os.path.join(archive_folder, os.path.basename(file_path))
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        os.rename(file_path, new_file_path)
        print(f"Moved {file_path} to {archive_folder}")

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")


# Gestionnaire d'événements pour surveiller les nouveaux fichiers
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Vérifiez que l'événement correspond à un fichier
        if not event.is_directory:
            process_file(event.src_path)


# Chemin du dossier à surveiller
folder_to_watch = "data/"
# Ensure the directory exists
os.makedirs(folder_to_watch, exist_ok=True)


# Function to save the uploaded file
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(folder_to_watch, uploaded_file.name)
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

# Display the file content and client response if available


observer = Observer()

event_handler = MyHandler()
observer.schedule(event_handler, folder_to_watch, recursive=False)
observer.start()


print(f"Watching folder: {os.path.abspath(folder_to_watch)}")

# Garder le script en cours d'exécution pour surveiller le dossier
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping observer...")
    observer.stop()
observer.join()
print("Observer stopped.")
