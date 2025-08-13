Mécanisme de vérification (lecteur)
===================================

Le lecteur peut être configuré en 2 modes :

| Mode      | Comportement                                                          |
| --------- | --------------------------------------------------------------------- |
| **Libre** | Accepte tout tag TLV valide, qu'il soit signé ou non                  |
| **Bridé** | Accepte uniquement les capsules **signées par une autorité reconnue** |

Dans ce second cas :

* `0xF3` (signature) et `0xF4` (authority ID) doivent être présents,
* la signature est vérifiée via une clé publique préenregistrée dans le lecteur,
* l’identifiant `AuthorityID` permet de sélectionner la bonne clé publique dans la liste embarquée.


Fonctionnement de la signature (Ed25519)
========================================

* La signature est réalisée **par l’app mobile**, qui détient une **clé privée locale**.

* L’app :

  1. Construit les TLV à signer (`0x01`, `0x02`, `0x03`, `0x04`, `0x05`, `0x06`, etc.)
  2. Calcule le SHA256 du buffer TLV
  3. Signe ce hash avec la clé privée (Ed25519)
  4. Ajoute les TLV `0xF2`, `0xF3`, `0xF4`

* Le lecteur, s’il est bridé, ne lit **que les capsules signées par une clé publique reconnue**, identifiée grâce au champ `0xF4`.


Sécurité cryptographique et gestion des clés
============================================

Le format ICF intègre un modèle de sécurité basé sur une **signature Ed25519** pour authentifier l’émetteur, et, dans le cas des badges d’administration (`badge_type: 0x02`), sur un **chiffrement asymétrique ECIES/X25519** du champ `0xE1`.
Deux approches sont possibles pour le chiffrement de la donnée sensible :

Solution retenue — Clé partagée entre lecteurs (`SK_admin`)
-----------------------------------------------------------

* Une clé privée `SK_admin` est **générée une seule fois** par l’application mobile (ou la CLI) lors de l’initialisation.
* Elle est **copiée localement sur chaque appareil** au moment de l’appairage (via une session chiffrée ou flash encryption).
* Le champ `0xE1` du badge est chiffré **une seule fois** avec la **clé publique dérivée de `SK_admin`** (via X25519).
* Chaque lecteur peut déchiffrer cette donnée localement.
* Ce modèle est :

  * **simple** (un seul chiffrement pour N lecteurs),
  * **efficace** (espace optimisé sur la puce),
  * **suffisamment sûr** si le firmware utilise le **chiffrement de flash actif** (flash encryption),
  * **interopérable** (le badge est lisible par tous les lecteurs appairés).

> **Remarque** : la clé `SK_admin` n'est jamais exposée dans le badge, seule sa dérivée publique l’est, dans le cadre du chiffrement ECIES.

.. mermaid::

   flowchart TB

       SK_sig[Clé privée de signature<br>SK_sig Ed25519]:::priv
       PK_sig[Clé publique de signature<br>PK_sig Ed25519]:::pub
       PK_sig_local[Clé publique de signature<br>PK_sig Ed25519]:::pub
       SK_master[Clé maître de groupe<br>SK_master X25519]:::priv
       SK_admin[Clé ECIES partagée<br>SK_admin ]:::priv
       PK_admin[Clé publique ECIES<br>PK_admin]:::pub
       authority_id[Authority ID  <br>ex: 0x012345...]:::meta
       pub_registry[Table des autorités<br>authority_id → PK_sig]:::tab
       pub_table[Table embarquée<br>authority_id → PK_sig]:::pub
       SK_admin_local[SK_admin stockée localement<br> volume  chiffré]:::priv

       %% Phase 1 : Génération des clés côté émetteur
       subgraph Client["Construction (App mobile / CLI)"]
           direction TB
           SK_sig -->|génère| PK_sig
           authority_id  -->|indexée dans| pub_registry
           PK_sig -->|indexée dans| pub_registry

           SK_master -->|dérive| SK_admin
           SK_admin -->|génère| PK_admin
       end

       %% Phase 2 : Configuration initiale du lecteur
       subgraph Lecteur["Interprétation (Lecteur Balabewi)"]
           direction TB
           pub_registry -->|copiée| pub_table
           SK_admin -->|copiée vers lecteur| SK_admin_local
       end

       %% Construction de la capsule
       subgraph Client["Construction (App mobile / CLI)"]
           direction TB
           SK_sig -->|signe F2 : SHA256 des TLV| capsule_f3[Signature]
           authority_id -->|copié dans capsule| capsule_f4[Authority ID]
           PK_admin -->|chiffre payload JSON| capsule_e1[Payload chiffré]
       end

       %% Capsule
       subgraph Capsule["Capsule CIF"]
           capsule_f3 --> 0xF3
           capsule_f4 --> 0xF4
           capsule_e1 --> 0xF1
       end

       %% Utilisation côté lecteur
       subgraph Lecteur["Interprétation (Lecteur Balabewi)"]
           direction TB

           0xF4 -->|lookup - authority_id| pub_table
           0xF3 -->|verify - signature| PK_sig_local
           0xF1 -->|decrypt - payload| SK_admin_local
           pub_table --> |extarct| PK_sig_local
           PK_sig_local --> |valide|cap[IOBEWI Capsule]
           SK_admin_local --> |Déchiffre| Payload
       end