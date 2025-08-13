Profils ICF
===========

Le format ICF peut être adapté à différents types de puces NFC/RFID et à divers usages,
en fonction des contraintes de mémoire disponible et des besoins en sécurité.
Pour cette raison, deux profils principaux sont définis :

- **ICF-Full** : conçu pour des puces à capacité étendue (ex. NTAG215/216),
  il intègre les mécanismes de sécurité complets (`0xF2` Hash, `0xF3` Signature, `0xF4` AuthorityID)
  et permet une richesse maximale des métadonnées.
- **ICF-Lite** : optimisé pour les puces à capacité réduite (ex. NTAG213),
  il se limite aux champs essentiels, avec une sécurité optionnelle,
  pour maximiser l’espace utile.

Ces profils définissent les champs obligatoires, optionnels, et l’ordre recommandé
pour assurer une interprétation cohérente par les lecteurs compatibles.

ICF-Full (recommandé NTAG215/216)
---------------------------------

**Requis :**
- `0x01` URL **ou** `0x03` Titre (au moins un des deux)
- `0xF2` Hash (SHA-256) calculé **sur tous les TLV précédents**
- `0xF3` Signature Ed25519 **du hash** (valeur de `0xF2`)
- `0xF4` AuthorityID (8 octets)

**Optionnels :**
- `0x02` Langue (2 octets)
- `0x04` Tag pédagogique (3 octets : cycle, matière, sous-classe)
- `0x05` Rétention (1 octet, jours)
- `0x06` Expiration (4 octets, UNIX epoch big-endian)
- `0xE0` Type badge (1 octet : 0=ressource, 1=config, 2=admin)
- `0xE1–0xEF` Payload système (taille variable, JSON ou binaire, usage lecteur)

**Ordre recommandé :**
::

   [0x01?] [0x02?] [0x03?] [0x04?] [0x05?] [0x06?]
   [0xE0?] [0xE1–0xEF?] [0xF2] [0xF3] [0xF4] [0xFF?]

ICF-Lite (NTAG213)
------------------

Profil optimisé pour les puces à faible capacité mémoire, lorsque la priorité
est de maximiser l’espace utile pour le contenu plutôt que pour les métadonnées
et les signatures.

**Requis :**
- `0x01` URL **ou** `0x03` Titre

**Optionnels :**
- `0x02` Langue (2 octets)
- `0x06` Expiration (4 octets, UNIX epoch big-endian)
- `0x04` Tag pédagogique (3 octets : cycle, matière, sous-classe)

**Sécurité :**
- Pas d’obligation de `0xF2/0xF3/0xF4`.
  Le lecteur **doit** afficher l’état *Non vérifié* si la signature est absente.

ICF sur NDEF
============

Le format ICF peut être encapsulé dans un message **NDEF** (*NFC Data Exchange Format*),
ce qui est particulièrement utile lorsque l’on souhaite que les données ICF
soient lisibles par des applications ou systèmes NFC standards, tout en conservant
l’intégralité de la structure TLV.

- **Record type** : MIME
- **MIME type** : `application/vnd.icf+tlv`
- **Payload** : octets TLV ICF complets (incluant `0xF2`, `0xF3`, `0xF4` si présents)
- **Message recommandé** : un seul record MIME par message NDEF

**Avantages :**
- Permet à un lecteur NFC générique de détecter qu’il s’agit de données ICF via le MIME type.
- Compatible avec les outils de lecture/écriture NDEF existants.
- Facilite l’intégration dans des workflows ou applications qui s’attendent à des records NDEF.

**Limitations :**
- Les en-têtes NDEF ne sont **pas signés** :
  la sécurité repose uniquement sur les champs internes ICF (`0xF2` Hash, `0xF3` Signature, `0xF4` AuthorityID).
- L’encapsulation NDEF ajoute un léger surcoût en octets, à prendre en compte
  sur les puces à faible capacité.

**Remarque :**
L’encapsulation NDEF n’implique **aucune réaffectation** ou modification
des tags TLV ICF. Le contenu interne reste conforme à la spécification ICF.
