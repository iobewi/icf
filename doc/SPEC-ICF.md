# ✨ Spécification du IOBEWI Capsule Format (ICF v1)

---

Le format ICF (IOBEWI Capsule Format) est un format TLV conçu par IOBEWI, dans le cadre du projet open source Balabewi, pour encoder de manière sécurisée des métadonnées et des liens vers des ressources numériques sur des puces RFID.

---


## 🌟 Objectif

Définir un format TLV, appelé IOBEWI Capsule Format (ICF), pérenne, compact et sécurisé, pour encoder des informations sur une puce RFID (NTAG215, 504 octets utiles), utilisée dans les lecteurs audio Balabewi.

Ce format vise à :

* garantir la **simplicité d’usage** sur une interface sans écran,
* permettre une **vérification cryptographique** de la source du contenu,
* s'adapter au **contexte scolaire ou familial**, en mode bridé ou ouvert,
* intégrer dès le départ **tous les mécanismes utiles** à la gouvernance, la sécurité et la pérennité des contenus.

---

## 📊 Format TLV général

Chaque champ suit la structure TLV :

| Champ    | Taille   | Description                       |
| -------- | -------- | --------------------------------- |
| `Type`   | 1 octet  | Identifiant du champ              |
| `Length` | 1 octet  | Taille du champ `Value` en octets |
| `Value`  | N octets | Donnée encodée                    |

Les TLV sont chaînés les uns à la suite, l'ordre est libre, **sauf pour la signature qui doit clore la séquence**.

---

## 🔢 Types TLV définis (v1)

| Type (hex) | Nom         | Taille max | Description                                                     |
| ---------- | ----------- | ---------- | --------------------------------------------------------------- |
| `0x01`     | URL         | 200 o      | Lien HTTP(S) complet vers une ressource numérique               |
| `0x02`     | Langue      | 2 o        | Code langue ISO 639-1 (`fr`, `en`, `es`…)                       |
| `0x03`     | Titre       | 64 o       | Titre optionnel du média (UTF-8)                                |
| `0x04`     | Tag pédagogique | 3 o        | Octet 1 : cycle, Octet 2 : matière, Octet 3 : sous-classe libre |
| `0x05`     | Rétention   | 1 o        | Durée de conservation du média local (en jours, 0 = non stocké) |
| `0x06`     | Expiration  | 4 o        | Timestamp d’expiration absolue (UNIX time, big-endian)          |
| `0xE0`     | Type badge  | 1 o        | 0=ressource, 1=configuration, 2=administration                 |
| `0xE1–0xEF`| Payload sys.| variable   | Données de config ou commandes admin                          |
| `0xF2`     | Hash        | 32 o       | SHA256 calculé sur tous les TLV précédents                      |
| `0xF3`     | Signature   | 64 o       | Signature du hash par une autorité locale (Ed25519)             |
| `0xF4`     | AuthorityID | 8 o        | Identifiant de l'autorité ayant signé le contenu                |
| `0xFF`     | Fin         | 0 o        | (optionnel) marqueur de fin de capsule                          |

> Le champ `AuthorityID` est essentiel si plusieurs autorités de confiance peuvent exister. Il permet au lecteur de savoir **quelle clé publique utiliser** pour vérifier la signature. Sans lui, le lecteur devrait essayer toutes les clés, ce qui est inefficace et peu fiable.

---

## 🧑‍💻 Convention de codage

* **Endianness** : tous les entiers multi-octets (timestamps, identifiants) sont codés **big-endian**.
* **Texte** : chaînes UTF-8 **sans BOM**, maximum strict indiqué par `Length`. Aucun encodage alterné autorisé (ex. UTF-16).
* **Tolérance** : un lecteur peut ignorer les champs inconnus (`Type ∉ [0x01–0xF4]`) s’il est en mode libre. Il doit rejeter les capsules invalides en mode bridé.

---

## 🧩 Détail des champs TLV

Chaque champ TLV défini dans l'ICF v1 est décrit ci-dessous de manière précise, avec son rôle, sa structure, et ses cas d’usage.

---

### `0x01` – 🌍 URL du contenu

* **Taille maximale** : 200 octets (UTF-8 sans BOM)
* **Type de données** : chaîne de caractères ASCII ou UTF-8
* **Contenu** : Lien HTTP(S) complet pointant vers une ressource numérique (ex. fichier audio, vidéo, page web…)
* **Exemple** : `https://balabewi.org/audio123.mp3`
* **Obligatoire** : Oui

> Le lien doit être accessible publiquement, sans authentification, et stable dans le temps.

---

### `0x02` – 🌐  Langue

* **Taille maximale** : 2 octets
* **Type de données** : ISO 639-1
* **Contenu** : Code à deux lettres représentant la langue principale du contenu numerique
* **Obligatoire** : Non, mais recommandé
* **Utilité** : 
 * Filtrage de contenu par langue dans une interface multilingue
 * Limitation géographique ou pédagogique selon la langue cible

---

### `0x03` – 📝 Titre

* **Taille maximale** : 64 octets
* **Type de données** : UTF-8
* **Contenu** : Titre lisible du média (ex. : *Histoires de pirates*)
* **Obligatoire** : Non, mais recommandé
* **Utilité** : Affichage dans une interface de supervision ou app mobile, classement, export

---

### `0x04` – 🎓 Tag pédagogique

* **Taille** : 3 octets
* **Structure** :

  * Octet 1 → **Cycle scolaire**
  * Octet 2 → **Matière ou thème**
  * Octet 3 → **Sous-classe libre**
* **Obligatoire** : Non, mais recommandé
* **Utilité** : Filtrage, gouvernance pédagogique, intégration dans un ENT ou interface métier

#### 📘 Tableau des cycles (octet 1)

| Valeur (hex) | Cycle scolaire           |
|--------------|--------------------------|
| `0x00`       | Non défini               |
| `0x01`       | Cycle 1 (maternelle)     |
| `0x02`       | Cycle 2 (CP-CE1-CE2)     |
| `0x03`       | Cycle 3 (CM1-CM2-6e)     |
| `0x04`       | Cycle 4 (5e-4e-3e)       |
| `0xFE`       | Réservé usage local      |
| `0xFF`       | Réservé usage futur      |

#### 📗 Tableau des matières (octet 2)

| Valeur (hex) | Matière / thème          |
|--------------|--------------------------|
| `0x00`       | Non défini               |
| `0x01`       | Lecture / histoire       |
| `0x02`       | Sciences / nature        |
| `0x03`       | Musique / chant          |
| `0x04`       | Langue étrangère         |
| `0x05`       | Projet personnalisé      |
| `0x06`       | Mathématiques            |
| `0x07`       | Éducation civique        |
| `0xFE`       | Réservé usage local      |
| `0xFF`       | Réservé usage futur      |

#### 📙 Sous-classe libre (octet 3)

* Utilisation libre par l’émetteur de la capsule (enseignant, app mobile…)
* Peut désigner :
 * un niveau précis (ex. : CE1 → 0x11)
 * un groupe classe (ex. : ULIS → 0x3A)
 * une série pédagogique (ex. : série "Écoute active" → 0x80)
* Valeurs non normalisées à ce jour
 * Si non utilisé : `0x00`

---

### `0x05` – 🕒 Durée de rétention

* **Taille** : 1 octet
* **Type de données** : entier non signé (uint8)
* **Contenu** : Nombre de jours pendant lesquels le média est conservé localement
* **Valeurs possibles** :

| Valeur          | Signification                 |
| --------------- | ----------------------------- |
| `0x00`          | Pas de stockage local         |
| `0x01` – `0xFF` | Stockage entre 1 et 255 jours |

> Permet de contrôler la place mémoire et l’actualisation automatique du contenu.

---

### `0x06` – 📆 Expiration absolue

* **Taille** : 4 octets
* **Type de données** : Timestamp UNIX (uint32 big-endian)
* **Contenu** : Date et heure au-delà de laquelle la capsule n’est plus valable
* **Obligatoire** : Non, mais conseillé dans un cadre scolaire ou temporaire
* **Exemple** : `0x66 87 3C A0` → `2025-12-31T23:59:59Z`

> Nécessite une horloge interne (RTC) ou une synchronisation réseau (NTP) sur le lecteur.

---

### `0xE0` – 🎫 Type de badge

* **Taille** : 1 octet
* **Valeurs** :
  * `0x00` → Badge ressource (lecture audio)
  * `0x01` → Badge configuration (paramètres simples)
  * `0x02` → Badge administration (données sensibles chiffrées)
* **Obligatoire** : Non — s'il est absent, le badge est considéré comme une ressource.

### `0xE1–0xEF` – 📦 Données système

* **Taille** : variable
* **Contenu** : Charges utiles de configuration ou commandes d'administration.
* **Persistance** : Certaines données peuvent être stockées en NVS si nécessaire.

---

### `0xF2` – 🔐 Hash SHA256

* **Taille** : 32 octets
* **Contenu** : Résultat du calcul SHA256 sur tous les TLV précédents
* **Format** : binaire brut
* **Utilité** : Garantit l’intégrité des données en cas de signature

> Le hash SHA256 est calculé sur la **concaténation binaire des TLV précédents**, dans l’ordre :>
> ```
> [Type₁][Length₁][Value₁][Type₂][Length₂][Value₂]... → SHA256
> ```>
> Ne **jamais inclure les TLV `0xF2`, `0xF3`, `0xF4`** dans ce calcul.>
> Recommandation : valider le buffer brut par des outils de test fournis (voir section CLI plus bas).

---

### `0xF3` – ✍️ Signature cryptographique

* **Taille** : 64 octets
* **Algorithme** : Ed25519
* **Contenu** : Signature de `0xF2` à l’aide d’une clé privée locale
* **Généré par** : l’application officielle ou un outil CLI sécurisé

> Signé à partir du hash SHA256 (champ `0xF2`)
> Doit être présent **avec** un champ `0xF4` pour être exploitable par un lecteur sécurisé

---

### `0xF4` – 🆔 Authority ID

* **Taille** : 8 octets
* **Type** : identifiant unique d’autorité (uint64 ou chaîne fixe)
* **Contenu** : Permet au lecteur de savoir quelle clé publique utiliser pour vérifier la signature
* **Exemple** : `01 23 45 67 89 AB CD EF`

> Chaque autorité locale (ex. : école, structure, éditeur) peut avoir sa propre paire de clés.

---

### `0xFF` – ✅ Marqueur de fin

* **Taille** : 0 octet
* **Utilité** : Optionnelle — peut marquer explicitement la fin d’une capsule
* **Interprétation** : Indique qu’aucun champ ne suit

---

## 🔐 Mécanisme de vérification (lecteur)

Le lecteur peut être configuré en 2 modes :

| Mode      | Comportement                                                          |
| --------- | --------------------------------------------------------------------- |
| **Libre** | Accepte tout tag TLV valide, qu'il soit signé ou non                  |
| **Bridé** | Accepte uniquement les capsules **signées par une autorité reconnue** |

Dans ce second cas :

* `0xF3` (signature) et `0xF4` (authority ID) doivent être présents,
* la signature est vérifiée via une clé publique préenregistrée dans le lecteur,
* l’identifiant `AuthorityID` permet de sélectionner la bonne clé publique dans la liste embarquée.

---

## 👥 Fonctionnement de la signature (Ed25519)

* La signature est réalisée **par l’app mobile**, qui détient une **clé privée locale**.

* L’app :

  1. Construit les TLV à signer (`0x01`, `0x02`, `0x03`, `0x04`, `0x05`, `0x06`, etc.)
  2. Calcule le SHA256 du buffer TLV
  3. Signe ce hash avec la clé privée (Ed25519)
  4. Ajoute les TLV `0xF2`, `0xF3`, `0xF4`

* Le lecteur, s’il est bridé, ne lit **que les capsules signées par une clé publique reconnue**, identifiée grâce au champ `0xF4`.

---

## 📄 Exemple de capsule signée

| Type | Len  | Valeur                           | Commentaire               |
| ---- | ---- | -------------------------------- | ------------------------- |
| `01` | `1A` | `https://balabewi.org/audio.mp3` | URL du média              |
| `02` | `02` | `66 72`                          | Langue : `fr` (français)  |
| `03` | `0F` | `Histoires de pirates`           | Titre                     |
| `04` | `03` | `0x01 0x01 0x00`                 | Cycle 1 / Lecture / Libre |
| `05` | `01` | `0x07`                           | Rétention de 7 jours      |
| `06` | `04` | `0x66 87 3C A0`                  | Expiration                |
| `F2` | `20` | `...sha256...`                   | Hash                      |
| `F3` | `40` | `...signature...`                | Signature Ed25519         |
| `F4` | `08` | `01 23 45 67 89 AB CD EF`        | ID autorité locale        |
| `FF` | `00` | `–`                              | Marqueur de fin           |

---

## 🔧 Espace utilisé sur NTAG215 (504 octets max)

| Champ          | Taille typique |
| -------------- | ---------------|
| URL            | ~120 à 200 o   |
| Langue         | 2 o            |
| Titre          | ~32 à 64 o     |
| Tag pédagogique| 3 o            |
| Rétention      | 1 o            |
| Expiration     | 4 o            |
| Hash (SHA256)  | 32 o           |
| Signature      | 64 o           |
| Authority ID   | 8 o            |
| Marqueur de fin| 0 à 2 o        |
| **Total**      | ~330 à 430 o   |

---

## 🧰 Outils recommandés

### ✅ CLI ou lib de référence (à développer)

* Encodage / décodage de capsules
* Signature via clé locale
* Vérification par clé publique
* Export/import en JSON

### Exemple JSON minimal :

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

### Exemple JSON complet :

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
---

### 🔍 Détails :

* `hash` : SHA256 des TLV `[0x01→0x07]`, **encodé en hexadécimal** (64 caractères, 32 octets binaires).
* `signature` : Signature **Ed25519 brute**, encodée en hexadécimal (64 octets binaires).
* `authority_id` : Tableau explicite de 8 octets, big-endian.

---

Souhaites-tu aussi la version TLV binaire en hexdump brut de cette capsule ?

---

## 🧠 Modes de lecture

| Mode      | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| **Libre** | Tout TLV valide est accepté, signé ou non                         |
| **Bridé** | Seules les capsules avec `0xF3` et `0xF4` valides sont autorisées |

---

## 🔐 Types de badges et sécurité

| Type           | Signature requise | Chiffrement requis | Persistant |
| -------------- | ----------------- | ------------------ | ----------- |
| Ressource      | Optionnel / Requis selon mode | Non | Non |
| Configuration  | Non | Non | Non |
| Administration | Oui | Oui (ECIES) | Oui |

---

## 🔮 Évolutivité et versioning

* Le champ `0x00` pourra servir à versionner le format (réservé à un usage futur).
* Les plages `0x10–0xEF` sont disponibles pour des extensions propriétaires ou publiques.

---

## 📌 Conclusion

Le format **ICF v1** est :

* ✅ **Facile à implémenter**
* 🔐 **Sûr** (via Ed25519 + SHA256)
* 📦 **Compact** (504 o max)
* 🧱 **Extensible** (balises réservées, version possible)
* 🧑‍🏫 **Pédagogiquement utile** (tag éducatif natif)

---

## 📇 Références & Crédits

**IOBEWI Capsule Format (ICF v1)** est une spécification ouverte, conçue et maintenue par **IOBEWI**, dans le cadre du projet open source **Balabewi**.

Ce format permet de stocker, sur une puce RFID à capacité limitée, des **liens vers des ressources numériques** (audio, vidéo, documentaires, activités…), accompagnés d’un ensemble minimal de **métadonnées utiles** (langue, titre, durée, tags pédagogiques, etc.).

Il permet également d’**authentifier l’émetteur** de l’information — parent, enseignant, institution — grâce à un mécanisme de signature cryptographique intégré. L'ICF est ainsi conçu pour offrir un usage **sobre, fiable, traçable et interopérable**, dans des contextes éducatifs ou familiaux, même sans écran.

---

**👤 Auteur & éditeur**
🛠️ IOBEWI
🌐 [https://iobewi.com](https://iobewi.com)
📧 [contact@iobewi.com](mailto:contact@iobewi.com)

---

**📜 Licence de la spécification**
Le format ICF est publié sous licence [**CC-BY-SA 4.0**](https://creativecommons.org/licenses/by-sa/4.0/),
 vous pouvez copier, adapter et partager la documentation et les formats, à condition de citer la source et de partager vos contributions sous la même licence.

---

**🔑 Références techniques**

* RFC 7049 — Concise Binary Object Representation (CBOR)
* ISO 7816-4 — Interindustry commands for interchange
* ISO/IEC 14443 — RFID proximity cards
* Ed25519 — High-speed high-security digital signature ([RFC 8032](https://datatracker.ietf.org/doc/html/rfc8032))