Format TLV général

Chaque champ suit la structure TLV :

========== ======== ===================================
Champ      Taille   Description
========== ======== ===================================
``Type``   1 octet  Identifiant du champ
``Length`` 1 octet  Taille du champ ``Value`` en octets
``Value``  N octets Donnée encodée
========== ======== ===================================

Les TLV sont chaînés les uns à la suite, l’ordre est libre, **sauf pour
la signature qui doit clore la séquence**.

--------------
