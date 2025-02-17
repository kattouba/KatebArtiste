# Kateb Artiste - Un jeu éducatif par Studio KATEB & Papa

## À propos du Studio

Kateb Artiste est développé par **Studio KATEB & Papa**, un studio spécialisé dans les jeux éducatifs. Vous pouvez en savoir plus sur notre travail sur notre site officiel : [Studio KATEB & Papa](https://studiokatebetpapa.rf.gd).

## Description

Kateb Artiste est une application de quiz développée en Python avec BeeWare dont le but est d'aider les joueurs à reconnaître les œuvres d'art, leurs artistes et leurs styles à travers un quiz interactif.

## Installation et Build Android

1. Assurez-vous d'avoir Python installé sur votre machine.
2. Clonez ce dépôt GitHub :
   ```
   git clone <URL_DU_DEPOT>
   ```
3. Accédez au dossier du projet :
   ```
   cd <NOM_DU_DOSSIER>
   ```
4. Installez les dépendances nécessaires :
   ```
   pip install briefcase toga
   ```

## Build pour Android

1. Assurez-vous d'avoir installé les outils nécessaires pour Briefcase :
   ```
   briefcase install
   ```
2. Construisez l'application pour Android avec :
   ```
   briefcase build android
   ```
3. Si besoin, vous pouvez aussi empaqueter l'application avec :
   ```
   briefcase package android
   ```

## Installation de l'APK sur Android

1. Après avoir construit l'application, vous obtiendrez un fichier APK.
2. Transférez l'APK sur votre appareil Android.
3. Installez l'APK en l'ouvrant depuis un gestionnaire de fichiers ou en exécutant :
   ```
   adb install <chemin_vers_l_apk>
   ```
4. Ouvrez l'application depuis le menu de votre appareil.

## Utilisation

1. Lancez l'application en ouvrant l'APK installé depuis le menu de votre appareil Android.
2. Répondez aux questions en choisissant parmi les options proposées.
3. Le score final est affiché après 10 questions.

## Structure du projet

```
/src
  /ressources
    - paintings.csv  # Données des tableaux
    /images  # Images des peintures
      - 1.jpg
      - 2.jpg
    - correct.mp3  # Son pour bonne réponse
    - wrong.mp3  # Son pour mauvaise réponse
  app.py  # Code principal de l'application
```

## Contributions

Les contributions sont les bienvenues ! N'hésitez pas à soumettre une pull request.

## Licence

Ce projet est sous licence GNU GPL v2.

