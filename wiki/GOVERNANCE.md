# Gouvernance du registre ICF

Le présent document définit comment sont gérés les **tags TLV (0x01–0xFF)**, leur
**attribution**, leur **statut** et leur **évolution**.

## Rôles

- **Maintainers ICF** : garants de la cohérence du registre et de la compatibilité.
- **Contributeurs** : toute personne ou organisation proposant de nouveaux tags ou modifiant des définitions existantes via Issues/PR.
- **Implémenteurs** : auteurs de lecteurs/émetteurs compatibles ICF (firmware, apps, outils).

## Espaces de tags

- `0x01–0x3F` : Métadonnées générales (titre, URL, langue, etc.)
- `0x40–0x7F` : Métadonnées média (réservé pour extensions futures)
- `0x80–0x8F` : **Expérimental** (peut changer sans préavis)
- `0x90–0x9F` : **Vendor-Specific** (nécessite préfixe de nommage et documentation)
- `0xA0–0xDF` : Extensions publiques (sur proposition)
- `0xE0–0xEF` : Système & chiffrement (E1…EF)
- `0xF0–0xFF` : Intégrité & autorité (hash, signature, authority_id)

## Statuts des tags

- **Proposé** : description soumise via Issue.
- **Réservé** : accepté, en attente d’implémentation.
- **Stable** : présent dans au moins une release avec **vecteurs de test** publiés.
- **Déprécié** : ne doit plus être utilisé (successeur indiqué).
- **Retiré** : interdit ; rejet impératif en mode strict.

Chaque entrée du registre indique : *Type*, *Nom*, *Taille max*, *Version d’intro*, *Statut*, *Lien vers PR/Issue*, *Notes de compatibilité*.

## Process d’allocation

1. **Issue** avec :
   - Type souhaité (ou plage), nom, taille, sémantique exacte,
   - exemples d’usage, impact sécurité/interop,
   - proposition de statut initial (**Proposé**).
2. **Review publique** par les maintainers (+ retours de la communauté).
3. **Attribution** (mise à jour de `doc/registry.md`) en **Réservé**.
4. **Stabilisation** : une **release** (ICF tools/firmware) doit inclure :
   - implémentation,
   - **vecteurs de test** (binaires + manifest),
   - documentation.
   → passage en **Stable**.
5. **Évolution** : tout changement **breaking** nécessite :
   - nouvelle version de spec,
   - phase **Déprécié** avec période de grâce,
   - plan de migration & tests.

## Règles spécifiques

- **Sécurité (0xE0–0xFF)**  
  Toute proposition affectant `0xE0–0xFF` doit :
  - documenter l’impact sécurité,
  - fournir **vecteurs de test**,
  - préciser la politique de compat (rejet strict si absent/invalide).

- **Vendor-Specific (0x90–0x9F)**  
  - Préfixe obligatoire dans le **Nom** (ex. `acme_content_hash`),
  - Documentation publique minimale,
  - Interdiction d’y placer des champs **de sécurité** (utiliser 0xE0–0xFF).

- **Compatibilité stricte**  
  - Les lecteurs **mode strict** doivent **rejeter** : tags **Retirés**, usages contredisant la spec, ou *tailles* hors bornes.
  - Les lecteurs **mode libre** peuvent ignorer un tag *inconnu* mais **ne doivent pas** tolérer un tag **malformé**.

## Versioning & registre

- `doc/registry.md` est la **source de vérité** des tags.
- Le tableau “Types TLV définis (v1)” dans `SPEC-ICF.md` est **informatif** et doit renvoyer vers le registre.
- Chaque ligne du registre référence la **PR** qui l’a introduite et la release qui l’a rendue **Stable**.

## Dépréciation & retrait

- **Déprécié** : annoncé dans `CHANGELOG`, conservé au moins **une version** complète ; fournir un **successeur**.
- **Retiré** : rejeté en mode strict ; en mode libre, peut être ignoré mais ne doit pas être interprété.

## Conflits & arbitrage

- Les maintainers tranchent en dernier ressort en privilégiant :
  1. la sécurité,
  2. l’interop,
  3. la stabilité (pas de breakage inutile).

