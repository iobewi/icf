ICF Tag Registry
================

Ce registre répertorie les tags TLV définis dans la version 1 de la spécification ICF.

.. list-table::
   :header-rows: 1
   :widths: 15 20 10 55

   * - Type (hex)
     - Nom
     - Taille max
     - Description
   * - ``0x01``
     - URL
     - 200 o
     - Lien HTTP(S) complet vers une ressource numérique
   * - ``0x02``
     - Langue
     - 2 o
     - Code langue ISO 639-1 (``fr``, ``en``, ``es``…)
   * - ``0x03``
     - Titre
     - 64 o
     - Titre optionnel du média (UTF-8)
   * - ``0x04``
     - Tag pédagogique
     - 3 o
     - Octet 1 : cycle, Octet 2 : matière, Octet 3 : sous-classe
   * - ``0x05``
     - Rétention
     - 1 o
     - Durée de conservation locale (jours, 0 = non stocké)
   * - ``0x06``
     - Expiration
     - 4 o
     - Timestamp d’expiration absolue (UNIX, big-endian)
   * - ``0xE0``
     - Type badge
     - 1 o
     - 0=ressource, 1=configuration, 2=administration
   * - ``0xE1-0xEF``
     - Payload sys.
     - variable
     - Données de config ou commandes admin (JSON)
   * - ``0xF2``
     - Hash
     - 32 o
     - SHA256 calculé sur les TLV précédents
   * - ``0xF3``
     - Signature
     - 64 o
     - Signature du hash par autorité (Ed25519)
   * - ``0xF4``
     - AuthorityID
     - 8 o
     - Identifiant de l’autorité ayant signé le contenu
   * - ``0xFF``
     - Fin
     - 0 o
     - (optionnel) marqueur de fin de capsule
