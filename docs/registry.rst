ICF Tag Registry (aligné sur TLV v1)
====================================

+------+-------+------+-----------------------------------------------+
| Type | Nom   | Ta   | Description                                   |
| (    |       | ille |                                               |
| hex) |       | max  |                                               |
+======+=======+======+===============================================+
| ``0x | URL   | 200  | Lien HTTP(S) complet vers une ressource       |
| 01`` |       | o    | numérique                                     |
+------+-------+------+-----------------------------------------------+
| ``0x | L     | 2 o  | Code langue ISO 639-1 (``fr``, ``en``,        |
| 02`` | angue |      | ``es``\ …)                                    |
+------+-------+------+-----------------------------------------------+
| ``0x | Titre | 64 o | Titre optionnel du média (UTF-8)              |
| 03`` |       |      |                                               |
+------+-------+------+-----------------------------------------------+
| ``0x | Tag   | 3 o  | Octet 1 : cycle, Octet 2 : matière, Octet 3 : |
| 04`` | p     |      | sous-classe libre                             |
|      | édago |      |                                               |
|      | gique |      |                                               |
+------+-------+------+-----------------------------------------------+
| ``0x | Réte  | 1 o  | Durée de conservation du média local (en      |
| 05`` | ntion |      | jours, 0 = non stocké)                        |
+------+-------+------+-----------------------------------------------+
| ``0x | Expir | 4 o  | Timestamp d’expiration absolue (UNIX time,    |
| 06`` | ation |      | big-endian)                                   |
+------+-------+------+-----------------------------------------------+
| ``0x | Type  | 1 o  | 0=ressource, 1=configuration,                 |
| E0`` | badge |      | 2=administration                              |
+------+-------+------+-----------------------------------------------+
| `    | Pa    | vari | Données de config ou commandes admin          |
| `0xE | yload | able | (encodées en JSON)                            |
| 1–0x | sys.  |      |                                               |
| EF`` |       |      |                                               |
+------+-------+------+-----------------------------------------------+
| ``0x | Hash  | 32 o | SHA256 calculé sur tous les TLV précédents    |
| F2`` |       |      |                                               |
+------+-------+------+-----------------------------------------------+
| ``0x | Sign  | 64 o | Signature du hash par une autorité locale     |
| F3`` | ature |      | (Ed25519)                                     |
+------+-------+------+-----------------------------------------------+
| ``0x | A     | 8 o  | Identifiant de l’autorité ayant signé le      |
| F4`` | uthor |      | contenu                                       |
|      | ityID |      |                                               |
+------+-------+------+-----------------------------------------------+
| ``0x | Fin   | 0 o  | (optionnel) marqueur de fin de capsule        |
| FF`` |       |      |                                               |
+------+-------+------+-----------------------------------------------+
