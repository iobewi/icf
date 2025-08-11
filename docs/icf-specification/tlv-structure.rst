==============
Structure TLV
==============

ICF encode les données en **Type-Length-Value** compacts.

Principes
---------
* `Type` : octet (0x01..0xFF)
* `Length` : longueur utile (petite entête)
* `Value` : contenu binaire/UTF-8 selon le tag

Notes de compatibilité
----------------------
* Les lecteurs doivent ignorer les **tags inconnus** (forward-compatible).
