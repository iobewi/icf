Espace utilisé sur NTAG215 (504 octets max)

13.1 Capsule de ressource (``badge_type: 0x00``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

==================== =================
Champ                Taille typique
==================== =================
``0x01`` URL         ~120 à 200 octets
``0x02`` Langue      2 octets
``0x03`` Titre       ~32 à 64 octets
``0x04`` Tag péd.    3 octets
``0x05`` Rétention   1 octet
``0x06`` Expiration  4 octets
``0xF2`` Hash        32 octets
``0xF3`` Signature   64 octets
``0xF4`` AuthorityID 8 octets
``0xFF`` Fin         0 à 2 octets
**Total**            **~330 à 430 o**
==================== =================

13.2 Badge de configuration (``badge_type: 0x01``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

===================== ===============
Champ                 Taille typique
===================== ===============
``0xE0`` Type         1 octet
``0xE1`` Payload JSON ~30 à 150 o
``0xFF`` Fin          0 à 2 octets
**Total**             **~40 à 160 o**
===================== ===============

..

   Dépend fortement du contenu JSON (nombre de clés/valeurs, formatage
   compact ou non)

13.3 Capsule de ressource avec configuratioon (``badge_type: 0x00 + 0xE1``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

============================== =====================
Champ                          Taille typique
============================== =====================
URL (``0x01``)                 ~120 à 200 octets
Langue (``0x02``)              2 octets
Titre (``0x03``)               ~32 à 64 octets
Tag pédagogique (``0x04``)     3 octets
Rétention (``0x05``)           1 octet
Expiration (``0x06``)          4 octets
Payload config JSON (``0xE1``) ~50 à 100 o
Hash (``0xF2``)                32 octets
Signature (``0xF3``)           64 octets
Authority ID (``0xF4``)        8 octets
Fin (``0xFF``)                 0 à 2 octets
**Total**                      **~370 à 480 octets**
============================== =====================

..

   Dépend fortement du contenu JSON (nombre de clés/valeurs, formatage
   compact ou non)

13.4 Badge d’administration (``badge_type: 0x02``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

======================== ================
Champ                    Taille typique
======================== ================
``0xE0`` Type            1 octet
``0xE1`` Payload chiffré ~64 à 128 o
``0xF2`` Hash            32 octets
``0xF3`` Signature       64 octets
``0xF4`` AuthorityID     8 octets
``0xFF`` Fin             0 à 2 octets
**Total**                **~170 à 240 o**
======================== ================

--------------
