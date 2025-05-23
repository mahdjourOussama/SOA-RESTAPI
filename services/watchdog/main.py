import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

API_HOST = "127.0.0.1"
API_PORT = 8000


def clientFunction(message):
    try:
        response = requests.post(
            f"http://{API_HOST}:{API_PORT}/loan-demand",
            json={"text": message},
        )
        results = response.json()
        print("-" * 25, "Response", "-" * 25)
        for key, value in results.items():
            print(f"{key}: {value}")
        print("-" * 50)
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
            print("-" * 25, "File content", "-" * 25)
            print(f"File content: {content}")
            print("-" * 50)
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
