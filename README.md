# borinoldcars.be

Site vitrine public du club **Borin'Old Cars** : https://borinoldcars.be

- Le contenu (slogan, email, adresse, réseaux, comité, agenda, garage, albums, boutique) est lu dans les
  fichiers de l'application des membres : https://borinoldcars.github.io/app/data/
  (dépôt `borinoldcars/borinoldcars.github.io`). Il n'y a donc rien à mettre à jour ici pour une nouvelle
  sortie, voiture ou photo.
- Les textes de présentation (« Le club », « Nous rejoindre ») se modifient dans `index.html`.
- Pages internes par ancre : `#sorties`, `#sortie-<id>`, `#voitures`, `#voiture-<id>`, `#albums`, `#album-<id>`,
  `#adhesion` (formulaire d'adhésion Tally intégré, identifiant `ADHESION_FORM` dans `site.js`),
  `#inscription-<id>` (inscription à une sortie), `#commande` (bon de commande de la boutique, lien
  `commande` de `boutique.json`).
- Inscriptions : quand le lien `Inscription` d'une sortie (Google Sheet → `events.json`) est un formulaire
  Tally (`https://tally.so/r/...`), le bouton « S'inscrire » ouvre une page du site avec ce formulaire
  intégré. Tout autre lien s'ouvre tel quel dans un nouvel onglet.
- Les formulaires intégrés ont un fond transparent : dans Tally, leur donner les couleurs du site
  (Design → fond #e5decf, texte #222222, accent #8a6538, bouton #2f2118 / texte #f1e4cc,
  police Playfair Display), sinon le texte risque d'être illisible.
- Le domaine est déclaré dans le fichier `CNAME` ; il est servi par GitHub Pages (branche `main`, dossier racine).
- Après une modification de `site.css` ou `site.js`, augmenter le numéro `?v=` dans `index.html` pour que les
  navigateurs rechargent les fichiers.
- Road books : `roadbooks.json` associe une sortie (son `id` dans `events.json`) à un PDF Google Drive
  (`"id-de-la-sortie": "id-du-fichier"`, ou `{ "pdf": "id", "gpx": "id" }` pour ajouter le bouton
  « Télécharger le GPX »). La fiche de la sortie affiche alors un bouton « Road book » qui ouvre
  `#roadbook-<id>` (aperçu + téléchargement). Les fichiers doivent être partagés « Tous les utilisateurs disposant du lien ».
- Partenaires : `sponsors.json` (`nom`, `description`, `logo` dans `sponsors/`, `lien` facultatif). La section
  « Nos partenaires » s'affiche en bas de l'accueil dès qu'il y a au moins un partenaire.
- Portraits du comité : `portraits.json` (`"slug-du-membre": "portraits/fichier.webp"`, le slug est celui de
  `config.json` → `comite`). Image carrée détourée ; elle s'affiche en rond sur la carte du membre.
- Affiches de l'agenda : le robot « Copie des affiches de l'agenda » (`.github/workflows/affiches.yml`,
  toutes les 3 heures) copie les affiches Google Drive dans `affiches/` ; le site les affiche depuis
  borinoldcars.be et ne repasse par Drive que pour une affiche pas encore copiée.
