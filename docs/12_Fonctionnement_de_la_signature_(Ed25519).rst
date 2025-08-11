Fonctionnement de la signature (Ed25519)

-  La signature est réalisée **par l’app mobile**, qui détient une **clé
   privée locale**.

-  L’app :

   1. Construit les TLV à signer (``0x01``, ``0x02``, ``0x03``,
      ``0x04``, ``0x05``, ``0x06``, etc.)
   2. Calcule le SHA256 du buffer TLV
   3. Signe ce hash avec la clé privée (Ed25519)
   4. Ajoute les TLV ``0xF2``, ``0xF3``, ``0xF4``

-  Le lecteur, s’il est bridé, ne lit **que les capsules signées par une
   clé publique reconnue**, identifiée grâce au champ ``0xF4``.

--------------

12.1 Exemple d’un badge en format JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

12.2 Badge de ressource (``badge_type: 0x00``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Minimal :
^^^^^^^^^

.. code:: json

   {
     "url": "https://balabewi.org/audio123.mp3",
     "language": "fr",
     "title": "Histoires de pirates",
     "tag": {
       "cycle": 1,
       "subject": 1,
       "sub": 0
     },
     "retention": 7,
     "expires": 1767225599,
     "authority_id": "0x0123456789ABCDEF"
   }

Complet :
^^^^^^^^^

.. code:: json

   {
     "url": "https://balabewi.org/audio123.mp3",
     "language": "fr",
     "title": "Histoires de pirates",
     "tag": {
       "cycle": 1,
       "subject": 1,
       "sub": 0
     },
     "retention": 7,
     "expires": 1767225599,
     "hash": "bdc9aaf329d204cdefb71884a91ce08987c9a91b657f3f4583a6c88e3c58ad71",
     "signature": "6b871e50c723011c6ab345e847c10d89d0a2604bced7e7c9d0fa1c8fd8fbd2b91d8df6c86156e15d1de9e68e5b4c8c7760b13ef6de25035178135eb79ab7d208",
     "authority_id": [1, 35, 69, 103, 137, 171, 205, 239]
   }

Avec paramètre de configuration :
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: json

   {
     "badge_type": 0,
     "url": "https://balabewi.org/audio123.mp3",
     "language": "fr",
     "title": "Histoires de pirates",
     "tag": {
       "cycle": 1,
       "subject": 1,
       "sub": 0
     },
     "retention": 7,
     "expires": 1767225599,
     "authority_id": "0x0123456789ABCDEF",
     "system_payload": {
       "volume": 50,
       "ambience": "bright",
       "lock_buttons": true
     }
   }

12.3 Badge de configuration (``badge_type: 0x01``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ce type de badge permet de configurer des paramètres simples du lecteur,
sans chiffrement ni signature obligatoire.

.. code:: json

   {
     "badge_type": 1,
     "system_payload": {
       "volume": 70,
       "sleep_timeout": 120,
       "ambience": "calm"
     }
   }

12.4 Badge d’administration (``badge_type: 0x02``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour respecter la spécification, le contenu d’un badge d’administration
(``badge_type: 2``) ne doit **jamais** exposer des données en clair dans
le champ ``system_payload``. Le contenu JSON original est d’abord
sérialisé, puis chiffré via ECIES, puis encodé en base64. Le champ
``system_payload`` dans l’exemple JSON est une chaîne binaire chiffrée
(souvent encodée en Base64 dans les outils). Elle ne peut être
interprétée qu’après déchiffrement par un lecteur équipé de la bonne
clé.

.. code:: json

   {
     "badge_type": 2,
     "system_payload": "BASE64(ECIES(payload JSON))",
     "signature": "<signature_ed25519>",
     "authority_id": [1, 35, 69, 103, 137, 171, 205, 239]
   }

--------------
