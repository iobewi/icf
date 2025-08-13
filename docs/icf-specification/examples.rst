============================================
Exemples de badges (format JSON illustratif)
============================================

Badge de ressource (``badge_type: 0``) — minimal
------------------------------------------------

.. code-block:: json

   {
     "url": "https://balabewi.org/audio123.mp3",
     "language": "fr",
     "title": "Histoires de pirates",
     "tag": { "cycle": 1, "subject": 1, "sub": 0 },
     "retention": 7,
     "expires": 1767225599,
     "authority_id": "0x0123456789ABCDEF"
   }

Badge de ressource — complet
----------------------------

.. code-block:: json

   {
     "url": "https://balabewi.org/audio123.mp3",
     "language": "fr",
     "title": "Histoires de pirates",
     "tag": { "cycle": 1, "subject": 1, "sub": 0 },
     "retention": 7,
     "expires": 1767225599,
     "hash": "bdc9aaf329d204cdefb71884a91ce08987c9a91b657f3f4583a6c88e3c58ad71",
     "signature": "6b871e50c723011c6ab345e847c10d89d0a2604bced7e7c9d0fa1c8fd8fbd2b91d8df6c86156e15d1de9e68e5b4c8c7760b13ef6de25035178135eb79ab7d208",
     "authority_id": [1, 35, 69, 103, 137, 171, 205, 239]
   }

Badge de ressource avec configuration temporaire
------------------------------------------------

.. code-block:: json

   {
     "badge_type": 0,
     "url": "https://balabewi.org/audio123.mp3",
     "language": "fr",
     "title": "Histoires de pirates",
     "tag": { "cycle": 1, "subject": 1, "sub": 0 },
     "retention": 7,
     "expires": 1767225599,
     "authority_id": "0x0123456789ABCDEF",
     "system_payload": { "volume": 50, "ambience": "bright", "lock_buttons": true }
   }

Badge de configuration (``badge_type: 1``)
------------------------------------------

.. code-block:: json

   {
     "badge_type": 1,
     "system_payload": {
       "volume": 70,
       "sleep_timeout": 120,
       "ambience": "calm"
     }
   }

Badge d’administration (``badge_type: 2``)
------------------------------------------

.. code-block:: json

   {
     "badge_type": 2,
     "system_payload": "BASE64(ECIES(payload JSON))",
     "signature": "<signature_ed25519>",
     "authority_id": [1, 35, 69, 103, 137, 171, 205, 239]
   }