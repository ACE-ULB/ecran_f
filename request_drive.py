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

# Télécharger "default.mp4" si non existant dans le dossier local
default_video_path = os.path.join(local_folder, "default.mp4")
default_video = drive.ListFile({'q': f"'{folder_id}' in parents and title='default.mp4' and trashed=false"}).GetList()

if default_video and not os.path.exists(default_video_path):
    print(f"Téléchargement de default.mp4...")
    default_video[0].GetContentFile(default_video_path)

# Lister les fichiers sur Google Drive (excluant "default.mp4")
drive_files = drive.ListFile({'q': f"'{folder_id}' in parents and title != 'default.mp4' and trashed=false"}).GetList()
drive_file_names = [file['title'] for file in drive_files]

# Lister les fichiers locaux (excluant "default.mp4")
local_files = [f for f in os.listdir(local_folder) if os.path.isfile(os.path.join(local_folder, f)) and f != "default.mp4"]

# 1. Supprimer les vidéos locales qui ne sont pas sur le Drive (excluant "default.mp4")
for local_file in local_files:
    if local_file not in drive_file_names:
        print(f"Suppression de {local_file}...")
        os.remove(os.path.join(local_folder, local_file))

# 2. Télécharger les vidéos manquantes (excluant "default.mp4")
for file in drive_files:
    file_path = os.path.join(local_folder, file['title'])
    if not os.path.exists(file_path):
        print(f"Téléchargement de {file['title']}...")
        file.GetContentFile(file_path)

# 3. Lister les vidéos restantes après synchronisation (excluant "default.mp4")
video_files = [os.path.join(local_folder, f) for f in os.listdir(local_folder) if f.endswith(('.mp4', '.avi', '.mkv')) and f != "default.mp4"]

# 4. Boucle de lecture
if video_files:
    while True:
        for video in video_files:
            print(f"Lecture de {video}...")
            subprocess.run(['cvlc', '--no-video-title-show', video])
else:
    print("Aucune vidéo disponible. Lecture de default.mp4.")
    subprocess.run(['cvlc', '--loop', '--no-video-title-show', default_video_path])
