Types de badges et sécurité
===========================

Le format ICF définit plusieurs types de badges, chacun répondant à des objectifs
différents : diffusion de ressources, configuration d’un appareil ou administration.
Chaque type applique des exigences distinctes en matière de signature, chiffrement
et persistance.

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

Fonctionnement de la signature (Ed25519)
========================================

Le mécanisme de signature garantit l’authenticité et l’intégrité de la capsule.

* La signature est générée **par l’application mobile** ou la **CLI**, qui détient la clé privée.
* Processus côté émetteur :
  
  1. Construction des TLV à signer (`0x01`, `0x02`, `0x03`, `0x04`, `0x05`, `0x06`, etc.)
  2. Calcul du hash SHA-256 du buffer TLV
  3. Signature de ce hash avec la clé privée (Ed25519)
  4. Ajout des TLV `0xF2` (hash), `0xF3` (signature) et `0xF4` (AuthorityID)

* Côté lecteur en mode bridé : seules les capsules signées par une clé publique reconnue
sont acceptées, la clé étant identifiée via le champ `0xF4`.

Sécurité cryptographique et gestion des clés
============================================

Le modèle de sécurité ICF repose sur :
- une **signature Ed25519** pour authentifier l’émetteur,
- un **chiffrement asymétrique ECIES/X25519** pour protéger les données sensibles
  (`0xE1`) des badges d’administration (`badge_type: 0x02`).

Solution retenue — Clé partagée entre lecteurs (`SK_admin`)
-----------------------------------------------------------

* Une clé privée `SK_admin` est générée une seule fois par l’application mobile ou la CLI.
* Elle est copiée localement sur chaque lecteur lors de l’appairage sécurisé.
* Le champ `0xE1` est chiffré une fois avec la clé publique dérivée de `SK_admin` (via X25519).
* Tous les lecteurs appairés peuvent déchiffrer localement la donnée.
* Avantages :
  - **Simple** : un seul chiffrement pour N lecteurs,
  - **Efficace** : économie d’espace sur la puce,
  - **Sûr** : si le firmware active le chiffrement du flash,
  - **Interopérable** : lisible par tous les lecteurs appairés.

> **Remarque** : la clé `SK_admin` n'est jamais exposée dans le badge ; seule sa clé publique est utilisée pour le chiffrement.

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
