Format TLV général
==================

Chaque champ suit la structure TLV :

.. list-table::
   :header-rows: 1
   :widths: 20 20 65

   * - Champ
     - Taille
     - Description
   * - ``Type``
     - 1 octet
     - Identifiant du champ
   * - ``Length``
     - 1 octet
     - Taille du champ ``Value`` en octets
   * - ``Value``
     - N octets
     - Donnée encodée


Les TLV sont chaînés les uns à la suite, l'ordre est libre, **sauf pour la signature qui doit clore la séquence**.

Convention de codage
====================

* **Endianness** : tous les entiers multi-octets (timestamps, identifiants) sont codés **big-endian**.
* **Texte** : chaînes UTF-8 **sans BOM**, maximum strict indiqué par `Length`. Aucun encodage alterné autorisé (ex. UTF-16).
* **Tolérance** : un lecteur peut ignorer les champs inconnus (`Type ∉ [0x01–0xF4]`) s’il est en mode libre. Il doit rejeter les capsules invalides en mode bridé.

.. include:: tag-registry.rst

Détail des champs TLV
=====================

Chaque champ TLV défini dans l'ICF v1 est décrit ci-dessous de manière précise, avec son rôle, sa structure, et ses cas d’usage.

`0x01` – URL du contenu
-----------------------

* **Taille maximale** : 200 octets (UTF-8 sans BOM)
* **Type de données** : chaîne de caractères ASCII ou UTF-8
* **Contenu** : Lien HTTP(S) complet pointant vers une ressource numérique (ex. fichier audio, vidéo, page web…)
* **Exemple** : `https://balabewi.org/audio123.mp3`
* **Obligatoire** : Oui

> Le lien doit être accessible publiquement, sans authentification, et stable dans le temps.

`0x02` –  Langue
----------------

* **Taille maximale** : 2 octets
* **Type de données** : ISO 639-1
* **Contenu** : Code à deux lettres représentant la langue principale du contenu numerique
* **Obligatoire** : Non, mais recommandé
* **Utilité** : 
  * Filtrage de contenu par langue dans une interface multilingue
  * Limitation géographique ou pédagogique selon la langue cible

`0x03` – Titre
--------------

* **Taille maximale** : 64 octets
* **Type de données** : UTF-8
* **Contenu** : Titre lisible du média (ex. : *Histoires de pirates*)
* **Obligatoire** : Non, mais recommandé
* **Utilité** : Affichage dans une interface de supervision ou app mobile, classement, export

`0x04` – Tag pédagogique
------------------------

* **Taille** : 3 octets
* **Structure** :

  * Octet 1 → **Cycle scolaire**
  * Octet 2 → **Matière ou thème**
  * Octet 3 → **Sous-classe libre**
* **Obligatoire** : Non, mais recommandé
* **Utilité** : Filtrage, gouvernance pédagogique, intégration dans un ENT ou interface métier

Tableau des cycles (octet 1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 60

   * - Valeur (hex)
     - Cycle scolaire
   * - ``0x00``
     - Non défini
   * - ``0x01``
     - Cycle 1 (maternelle)
   * - ``0x02``
     - Cycle 2 (CP-CE1-CE2)
   * - ``0x03``
     - Cycle 3 (CM1-CM2-6e)
   * - ``0x04``
     - Cycle 4 (5e-4e-3e)
   * - ``0xFE``
     - Réservé usage local
   * - ``0xFF``
     - Réservé usage futur

Tableau des matières (octet 2)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Valeur (hex)
     - Matière / thème
   * - `0x00`
     - Non défini
   * - `0x01`
     - Lecture / histoire
   * - `0x02`
     - Sciences / nature
   * - `0x03`
     - Musique / chant
   * - `0x04`
     - Langue étrangère
   * - `0x05`
     - Projet personnalisé
   * - `0x06`
     - Mathématiques
   * - `0x07`
     - Éducation civique
   * - `0xFE`
     - Réservé usage local
   * - `0xFF`
     - Réservé usage futur

Sous-classe libre (octet 3)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Utilisation libre par l’émetteur de la capsule (enseignant, app mobile…)
* Peut désigner :
  * un niveau précis (ex. : CE1 → 0x11)
  * un groupe classe (ex. : ULIS → 0x3A)
  * une série pédagogique (ex. : série "Écoute active" → 0x80)
* Valeurs non normalisées à ce jour
  * Si non utilisé : `0x00`

`0x05` – Durée de rétention
---------------------------

* **Taille** : 1 octet
* **Type de données** : entier non signé (uint8)
* **Contenu** : Nombre de jours pendant lesquels le média est conservé localement
* **Valeurs possibles** :

.. list-table::
   :header-rows: 1

   * - Valeur
     - Signification
   * - `0x00`
     - Pas de stockage local
   * - `0x01` – `0xFF`
     - Stockage entre 1 et 255 jours

> Permet de contrôler la place mémoire et l’actualisation automatique du contenu.

`0x06` – Expiration absolue
---------------------------

* **Taille** : 4 octets
* **Type de données** : Timestamp UNIX (uint32 big-endian)
* **Contenu** : Date et heure au-delà de laquelle la capsule n’est plus valable
* **Obligatoire** : Non, mais conseillé dans un cadre scolaire ou temporaire
* **Exemple** : `0x66 87 3C A0` → `2025-12-31T23:59:59Z`

> Nécessite une horloge interne (RTC) ou une synchronisation réseau (NTP) sur le lecteur.

`0xE0` – Type de badge
----------------------

* **Taille** : 1 octet
* **Valeurs possibles** :

  * `0x00` → Badge ressource *(lecture de contenu numérique)*
  * `0x01` → Badge configuration *(paramètres simples non critiques)*
  * `0x02` → Badge administration *(opérations critiques ou sensibles)*
* **Obligatoire** : Non — en son absence, le badge est interprété comme une ressource (`0x00` par défaut)


.. list-table::
   :header-rows: 1

   * - Type
     - Valeur
     - Signature requise
     - Chiffrement requis
     - Persistant
     - Interprétation
   * - Ressource
     - 0x00
     - Optionnelle (requise si mode bridé)
     - Non
     - Non
     - Contenu à lire (audio, vidéo, doc...)
   * - Configuration
     - 0x01
     - Non
     - Non
     - Non
     - Paramétrage simple d’un appareil
   * - Administration
     - 0x02
     - Oui
     - Oui (ECIES)
     - Oui
     - Configuration critique / commandes sensibles

> Les badges de configuration sont interprétés au moment de la lecture et n'ont pas besoin d’être persistés.
> Les badges d’administration peuvent modifier de façon persistante la configuration du lecteur (ex: clés Wi-Fi, endpoints, règles de sécurité…).

`0xE1` – Données système (Payloads structurés)
----------------------------------------------

* **Taille** : variable
* **Contenu** : Charge utile structurée (ex. paramètres de configuration ou commandes internes)
* **Persistance** : dépend du type de badge (voir tableau ci-dessus)
* **Encodage recommandé** : la `Value` contient **exclusivement une structure JSON valide**. Toute autre forme d'encodage (binaire, CBOR, texte libre) est interdite.


Badge de ressource avec configuration (`badge_type: 0x00` + `0xE1`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dans certains contextes (lieux publics, médiathèques, écoles), une capsule de type ressource peut inclure un champ `0xE1` contenant des **paramètres de lecture temporaires**, au format **JSON clair**.

* Ce champ est optionnel.
* Les paramètres sont **appliqués uniquement pendant la lecture** et ne modifient **pas la configuration durable** de l'appareil.
* Les lecteurs peuvent choisir d’ignorer ces options si la politique locale de sécurité l’exige.


Badge de configuration (`badge_type: 0x01`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Le champ `0xE1` contient des données **en clair**, directement interprétables par le lecteur.
* Ces données encodent des paramètres simples : volume, mise en veille, ambiance lumineuse, etc.
* La structure exacte doit être connue du firmware pour que la configuration soit appliquée correctement.

> Un seul TLV `0xE1` est attendu par badge. Si plusieurs sont présents, seul le premier peut être pris en compte.

Badge d’administration (`badge_type: 0x02`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Le champ `0xE1` d’un badge de type `0x02` contient une **donnée chiffrée**, représentant une commande ou un paramètre critique destiné à être appliqué de manière persistante sur un ou plusieurs appareils.
* Il est **systématiquement chiffré** via **ECIES/X25519**, à l’aide de la **clé publique dérivée de `SK_admin`**, une clé privée partagée et installée localement sur un groupe d'appareils appairés.
* Ce mécanisme permet de **chiffrer la donnée une seule fois**, tout en la rendant **déchiffrable par tous les appareils** du groupe.

> Ce modèle est sécurisé tant que :
>
> * la donnée est considérée comme **commune au groupe**,
> * la clé privée `SK_admin` est **protégée localement** (par exemple via chiffrement de la flash),
> * la capsule est **signée par une autorité de confiance**.

* Le contenu du champ `0xE1` est une **structure JSON sérialisée**, chiffrée via ECIES, puis **encodée en base64**.
* La **signature Ed25519** (champ `0xF3`) atteste que le badge provient d’un émetteur autorisé, identifié via le champ `0xF4` (`authority_id`).

`0xF3` – Signature cryptographique
----------------------------------

* **Taille** : 64 octets
* **Algorithme** : Ed25519
* **Contenu** : Signature de `0xF2` à l’aide d’une clé privée locale
* **Généré par** : l’application officielle ou un outil CLI sécurisé

> Signé à partir du hash SHA256 (champ `0xF2`)
> Doit être présent **avec** un champ `0xF4` pour être exploitable par un lecteur sécurisé

`0xF4` – Authority ID
---------------------

* **Taille** : 8 octets
* **Type** : identifiant unique d’autorité (uint64 ou chaîne fixe)
* **Contenu** : Permet au lecteur de savoir quelle clé publique utiliser pour vérifier la signature
* **Exemple** : `01 23 45 67 89 AB CD EF`

> Le champ `AuthorityID` est essentiel si plusieurs autorités de confiance doivent coexister sur un même appareil.
> Il permet au lecteur de savoir **quelle clé publique utiliser** pour vérifier la signature.
> Chaque autorité locale (par exemple : école, structure, éditeur) peut disposer de sa propre paire de clés.

`0xFF` – Marqueur de fin
------------------------

* **Taille** : 0 octet
* **Utilité** : Optionnelle — peut marquer explicitement la fin d’une capsule
* **Interprétation** : Indique qu’aucun champ ne suit

# Addendum — Profils, Readers, et NDEF (aligné sur TLV v1)

Ce document complète SPEC-ICF.md sans modifier la table TLV existante.
