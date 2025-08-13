ICF Tag Registry (aligné sur TLV v1)
====================================

Le tableau suivant définit **l’ensemble des tags TLV réservés** dans le
format **ICF** version 1.  
Tout tag non listé est considéré comme **non défini** et **doit** être
rejeté en mode strict.  
Les valeurs indiquées sont figées pour la version courante de la
spécification et ne peuvent évoluer qu’à travers un processus officiel
de modification du registre.

Chaque entrée précise :

- le **Type** : valeur hexadécimale unique du tag,
- le **Nom** : désignation courte,
- la **Taille max** en octets,
- la **Description fonctionnelle**.

Les définitions détaillées, exemples d’utilisation et règles associées
sont disponibles dans la documentation officielle RST du registre ICF.

+--------+----------------+---------+---------------------------------------------------+
| Type   | Nom            | Taille  | Description                                       |
| (hex)  |                | max     |                                                   |
+========+================+=========+===================================================+
| ``0x01`` | URL          | 200 o   | Lien HTTP(S) complet vers une ressource numérique |
+--------+----------------+---------+---------------------------------------------------+
| ``0x02`` | Langue       | 2 o     | Code langue ISO 639-1 (``fr``, ``en``, ``es``…)   |
+--------+----------------+---------+---------------------------------------------------+
| ``0x03`` | Titre        | 64 o    | Titre optionnel du média (UTF-8)                  |
+--------+----------------+---------+---------------------------------------------------+
| ``0x04`` | Tag          | 3 o     | Octet 1 : cycle, Octet 2 : matière, Octet 3 :      |
|          | pédagogique  |         | sous-classe libre                                 |
+--------+----------------+---------+---------------------------------------------------+
| ``0x05`` | Rétention    | 1 o     | Durée de conservation du média local (en jours,   |
|          |              |         | 0 = non stocké)                                   |
+--------+----------------+---------+---------------------------------------------------+
| ``0x06`` | Expiration   | 4 o     | Timestamp d’expiration absolue (UNIX time,        |
|          |              |         | big-endian)                                       |
+--------+----------------+---------+---------------------------------------------------+
| ``0xE0`` | Type badge   | 1 o     | 0 = ressource, 1 = configuration, 2 = administration |
+--------+----------------+---------+---------------------------------------------------+
| ``0xE1``–``0xEF`` | Payload sys. | variable | Données de config ou commandes admin (JSON) |
+--------+----------------+---------+---------------------------------------------------+
| ``0xF2`` | Hash         | 32 o    | SHA256 calculé sur tous les TLV précédents        |
+--------+----------------+---------+---------------------------------------------------+
| ``0xF3`` | Signature    | 64 o    | Signature du hash par une autorité locale (Ed25519) |
+--------+----------------+---------+---------------------------------------------------+
| ``0xF4`` | AuthorityID  | 8 o     | Identifiant de l’autorité ayant signé le contenu  |
+--------+----------------+---------+---------------------------------------------------+
| ``0xFF`` | Fin          | 0 o     | (optionnel) marqueur de fin de capsule            |
+--------+----------------+---------+---------------------------------------------------+
