==============
Modèle sécurité
==============

Concepts
--------
* **Signature** : Ed25519 (authenticité, intégrité)
* **Chiffrement ciblé** : X25519/ECIES (confidentialité pour un lecteur)
* **Authority ID** : identifie l’autorité signante

Bonnes pratiques
----------------
* Clés privées **jamais exportées** du dispositif qui les génère
* Rotation des clés et révocation par listes
