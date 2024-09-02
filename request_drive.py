from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import subprocess

# Authentification avec Google
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

drive = GoogleDrive(gauth)

# ID du dossier Google Drive
folder_id = '11Dk0-U_xkFqOfp7jRlYWZyfpN7GbhJJi'

# Dossier local pour les vidéos
local_folder = "./videos"

# Créer le dossier local s'il n'existe pas
if not os.path.exists(local_folder):
    os.makedirs(local_folder)

# Lister les fichiers sur Google Drive
drive_files = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
drive_file_names = [file['title'] for file in drive_files]

# Lister les fichiers locaux
local_files = [f for f in os.listdir(local_folder) if os.path.isfile(os.path.join(local_folder, f))]

# 1. Supprimer les vidéos locales qui ne sont pas sur le Drive
for local_file in local_files:
    if local_file not in drive_file_names:
        print(f"Suppression de {local_file}...")
        os.remove(os.path.join(local_folder, local_file))

# 2. Télécharger les vidéos manquantes
for file in drive_files:
    file_path = os.path.join(local_folder, file['title'])
    if not os.path.exists(file_path):
        print(f"Téléchargement de {file['title']}...")
        file.GetContentFile(file_path)

# 3. Lister les vidéos restantes après synchronisation
video_files = [os.path.join(local_folder, f) for f in os.listdir(local_folder) if f.endswith(('.mp4', '.avi', '.mkv'))]

# 4. Boucle de lecture ou affichage de l'image si aucune vidéo
if video_files:
    while True:
        for video in video_files:
            print(f"Lecture de {video}...")
            subprocess.run(['omxplayer', '--loop', video])
else:
    # 4bis. Afficher une image si aucune vidéo n'est disponible
    print("Aucune vidéo disponible. Affichage de l'image empty_drive.png.")
    subprocess.run(['fbi', '-T', '1', '-a', 'empty_drive.png'])
