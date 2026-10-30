# Vetaher : page de liens autonome

Page de liens statique adaptée de [LittleLink](https://github.com/sethcottle/littlelink), sous licence MIT. La version présentée est un **aperçu à valider**, pas une migration déjà appliquée aux profils sociaux.

## Fonctionnement
- HTML et CSS uniquement ; aucun JavaScript, cookie ou outil de suivi.
- Logo authentique de l'association, hébergé avec la page.
- Les liens ouvrent les services déjà existants. Aucun paiement ni RIB n'est géré ici.
- Police système : pas de police tierce ni de dépendance externe au chargement.
- Les anciens boutons de don sont regroupés sous « Soutenir Vetaher » ; la page ne garantit aucun fléchage spécifique des fonds.

## Modifier les liens
1. Modifier `links.json` (libellés et destinations).
2. Exécuter `python3 build.py`.
3. Prévisualiser avec `python3 -m http.server 8000 --bind 127.0.0.1 --directory public`, puis ouvrir `http://127.0.0.1:8000/`.

La génération refuse les URL non HTTPS et les domaines hors de la liste autorisée. Pour ajouter un domaine légitime, revoir `ALLOWED_HOSTS` dans `build.py` plutôt que désactiver la validation.

## Déploiement
Le dossier `public/` est autonome et peut être hébergé sur un serveur statique. Le workflow GitHub Pages fourni reconstruit puis déploie uniquement ce dossier.

L'aperçu porte `noindex`, `nofollow` et un bandeau explicite. La publication de cet aperçu ne change aucun ancien lien. Après validation, il reste à remplacer l'adresse dans les bios des comptes autorisés. Le retrait du bandeau et des directives d'aperçu fait partie de cette validation, pas d'une migration automatique.

## Vérification
La recette utilise Chromium réel sur 320, 375, 390, 430, 768 et 1440 px. Elle contrôle les liens rendus, le débordement horizontal, les tailles tactiles, les liens de licence, le clavier, les contrastes et l'absence de requêtes tierces. Les destinations doivent aussi être vérifiées séparément en lecture seule : un HTTP 200 ne prouve pas qu'un service en aval fonctionne.

## Licence et provenance
Voir `PROVENANCE.json` et `public/LICENSE.txt`. LittleLink : Copyright 2019-2024 Seth Cottle. Adaptations de la page sous licence MIT. Le logo et la marque Vetaher restent la propriété de leur titulaire et ne sont pas placés sous licence MIT.
