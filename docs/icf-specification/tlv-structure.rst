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

