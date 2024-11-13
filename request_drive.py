from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import subprocess
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Identifier le dossier Google Drive en fonction du fichier local
if os.path.exists(".solbosch"):
    folder_id = os.getenv("SOLBOSCH_FOLDER_ID")
    print("Configuration Solbosch détectée.")
elif os.path.exists(".plaine"):
    folder_id = os.getenv("PLAINE_FOLDER_ID")
    print("Configuration Plaine détectée.")
else:
    raise FileNotFoundError("Aucun fichier de configuration trouvé. Vérifiez la configuration.")

if not folder_id:
    raise ValueError("L'ID du dossier Google Drive est manquant dans le fichier .env.")

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

if default_video_list:
    default_video = default_video_list[0]
    default_video_id = default_video['id']
    default_video_modified_date = default_video['modifiedDate']
    
    # Vérification de l'existence et de la mise à jour de la vidéo par défaut
    if os.path.exists(default_video_path):
        local_modified_time = os.path.getmtime(default_video_path)
        if local_modified_time < default_video_modified_date:
            print("Mise à jour de default.mp4 car une version plus récente est disponible...")
            default_video.GetContentFile(default_video_path)
    else:
        print("Téléchargement de default.mp4...")
        default_video.GetContentFile(default_video_path)

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
while True:
	if video_files and len(video_files) > 1:
		for video in video_files:
			print(f"Lecture de {video}...")
			subprocess.run(['cvlc', '--no-video-title-show', '--play-and-exit', video])
	elif len(video_files) == 1:
		video = video_files[0]
		print(f"Lecture de {video}...")
		subprocess.run(['cvlc', '--no-video-title-show', '--loop', video])
	else:
		print("Aucune vidéo disponible. Lecture de la vidéo par défaut")
		subprocess.run(['cvlc', '--loop', '--no-video-title-show', default_video_path])
