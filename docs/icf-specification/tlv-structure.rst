Format TLV général
==================

Chaque capsule ICF est composée d’une suite de champs **TLV** (*Type – Length – Value*).

Structure générique
-------------------

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

Les TLV sont chaînés les uns à la suite.  
L’ordre est libre, **sauf pour la signature (`0xF3`) qui doit clore la séquence**.

Conventions de codage
---------------------

* **Endianness** : tous les entiers multi-octets (timestamps, identifiants) sont en **big-endian**.
* **Texte** : chaînes UTF-8 **sans BOM**, longueur maximale strictement indiquée par `Length`. Aucun encodage alternatif (UTF-16, etc.) n’est autorisé.

.. tip::
   En lecture, le parseur TLV **doit** parcourir la capsule séquentiellement et valider chaque champ avant de passer au suivant.  
   La présence du champ `0xFF` n’est pas obligatoire, mais s’il est présent, il marque explicitement la fin.

.. include:: tag-registry.rst

Détail des champs TLV
=====================

Chaque champ TLV défini dans l'ICF est décrit ci-dessous de manière précise, avec son rôle, sa structure, et ses cas d’usage.

.. _tag_0x01:

`0x01` – URL du contenu
-----------------------

* **Taille maximale** : 200 octets (UTF-8 sans BOM)
* **Type de données** : chaîne de caractères ASCII ou UTF-8
* **Contenu** : Lien HTTP(S) complet pointant vers une ressource numérique (ex. fichier audio, vidéo, page web…)
* **Exemple** : `https://balabewi.org/audio123.mp3`
* **Obligatoire** : Oui

.. note::
  Le lien doit être accessible publiquement, sans authentification, et stable dans le temps.

.. _tag_0x02:

`0x02` –  Langue
----------------

* **Taille maximale** : 2 octets
* **Type de données** : ISO 639-1
* **Contenu** : Code à deux lettres représentant la langue principale du contenu numerique
* **Obligatoire** : Non, mais recommandé
* **Utilité** : 
  
  * Filtrage de contenu par langue dans une interface multilingue
  * Limitation géographique ou pédagogique selon la langue cible

.. _tag_0x03:

`0x03` – Titre
--------------

* **Taille maximale** : 64 octets
* **Type de données** : UTF-8
* **Contenu** : Titre lisible du média (ex. : *Histoires de pirates*)
* **Obligatoire** : Non, mais recommandé
* **Utilité** : Affichage dans une interface de supervision ou app mobile, classement, export

.. _tag_0x04:

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

.. _tag_0x05:

`0x05` – Durée de rétention
---------------------------

* **Taille** : 1 octet
* **Type de données** : entier non signé (uint8)
* **Contenu** : Nombre de jours pendant lesquels le média est conservé localement
* **Obligatoire** : Non, mais conseillé dans un cadre scolaire ou temporaire
* **Valeurs possibles** :
 * ``0x00`` Pas de stockage local (lecture en direct uniquement)
 * ``0x01 – 0xFF`` Stockage entre 1 et 255 jours
  
.. note::
   Un lecteur peut ajuster ou ignorer cette valeur si une politique plus restrictive
   (ex. `0x07 – SourcePolicy` ou règle locale) est en vigueur.

.. tip::
   Utilisez ce champ pour optimiser la place mémoire et planifier l’actualisation automatique du contenu.

.. _tag_0x06:

`0x06` – Expiration absolue
---------------------------

* **Taille** : 4 octets
* **Type de données** : Timestamp UNIX (uint32 big-endian)
* **Contenu** : Date et heure au-delà de laquelle la capsule n’est plus valable
* **Obligatoire** : Non, mais conseillé dans un cadre scolaire ou temporaire
* **Exemple** : `0x66 87 3C A0` → `2025-12-31T23:59:59Z`

.. note::
   Nécessite une horloge interne (RTC) ou une synchronisation réseau (NTP) sur le lecteur.  
   Un lecteur peut ajuster ou ignorer cette valeur si une politique plus restrictive
   (ex. `0x07 – SourcePolicy` ou règle locale) est en vigueur.

.. _tag_0x07:

`0x07` – SourcePolicy
---------------------

* **Taille** : 3 à 11 octets  
* **Type de données** : structure binaire compacte  
* **Obligatoire** : Oui
* **Contenu** : Politique d’usage et de conservation définie par l’éditeur ou la source, signée dans la capsule.

**Structure** :

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Octet(s)
     - Champ
     - Description
   * - 0
     - Version
     - Version du sous-format (actuellement ``0x01``).  
  
       Si inconnue → politique restrictive (pas de cache persistant).
   * - 1
     - Classe source
     - Typologie de la provenance (voir :ref:`sp_classes`).
   * - 2
     - Flags cache
     - Bits de contrôle (voir :ref:`sp_flags`).
   * - 3–N
     - AgreementID *(optionnel)*
     - Présent uniquement si la **classe** ou la **politique locale** 
  
       l’exige. 4 à 8 octets (identifiant contractuel, hash ou numéro 
      
       séquentiel signé).

.. note::
   - **Taille minimale** : 3 octets (version + classe + flags)  
   - **Taille complète** : jusqu’à 11 octets (avec AgreementID 8 octets)  
.. _sp_classes:

Classes de source (octet 1)
---------------------------

``0x00`` — **self_hosted**  
  Contenu auto-hébergé par l’émetteur. Cache persistant autorisé si la politique locale le permet.  
  Chiffrement recommandé.

``0x01`` — **api_restreinte**  
  Ressource issue d'une API avec conditions d'utilisation strictes.  
  Par défaut : pas de cache persistant, sauf accord explicite.

``0x02`` — **flux_restreint**  
  Ressource issue d'un flux (RSS/Atom) avec limitations contractuelles de durée.  
  Revalidation conseillée, cache soumis aux conditions de la politique en vigueur.

``0x03`` — **licence_libre**  
  Contenu sous licence libre. Politique locale généralement permissive.

``0xFF`` — **autre**  
  Toute autre source nécessitant une définition explicite des règles.

.. _sp_flags:

Flags de cache (octet 2)
------------------------

Le champ **Flags** est un **masque de bits** codé sur un octet (u8).  
Chaque bit correspond à une option, numérotée du **bit 0** (poids faible, valeur 1) au **bit 7** (poids fort, valeur 128).  
Plusieurs options peuvent être activées simultanément en additionnant leurs valeurs.

``0 (0x01)`` — **ALLOW_CACHE**  
  Autorise le cache persistant si la politique locale le permet.

``1 (0x02)`` — **DEVICE_BOUND**  
  Chiffrement lié au device. Un média extrait ne doit pas être lisible ailleurs.

``2 (0x04)`` — **BADGE_BOUND**  
  Accès conditionné à la présence du badge.  
  Le média est chiffré avec une clé dérivée incluant un identifiant stable.

``3 (0x08)`` — **EPHEMERAL_ONLY**  
  Lecture uniquement en streaming/buffering. Implique ALLOW_CACHE=0.

**Exemples de combinaison** :

- ``ALLOW_CACHE`` + ``DEVICE_BOUND`` + ``BADGE_BOUND``  
  → binaire : ``00000111`` → hexadécimal : ``0x07``
- ``EPHEMERAL_ONLY`` seul  
  → binaire : ``00001000`` → hexadécimal : ``0x08``

.. note::
   - Les bits non définis doivent être ignorés (valeur future) et considérés comme à ``0`` par les implémentations actuelles.
   - Si ``EPHEMERAL_ONLY`` est activé, ``ALLOW_CACHE`` doit être à 0.



.. _tag_0xE0:

`0xE0` – Type de badge
----------------------

* **Taille** : 1 octet
* **Type de données** : masque de bits (uint8)
* **Obligatoire** : Non — en son absence, le badge est interprété comme une ressource (``0x01`` par défaut).
* **Valeurs possibles** :

``0 (0x01)`` — **RESOURCE**  
  * Badge donnant accès à un contenu numérique (audio, vidéo, doc…).

``1 (0x02)`` — **CONFIGURATION**  
  * Contient des paramètres de configuration non critiques (volume, ambiance lumineuse…). 
  *  il modifie de facon temporaire la configuration du lecteur.

``2 (0x04)`` — **ADMINISTRATION**  
  * Donne accès à des opérations critiques ou sensibles (commande système, config réseau, sécurité…).
  * il modifie de facon persistante la configuration du lecteur.
  * La signature est requise et le chiffrement obligatoire (ECIES).

``3 - 7`` — **RESERVED**  
  * Doit être à 0 pour compatibilité future.

.. note::
   - Les bits non définis doivent être ignorés (valeur future) et considérés comme à ``0`` par les implémentations actuelles.

.. _tag_0xE1:

`0xE1` – Données structurées (Payloads structurés)
--------------------------------------------------

* **Taille** : variable
* **Type de données** :  
  
  * Pour les badges **en clair** (`0x01`, `0x02`) : JSON UTF-8 **sans BOM**, la ``Value`` doit contenir **exclusivement** une structure JSON **valide**. Toute autre forme (binaire brut, CBOR, texte libre) est **interdite**.  
  * Pour les badges **chiffrés** (`0x04`) : Bloc binaire chiffré (opaque) contenant un JSON valide après déchiffrement.

* **Contenu** : Charge utile structurée (ex. paramètres de configuration ou commandes internes)

Badge de configuration (`badge_type: 0x02`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Le champ `0xE1` contient des données **en clair**, directement interprétables par le lecteur.
* Ces données encodent des paramètres simples : volume, mise en veille, ambiance lumineuse, etc.
* La structure exacte doit être connue du firmware pour que la configuration soit appliquée correctement.

Badge d’administration (`badge_type: 0x04`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Le champ `0xE1` contient des données **chiffrées**, représentant une commande ou un paramètre critique destiné à être appliqué de manière persistante sur un ou plusieurs appareils.
* Il est **systématiquement chiffré** suivent les mécanismes normatifs décrits en :ref:`sec_payload_admin`.


Badge de ressource avec configuration ( `badge_type: 0x01 + 0x02→ 0x03` )
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dans certains contextes (lieux publics, médiathèques, écoles), une capsule de type ressource peut inclure des **paramètres de lecture temporaires**.

* Le champ `0xE1` contient des données **en clair**, directement interprétables par le lecteur.
* Les paramètres sont **appliqués uniquement pendant la lecture** et ne modifient **pas la configuration durable** de l'appareil.
* Les lecteurs peuvent choisir d’ignorer ces options si la politique locale de sécurité l’exige.


.. _tag_0xF2:

0xF2 – Hash
-----------
* **Taille maximale** : 32 octets  
* **Type de données** : hash binaire SHA-256  
* **Contenu** : Valeur du hash SHA-256 calculée sur **tous les TLV précédents**, dans l’ordre de la capsule, **sans inclure `0xF2`, `0xF3`, `0xF4` et `0xFF`**.  
* **Utilité** : Garantir l’intégrité du contenu et permettre la vérification de signature (`0xF3`).  
* **Obligatoire** : Oui  

.. note::
  Le hash doit être calculé strictement sur les octets TLV (tag, taille, valeur), et non sur leur représentation textuelle.

.. _tag_0xF3:

`0xF3` – Signature cryptographique
----------------------------------

* **Taille** : 64 octets
* **Type de données** : Signature numérique
* **Contenu** : Signature du hash SHA-256 (champ ``0xF2``) à l’aide d’une clé privée liée à l’autorité déclarée dans ``0xF4``.
* **Obligatoire** : Non — sauf en mode bridé ou si exigé par la politique source.


.. note::
  * Les algorithmes, formats et procédures sont détaillés en :ref:`sec_signature`.  
  * Ce champ **doit** être présent **avec** ``0xF4`` pour être exploitable par un lecteur sécurisé.

.. _tag_0xF4:

`0xF4` – Authority ID
---------------------

* **Taille** : 8 octets
* **Type de données** : Identifiant unique d’autorité (uint64 ou chaîne fixe)
* **Contenu** : Identifie l’autorité émettrice afin de sélectionner la clé publique appropriée pour vérifier la signature associée.
* **Obligatoire** : Non — sauf en mode bridé ou si exigé par la politique source.

.. note::
   Les formats, usages et règles de gestion des autorités sont détaillés en :ref:`sec_authorities`.  
   Ce champ **doit** être présent **avec** ``0xF3`` pour permettre la vérification de signature dans un lecteur sécurisé.

.. _tag_0xFF:

`0xFF` – Marqueur de fin
------------------------

* **Taille** : 0 octet
* **Utilité** : Optionnelle — peut marquer explicitement la fin d’une capsule
* **Interprétation** : Indique qu’aucun champ ne suit

Espace utilisé
==============

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
   * - `0x07` SourcePolicy
     - 8 octets
   * - `0xF2` Hash
     - 32 octets
   * - `0xF3` Signature
     - 64 octets
   * - `0xF4` AuthorityID
     - 8 octets
   * - `0xFF` Fin
     - 0 à 2 octets
   * - **Total**
     - **\-338 à 438 o**

Capsule de configuration (`badge_type: 0x01`)
---------------------------------------------

.. list-table::
   :header-rows: 1

   * - Champ
     - Taille typique
   * - `0xE0` Type
     - 1 o
   * - `0xE1` Payload JSON
     - 30 à 150 o
   * - `0x07` SourcePolicy
     - 8 octets
   * - `0xF2` Hash (SHA-256)
     - 32 o
   * - `0xF3` Signature (Ed25519)
     - 64 o
   * - `0xF4` AuthorityID
     - 8 o
   * - `0xFF` Fin
     - 0 à 2 o
   * - **Total**
     - **≈ 143 à 293 o**

> Dépend fortement du contenu JSON (nombre de clés/valeurs, formatage compact ou non)

Capsule de ressource avec configuration (`badge_type: 0x00 + 0xE1`)
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
   * - SourcePolicy (`0x07`)
     - 8 octets
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
     - **\-378 à 488 o**

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
   * - `0x07` SourcePolicy
     - 8 octets
   * - `0xF2` Hash
     - 32 octets
   * - `0xF3` Signature
     - 64 octets
   * - `0xF4` AuthorityID
     - 8 octets
   * - `0xFF` Fin
     - 0 à 2 octets
   * - **Total**
     - **\-178 à 248 o**
