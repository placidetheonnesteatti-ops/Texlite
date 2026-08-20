# Docu2TeX

Docu2TeX est une application de bureau hors ligne destinée à convertir des documents **Word (.docx)** et **PDF (.pdf)** vers des projets **LaTeX** propres et réutilisables.

## Objectif de la V1

- interface Windows simple et présentable ;
- conversion locale, sans envoi des documents vers un serveur ;
- DOCX → LaTeX avec conservation du texte, styles de base, tableaux, sauts de page et images ;
- PDF → LaTeX par extraction/reconstruction de texte et d'images ;
- compilation XeLaTeX/LuaLaTeX automatique si un moteur LaTeX compatible est installé ;
- mesure de pagination lorsque le document source peut être rendu localement ;
- projet de sortie organisé avec `main.tex`, `images/` et le PDF produit ;
- pipeline GitHub Actions pour construire une version Windows avec PyInstaller.

## Limite importante

La pagination exacte entre Word/PDF et LaTeX n'est pas une opération mathématiquement garantie : Word, PDF et TeX utilisent des moteurs de composition différents. Docu2TeX mesure l'écart quand il peut le faire et signale les différences. La V1 privilégie une reconstruction éditable plutôt qu'une simple image du document.

La reconstruction PDF est volontairement signalée comme une approximation : les PDF scannés, formulaires complexes et compositions graphiques avancées nécessitent un moteur spécialisé plus poussé.

## Lancer en développement

Python 3.13 recommandé.

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements-dev.txt
python main.py
```

Pour la compilation PDF, installez **MiKTeX** avec XeLaTeX activé ou **TeX Live**. Sous Windows, Docu2TeX détecte automatiquement `xelatex`, puis `lualatex`. PDFLaTeX n'est pas compatible avec le préambule utilisé par l'application.

## Tests

```bash
pytest -q
```

## Construire l'EXE sous GitHub

Le workflow `.github/workflows/windows-build.yml` exécute les tests unitaires puis construit une archive `Docu2TeX-Windows.zip` à partir d'un tag `v*` ou d'un lancement manuel.

### Publication correcte

N'envoyez pas le fichier ZIP de livraison seul sur GitHub : GitHub Actions ne l'extrait pas. Décompressez d'abord l'archive, ouvrez le dossier `Docu2TeX`, puis publiez **son contenu** à la racine du dépôt. Le fichier `.github/workflows/windows-build.yml` et `build_windows.spec` doivent être présents dans ce dépôt.

## Architecture

```text
Docu2TeX/
├── app/                  # interface PySide6
├── core/                 # moteur de conversion
│   ├── compiler.py
│   ├── docx_converter.py
│   ├── pdf_converter.py
│   ├── service.py
│   └── tex_writer.py
├── tests/
├── .github/workflows/
├── build_windows.spec
├── main.py
└── requirements*.txt
```

## V2 prévue

- moteur de comparaison visuelle page par page ;
- optimisation automatique de la pagination ;
- meilleure récupération des tailles/positions réelles des images ;
- tableaux fusionnés plus fidèles ;
- styles Word → macros LaTeX ;
- en-têtes et pieds de page ;
- notes de bas de page ;
- listes imbriquées ;
- équations et objets Office ;
- traitement amélioré des PDF scannés avec OCR optionnel ;
- mode « fidélité maximale » et aperçu avant/après.

## Capacités renforcées de la V1.1

- styles de titres et mise en forme de base des caractères ;
- listes à puces et numérotées simples ;
- en-tête et pied de page simples ;
- images DOCX récupérées dans `images/` et dimensionnées sans étirement volontaire ;
- tableaux courts en `tabularx`, tableaux longs en `longtable` ;
- reconstruction PDF par blocs de texte avec estimation de corps de police et conservation des séparations de pages ;
- contrôle de pagination et tentative d'ajustement automatique de `parskip` lorsque le nombre de pages diffère ;
- compilation locale avec XeLaTeX, LuaLaTeX ou PDFLaTeX ;
- aucun service cloud, aucune API distante.

## Installation Windows

Le programme fonctionne hors ligne une fois ses dépendances installées. Pour générer le PDF automatiquement, **MiKTeX ou TeX Live doit être installé sur le PC Windows**. L'EXE produit par GitHub Actions ne contient volontairement pas une distribution LaTeX complète.

## GitHub Actions

1. Pousser le dépôt sur GitHub.
2. Lancer manuellement `Build Windows EXE` ou pousser un tag `v1.1.1`.
3. Récupérer `Docu2TeX-Windows.zip` dans les artifacts ou dans la Release.
