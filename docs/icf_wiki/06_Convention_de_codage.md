Convention de codage

* **Endianness** : tous les entiers multi-octets (timestamps, identifiants) sont codés **big-endian**.
* **Texte** : chaînes UTF-8 **sans BOM**, maximum strict indiqué par `Length`. Aucun encodage alterné autorisé (ex. UTF-16).
* **Tolérance** : un lecteur peut ignorer les champs inconnus (`Type ∉ [0x01–0xF4]`) s’il est en mode libre. Il doit rejeter les capsules invalides en mode bridé.

---