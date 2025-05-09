# Tetris-Geschenk (mit benutzerdefinierten Figuren)

Ein personalisiertes Tetris-Spiel, erstellt mit Python und Pygame, mit individuell gestalteten .png-Sprites.

## Features

- klassische Tetris-Logik
- benutzerdefinierte Figuren als PNG-Bilder in /assets
- Punktestand, Levelsystem, Game-Over-Screen
- portable `.exe` (keine Installation nötig)

## Ordnerstruktur

```bash
tetris/
├── __init__.py
├── main.py
├── game.py
├── tetromino.py
└── assets/
    ├── L-block.png
    ├── Z-block.png
    ├── ...
    └── brthday.ico      
```

## EXE mit PyInstaller erstellen

(venv aktivieren)

```bash
pyinstaller --onefile --windowed `
  --paths . `
  --icon assets\brthday.ico `
  --add-data "assets;assets" `
  main.py
```

## Assets

Die Block-Sprites 128×128 px bei voller Transparenz.

## Weitergabe

Gib einfach die `dist/main.exe` oder den ganzen `dist/`-Ordner weiter. 

---

## Hinweise

Dieses Projekt wurde ursprünglich als Geburtstagsgeschenk erstellt und ist anpassbar für andere Themen, Figuren und Farben.
