=================
Spécification ICF
=================

Le **IOBEWI Capsule Format (ICF)** est un format TLV ouvert conçu pour encoder de manière sécurisée des métadonnées et liens vers des ressources numériques sur puces RFID, dans le cadre du projet open source Balabewi.

********
Objectif
********

Définir un format TLV, appelé IOBEWI Capsule Format (ICF), pérenne, compact et sécurisé, pour encoder des informations sur une puce RFID (NTAG215, 504 octets utiles), utilisée dans les lecteurs audio Balabewi.

Ce format vise à :

* garantir la **simplicité d’usage** sur une interface sans écran,
* permettre une **vérification cryptographique** de la source du contenu,
* s'adapter au **contexte scolaire ou familial**, en mode bridé ou ouvert,
* intégrer dès le départ **tous les mécanismes utiles** à la gouvernance, la sécurité et la pérennité des contenus.

***
TLV 
***
.. include:: tlv-structure.rst

******
Modèle 
******
.. include:: model.rst

********
Sécurité
********
.. include:: security.rst

****************
Interopérabilité
****************
.. include:: interop.rst

********
Exemples 
********
.. include:: examples.rst