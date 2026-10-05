# borinoldcars.be

Site vitrine public du club **Borin'Old Cars** : https://borinoldcars.be

- Le contenu (slogan, email, adresse, réseaux, comité, agenda, garage, albums, boutique) est lu dans les
  fichiers de l'application des membres : https://borinoldcars.github.io/app/data/
  (dépôt `borinoldcars/borinoldcars.github.io`). Il n'y a donc rien à mettre à jour ici pour une nouvelle
  sortie, voiture ou photo.
- Les textes de présentation (« Le club », « Nous rejoindre ») se modifient dans `index.html`.
- Pages internes par ancre : `#sorties`, `#sortie-<id>`, `#voitures`, `#voiture-<id>`, `#albums`, `#album-<id>`,
  `#adhesion` (formulaire d'adhésion Tally intégré, identifiant `ADHESION_FORM` dans `site.js`).
- Le domaine est déclaré dans le fichier `CNAME` ; il est servi par GitHub Pages (branche `main`, dossier racine).
- Après une modification de `site.css` ou `site.js`, augmenter le numéro `?v=` dans `index.html` pour que les
  navigateurs rechargent les fichiers.
