# Loop Videos Building F Monitor
Ce programme a pour but de faire tourner les vidéos provenant d'un Google Drive, en boucle sur un Raspberry Pi 4.

## Infos
Un code bash qui s'exécute au démarrage fait un git pull de ce repository et lance ensuite le code python ici présent.

L'accès en API au Drive est fait en accompagnement d'un ID OAuth fourni par Google Cloud via l'organisation ACE.

Lors de la première exécution il faut manuellement autoriser les permissions de manipulation via un compte qui peut gérer le dossier Drive.

Le programme récupère les vidéos sur le Drive et supprime celles qu'il a téléchargé mais n'y sont plus, et lance ensuite la boucle vidéo. Par conséquent, il regarde l'état du Drive une fois par jour, lors de son allumage donc.

## Execution
Chronologiquement le code fait :
- Consulte la liste des fichiers dans le Drive cible.
- Supprime les vidéos existant en local mais plus sur le Drive.
- Télécharge les vidéos n'existant pas en local mais bien sur le Drive.
- Lance une boucle vidéo via cvlc qui ne s'arretera pas.
- Ou si il ni a pas de vidéo à faire tourner, fait une boucle sur la video "default.mp4" présente sur le Drive avec accès restreint.

# Manipulations
Pour intéragir avec le Raspberry Pi sans pour autant le déplacer physiquement, utiliser ssh :
- ssh ace@[IP ADDRESS]

Le lancement automatique du programme shell à la racine "videoloop.sh" qui gère le github et lance ensuite la boucle, se fait via un service :
- systemctl status/start/restart/enable/disable ecran_F

Localisation du code service "ecran_F"
- /etc/systemd/system/ecran_F.service

Pour arrêter la boucle et voir le terminal sur l'écran :
- kill [PID de ecran_F obtenu via status]

Pour un simple redémarrage afin de forcer un nouvel update de dernière minute sur le Drive :
- sudo reboot

# Credits
Code made by None - julien.leclercq@ace-ulb.be