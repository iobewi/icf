Gouvernance du registre ICF
===========================

Le présent document définit la gestion des **tags TLV (0x01–0xFF)** : leur
**attribution**, leur **statut** et leur **évolution**.

Source de vérité
----------------
La **documentation officielle ICF** au format RST constitue la **seule référence valide** pour la définition, l’attribution et le suivi des tags.  
Aucune autre copie ou dérivé du registre ne fait foi.

Rôles
-----

- **Maintainers ICF** : garants de la cohérence du registre et de la compatibilité.
- **Contributeurs** : proposent de nouveaux tags ou modifient des définitions via Issues/PR.
- **Implémenteurs** : développent des lecteurs/émetteurs compatibles ICF (firmware, apps, outils).

Espaces de tags
---------------

- ``0x01–0x3F`` : Métadonnées générales (titre, URL, langue…)
- ``0x40–0x7F`` : Métadonnées média (réservé pour extensions futures)
- ``0x80–0x8F`` : **Expérimental** (modifiable sans préavis)
- ``0x90–0x9F`` : **Vendor-Specific** (préfixe obligatoire, doc publique)
- ``0xA0–0xDF`` : Extensions publiques (sur proposition)
- ``0xE0–0xEF`` : Système & chiffrement (E1…EF)
- ``0xF0–0xFF`` : Intégrité & autorité (hash, signature, authority_id)

Statuts des tags
----------------

- **Proposé** : soumis via Issue.
- **Réservé** : accepté, en attente d’implémentation.
- **Stable** : implémenté dans au moins une release avec **vecteurs de test** publiés.
- **Déprécié** : à remplacer (successeur indiqué).
- **Retiré** : interdit ; rejet impératif en mode strict.

Chaque entrée de la documentation officielle indique : *Type*, *Nom*, *Taille max*, *Version d’intro*, *Statut*, *Lien PR/Issue*, *Compatibilité*.

Processus d’allocation
----------------------

1. **Soumission** (Issue) : type/plage, nom, taille, sémantique, exemples, impacts sécurité/interop, statut initial.
2. **Review publique** : maintainers + communauté.
3. **Attribution** : ajout dans la documentation officielle au statut **Réservé**.
4. **Stabilisation** : intégration dans une release avec :
   - implémentation,
   - **vecteurs de test** (binaires + manifest),
   - documentation RST à jour.
   → passage en **Stable**.
5. **Évolution** : changement *breaking* → nouvelle version, phase **Déprécié** avec période de grâce, plan de migration & tests.

Règles spécifiques
------------------

- **Sécurité (0xE0–0xFF)** :
  - Documenter l’impact sécurité,
  - Fournir **vecteurs de test**,
  - Définir la politique de compatibilité (rejet strict si absent/invalide).

- **Vendor-Specific (0x90–0x9F)** :
  - Préfixe obligatoire (ex. ``acme_content_hash``),
  - Documentation publique minimale,
  - Interdiction des champs de sécurité (utiliser 0xE0–0xFF).

- **Compatibilité stricte** :
  - Mode strict → rejet : tags **Retirés**, usages hors spec, tailles invalides.
  - Mode libre → ignorer les tags inconnus, mais refuser tout tag malformé.

Versioning
----------

- La documentation officielle RST est la **seule source de vérité**.
- Le tableau “Types TLV définis” présent dans la spécification est **informatif** et renvoie vers la documentation officielle.
- Chaque ligne du registre officiel référence la **PR** d’introduction et la release de stabilisation.

Dépréciation & retrait
----------------------

- **Déprécié** : annoncé dans ``CHANGELOG``, conservé au moins une version complète, avec successeur.
- **Retiré** : rejeté en mode strict ; en mode libre → ignoré mais non interprété.

Conflits & arbitrage
--------------------

Les maintainers tranchent en dernier ressort, en priorisant :

1. la sécurité,
2. l’interopérabilité,
3. la stabilité (pas de changements inutiles).
