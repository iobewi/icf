====================
Registre de tags ICF
====================

.. list-table:: ICF Tag Registry (aligné sur TLV v1)
   :header-rows: 1
   :widths: 10 20 10 60

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
     - Code ISO 639-1 (``fr``, ``en``, ``es`` …)
   * - ``0x03``
     - Titre
     - 64 o
     - Titre optionnel du média (UTF-8)

.. note::
   Compléter avec l’ensemble des tags officiels (pédagogie, sécurité, etc.).
