# Changelog

## 1.1.1 — 2026-08-20

- Correction du paquet Windows PyInstaller : version dossier `dist\\Docu2TeX` et archive GitHub fonctionnelle.
- `build_windows.spec` est désormais inclus lors d'un `git add .`.
- Correction des en-têtes et pieds de page LaTeX.
- XeLaTeX ou LuaLaTeX sont maintenant les seuls moteurs acceptés, conformément au préambule.
- Échappement LaTeX renforcé (`\\`, `~`, `^` et opérateurs mathématiques Unicode).
- Prise en charge des styles Word français `Titre 1` à `Titre 4` ; le niveau 4 devient `\\paragraph`.
- Les réglages de nettoyage du texte, de sauts de page, de conservation des images et d'optimisation des tableaux sont appliqués par le moteur.
- Les tests unitaires s'exécutent dans GitHub Actions ; le test de compilation LaTeX est désormais identifié comme test d'intégration.

## 1.1.0 — 2026-08-20

- Renforcement du moteur DOCX → LaTeX.
- Listes à puces et numérotées simples.
- En-têtes et pieds de page simples.
- Dimensions d'images DOCX récupérées depuis les propriétés du document.
- Tableaux courts générés en `tabularx` et tableaux longs en `longtable`.
- Reconstruction PDF par blocs, avec taille de police estimée.
- Contrôle du nombre de pages source/résultat.
- Ajustement automatique limité de la pagination via `parskip`.
- Bouton d'ouverture du dossier de sortie.
- Workflow GitHub Actions prêt pour la construction Windows et les Releases.
