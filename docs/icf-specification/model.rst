Types de badges et sécurité
===========================

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 15

   * - Type
     - Signature requise
     - Chiffrement requis
     - Persistant
   * - Ressource
     - Optionnel / Requis selon mode
     - Non
     - Non
   * - Configuration
     - Non
     - Non
     - Non
   * - Administration
     - Oui
     - Oui (ECIES)
     - Oui


Profils ICF
===========

ICF-Full (recommandé NTAG215/216)
---------------------------------

**Requis :**
- `0x01` URL **ou** `0x03` Titre (au moins un des deux)
- `0xF2` Hash (SHA-256) calculé **sur tous les TLV précédents**
- `0xF3` Signature Ed25519 **du hash** (valeur de `0xF2`)
- `0xF4` AuthorityID (8 octets)

**Optionnels :**
- `0x02` Langue (2 lettres)
- `0x04` Tag pédagogique (3 octets : cycle, matière, sous-classe)
- `0x05` Rétention (jours)
- `0x06` Expiration (u32 epoch)
- `0xE0` Type badge (0=ressource, 1=config, 2=admin)
- `0xE1–0xEF` Payload système (JSON ou binaire, usage lecteur)

**Ordre recommandé :**
::

[0x01?] [0x02?] [0x03?] [0x04?] [0x05?] [0x06?] [0xE0?] [0xE1–0xEF?] [0xF2] [0xF3] [0xF4] [0xFF?]   

ICF-Lite (NTAG213)
------------------

**Requis :**
- `0x01` URL **ou** `0x03` Titre

**Optionnels :**
- `0x02` Langue, `0x06` Expiration, `0x04` Tag pédagogique

**Sécurité :**
- Pas d’obligation de `0xF2/0xF3/0xF4`. Le lecteur **doit** afficher l’état *Non vérifié* si la signature est absente.


Profils de lecteurs (interop)
=============================

- **Reader-L0** : Parse TLV, affiche `URL/Titre`, `Langue`, `Expiration` si présents. Affiche un état de confiance (*Non vérifié* si pas de signature).
- **Reader-L1** : En plus, calcule `0xF2`, vérifie `0xF3` avec la clé liée à `0xF4`. Affiche *Validé (autorité X)* / *Signature invalide* / *Autorité inconnue*.
- **Reader-L2** : En plus, déchiffre `0xE1–0xEF` si applicable. L’échec de déchiffrement **ne bloque pas** l’affichage des métadonnées publiques.


ICF sur NDEF
============

- **Record type** : MIME
- **MIME type** : `application/vnd.icf+tlv`
- **Payload** : octets TLV ICF complets (incluant `0xF2`, `0xF3`, `0xF4` si présents)
- **Message recommandé** : un seul record MIME

**Remarque :** NDEF n’implique **aucune** réaffectation de tags TLV ICF. Les en-têtes NDEF ne sont pas signés ; la confiance repose sur `0xF2/0xF3/0xF4` à l’intérieur du payload ICF.


Espace utilisé sur NTAG215 (504 octets max)
===========================================

Capsule de ressource (`badge_type: 0x00`)
-----------------------------------------

.. list-table::
   :header-rows: 1

   * - Champ
     - Taille typique
   * - `0x01` URL
     - \-120 à 200 octets
   * - `0x02` Langue
     - 2 octets
   * - `0x03` Titre
     - \-32 à 64 octets
   * - `0x04` Tag péd.
     - 3 octets
   * - `0x05` Rétention
     - 1 octet
   * - `0x06` Expiration
     - 4 octets
   * - `0xF2` Hash
     - 32 octets
   * - `0xF3` Signature
     - 64 octets
   * - `0xF4` AuthorityID
     - 8 octets
   * - `0xFF` Fin
     - 0 à 2 octets
   * - **Total**
     - **\-330 à 430 o**

Capsule de configuration (`badge_type: 0x01`)
---------------------------------------------

.. list-table::
   :header-rows: 1

   * - Champ
     - Taille typique
   * - `0xE0` Type
     - 1 octet
   * - `0xE1` Payload JSON
     - \-30 à 150 o
   * - `0xFF` Fin
     - 0 à 2 octets
   * - **Total**
     - **\-40 à 160 o**

> Dépend fortement du contenu JSON (nombre de clés/valeurs, formatage compact ou non)

Capsule de ressource avec configuratioon (`badge_type: 0x00 + 0xE1`)
--------------------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Champ
     - Taille typique
   * - URL (`0x01`)
     - \-120 à 200 octets
   * - Langue (`0x02`)
     - 2 octets
   * - Titre (`0x03`)
     - \-32 à 64 octets
   * - Tag pédagogique (`0x04`)
     - 3 octets
   * - Rétention (`0x05`)
     - 1 octet
   * - Expiration (`0x06`)
     - 4 octets
   * - Payload config JSON (`0xE1`)
     - \-50 à 100 o
   * - Hash (`0xF2`)
     - 32 octets
   * - Signature (`0xF3`)
     - 64 octets
   * - Authority ID (`0xF4`)
     - 8 octets
   * - Fin (`0xFF`)
     - 0 à 2 octets
   * - **Total**
     - **\-370 à 480 octets**

> Dépend fortement du contenu JSON (nombre de clés/valeurs, formatage compact ou non)

Capsule d’administration (`badge_type: 0x02`)
---------------------------------------------

.. list-table::
   :header-rows: 1

   * - Champ
     - Taille typique
   * - `0xE0` Type
     - 1 octet
   * - `0xE1` Payload chiffré
     - \-64 à 128 o
   * - `0xF2` Hash
     - 32 octets
   * - `0xF3` Signature
     - 64 octets
   * - `0xF4` AuthorityID
     - 8 octets
   * - `0xFF` Fin
     - 0 à 2 octets
   * - **Total**
     - **\-170 à 240 o**

Modes de lecture
================
.. list-table::
   :header-rows: 1

   * - Mode
     - Description
   * - **Libre**
     - Tout TLV valide est accepté, signé ou non
   * - **Bridé**
     - Seules les capsules avec `0xF3` et `0xF4` valides sont autorisées
