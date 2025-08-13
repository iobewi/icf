Exemple d’un badge en format JSON
---------------------------------

Badge de ressource (`badge_type: 0x00`)
---------------------------------------

Minimal :
^^^^^^^^^

```json
{
  "url": "https://balabewi.org/audio123.mp3",
  "language": "fr",
  "title": "Histoires de pirates",
  "tag": {
    "cycle": 1,
    "subject": 1,
    "sub": 0
  },
  "retention": 7,
  "expires": 1767225599,
  "authority_id": "0x0123456789ABCDEF"
}
```

Complet :
^^^^^^^^^

```json
{
  "url": "https://balabewi.org/audio123.mp3",
  "language": "fr",
  "title": "Histoires de pirates",
  "tag": {
    "cycle": 1,
    "subject": 1,
    "sub": 0
  },
  "retention": 7,
  "expires": 1767225599,
  "hash": "bdc9aaf329d204cdefb71884a91ce08987c9a91b657f3f4583a6c88e3c58ad71",
  "signature": "6b871e50c723011c6ab345e847c10d89d0a2604bced7e7c9d0fa1c8fd8fbd2b91d8df6c86156e15d1de9e68e5b4c8c7760b13ef6de25035178135eb79ab7d208",
  "authority_id": [1, 35, 69, 103, 137, 171, 205, 239]
}
```

Avec paramètre de configuration :
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```json
{
  "badge_type": 0,
  "url": "https://balabewi.org/audio123.mp3",
  "language": "fr",
  "title": "Histoires de pirates",
  "tag": {
    "cycle": 1,
    "subject": 1,
    "sub": 0
  },
  "retention": 7,
  "expires": 1767225599,
  "authority_id": "0x0123456789ABCDEF",
  "system_payload": {
    "volume": 50,
    "ambience": "bright",
    "lock_buttons": true
  }
}
```

Badge de configuration (`badge_type: 0x01`)
-------------------------------------------

Ce type de badge permet de configurer des paramètres simples du lecteur, sans chiffrement ni signature obligatoire.

```json
{
  "badge_type": 1,
  "system_payload": {
    "volume": 70,
    "sleep_timeout": 120,
    "ambience": "calm"
  }
}
```

Badge d’administration (`badge_type: 0x02`)
-------------------------------------------

Pour respecter la spécification, le contenu d’un badge d’administration (`badge_type: 2`) ne doit **jamais** exposer des données en clair dans le champ `system_payload`.
Le contenu JSON original est d’abord sérialisé, puis chiffré via ECIES, puis encodé en base64.
Le champ `system_payload` dans l’exemple JSON est une chaîne binaire chiffrée (souvent encodée en Base64 dans les outils). Elle ne peut être interprétée qu’après déchiffrement par un lecteur équipé de la bonne clé.

```json
{
  "badge_type": 2,
  "system_payload": "BASE64(ECIES(payload JSON))",
  "signature": "<signature_ed25519>",
  "authority_id": [1, 35, 69, 103, 137, 171, 205, 239]
}
```



Espace utilisé sur NTAG215 (504 octets max)
===========================================

Capsule de ressource (`badge_type: 0x00`)
-----------------------------------------

| Champ              | Taille typique     |
| ------------------ | ------------------ |
| `0x01` URL         | \~120 à 200 octets |
| `0x02` Langue      | 2 octets           |
| `0x03` Titre       | \~32 à 64 octets   |
| `0x04` Tag péd.    | 3 octets           |
| `0x05` Rétention   | 1 octet            |
| `0x06` Expiration  | 4 octets           |
| `0xF2` Hash        | 32 octets          |
| `0xF3` Signature   | 64 octets          |
| `0xF4` AuthorityID | 8 octets           |
| `0xFF` Fin         | 0 à 2 octets       |
| **Total**          | **\~330 à 430 o**  |

Badge de configuration (`badge_type: 0x01`)
-------------------------------------------

| Champ               | Taille typique   |
| ------------------- | ---------------- |
| `0xE0` Type         | 1 octet          |
| `0xE1` Payload JSON | \~30 à 150 o     |
| `0xFF` Fin          | 0 à 2 octets     |
| **Total**           | **\~40 à 160 o** |

> Dépend fortement du contenu JSON (nombre de clés/valeurs, formatage compact ou non)

Capsule de ressource avec configuratioon (`badge_type: 0x00 + 0xE1`)
--------------------------------------------------------------------

| Champ                        | Taille typique         |
| ---------------------------- | ---------------------- |
| URL (`0x01`)                 | \~120 à 200 octets     |
| Langue (`0x02`)              | 2 octets               |
| Titre (`0x03`)               | \~32 à 64 octets       |
| Tag pédagogique (`0x04`)     | 3 octets               |
| Rétention (`0x05`)           | 1 octet                |
| Expiration (`0x06`)          | 4 octets               |
| Payload config JSON (`0xE1`) | \~50 à 100 o           |
| Hash (`0xF2`)                | 32 octets              |
| Signature (`0xF3`)           | 64 octets              |
| Authority ID (`0xF4`)        | 8 octets               |
| Fin (`0xFF`)                 | 0 à 2 octets           |
| **Total**                    | **\~370 à 480 octets** |

> Dépend fortement du contenu JSON (nombre de clés/valeurs, formatage compact ou non)

Badge d’administration (`badge_type: 0x02`)
-------------------------------------------

| Champ                  | Taille typique    |
| ---------------------- | ----------------- |
| `0xE0` Type            | 1 octet           |
| `0xE1` Payload chiffré | \~64 à 128 o      |
| `0xF2` Hash            | 32 octets         |
| `0xF3` Signature       | 64 octets         |
| `0xF4` AuthorityID     | 8 octets          |
| `0xFF` Fin             | 0 à 2 octets      |
| **Total**              | **\~170 à 240 o** |