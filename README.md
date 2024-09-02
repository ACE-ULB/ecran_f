# Loop Videos Building F Monitor
Ce programme a pour but de faire tourner les vidéos provenant d'un Google Drive, en boucle sur un Raspi.

# Infos
Un code bash qui s'exécute au démarrage fait un git pull de ce repository et lance ensuite le code python ici présent.

L'accès en API au Drive est fait en accompagnement d'un ID OAuth fourni par Google Cloud via l'organisation ACE.

Lors de la première exécution il faut manuellement autoriser les permissions de manipulation via un compte qui peut gérer le dossier Drive.

# Execution
Chronologiquement le code fait :
- Consulte la liste des fichiers dans le Drive cible.
- Supprime les vidéos existant en local mais plus sur le Drive.
- Télécharge les vidéos n'existant pas en local mais bien sur le Drive.
- Lance une boucle vidéo via omxplayer qui ne s'arretera pas.
- Ou si il ni a pas de vidéo en local, affichera l'image "empty_drive.png" ici présente également.

# Credits
Code made by None - julien.leclercq@ace-ulb.be