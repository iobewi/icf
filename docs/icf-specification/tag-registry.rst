ICF Tag Registry
================

Ce registre répertorie les tags TLV définis dans la spécification ICF.

.. list-table::
   :header-rows: 1
   :widths: 12 22 12 16 38

   * - Type (hex)
     - Nom
     - Taille
     - Obligatoire
     - Description
   * - ``0x01``
     - :ref:`URL <tag_0x01>`
     - 200 o
     - Oui
     - Lien HTTP(S) complet vers une ressource numérique
   * - ``0x02``
     - :ref:`Langue <tag_0x02>`
     - 2 o
     - Non (recommandé)
     - Code langue ISO 639-1 (``fr``, ``en``, ``es``…)
   * - ``0x03``
     - :ref:`Titre <tag_0x03>`
     - 64 o
     - Non (recommandé)
     - Titre lisible du média (UTF-8)
   * - ``0x04``
     - :ref:`Tag pédagogique <tag_0x04>`
     - 3 o
     - Non (recommandé)
     - Octet 1 : cycle, Octet 2 : matière, Octet 3 : sous-classe
   * - ``0x05``
     - :ref:`Rétention <tag_0x05>`
     - 1 o
     - Non (conseillé)
     - Durée de conservation locale (jours). Le lecteur peut l’ajuster si une politique plus stricte s’applique.
   * - ``0x06``
     - :ref:`Expiration <tag_0x06>`
     - 4 o
     - Non (conseillé)
     - Timestamp d’expiration absolue (UNIX, big-endian)
   * - ``0x07``
     - :ref:`SourcePolicy <tag_0x07>`
     - 3–11 o
     - Oui
     - Typologie de la source, flags de cache, AgreementID (optionnel). Cadre d’usage signé et appliqué côté lecteur.
   * - ``0xE0``
     - :ref:`Type de badge (flags) <tag_0xE0>`
     - 1 o
     - Non
     - Masque de bits : RESOURCE/CONFIGURATION/ADMINISTRATION. Défaut : RESOURCE si absent.
   * - ``0xE1``
     - :ref:`Payloads structurés <tag_0xE1>`
     - variable
     - Conditionnel
     - Données de config/commandes : JSON en clair (CONFIG/RESOURCE) ou bloc chiffré (ADMIN).
   * - ``0xF2``
     - :ref:`Hash <tag_0xF2>`
     - 32 o
     - Oui
     - SHA-256 sur les TLV précédents (hors ``0xF2``, ``0xF3``, ``0xF4``, ``0xFF``)
   * - ``0xF3``
     - :ref:`Signature <tag_0xF3>`
     - 64 o
     - Conditionnel
     - Signature du hash ; requise en **mode bridé** ou si la politique l’exige (utilisée avec ``0xF4``).
   * - ``0xF4``
     - :ref:`AuthorityID <tag_0xF4>`
     - 8 o
     - Conditionnel
     - Identifiant d’autorité pour sélectionner la clé publique de vérification (utilisé avec ``0xF3``).
   * - ``0xFF``
     - :ref:`Fin <tag_0xFF>`
     - 0 o
     - Non
     - Marqueur de fin optionnel
