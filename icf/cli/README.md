# 📦 ICF Capsule CLI & Python Library

Cette bibliothèque et son interface en ligne de commande permettent de manipuler le format **ICF (IOBEWI Capsule Format)**, conçu pour encoder de manière compacte, sécurisée et vérifiable des métadonnées sur des puces RFID (NTAG215) dans le cadre du projet **Balabewi**.

---

## ✨ Fonctionnalités

### 🧩 Bibliothèque (`icf.py`)

- Construction de capsules TLV (Type-Length-Value)
- Encodage/décodage binaire
- Signature cryptographique (Ed25519)
- Vérification de l’authenticité
- Export et import JSON
- Enums intégrés pour les tags pédagogiques (`Cycle`, `Matiere`)
- Affichage lisible (`tag_str()`)

### 🛠️ Interface CLI (`icfcli.py`)

| Commande        | Description                                               |
|-----------------|-----------------------------------------------------------|
| `encode`        | Génère un binaire `.icf` signé à partir d’arguments CLI   |
| `decode`        | Décode et vérifie une capsule `.icf`                      |
| `list-tags`     | Affiche les cycles et matières pédagogiques disponibles   |
| `export-json`   | Convertit une capsule `.icf` en `.json`                   |
| `import-json`   | Recharge un `.json`, le signe et produit une `.icf`       |

---

## 🧪 Exemples

### Générer une capsule :

```bash
python3 icfcli.py encode \
  --url https://balabewi.org/audio.mp3 \
  --title "Histoire du soir" \
  --language fr \
  --retention 14 \
  --tag 2,6,42 \
  --expires 1760000000 \
  --private-key cle.pem \
  --authority-id 0123456789ABCDEF \
  --output sortie.icf
```

### Lire et vérifier une capsule :

```bash
python3 icfcli.py decode --input sortie.icf --public-key pub.pem
```

### Exporter en JSON :

```bash
python3 icfcli.py export-json --input sortie.icf --output sortie.json
```

### Importer et signer depuis JSON :

```bash
python3 icfcli.py import-json --input sortie.json --output nouvelle.icf \
  --private-key cle.pem --authority-id 0123456789ABCDEF
```

---

## 🔍 Affichage pédagogique

Activez `--verbose` pour afficher :
- Hash calculé (`SHA-256`)
- Signature (`Ed25519`)
- Contenu hexadécimal complet
- Décodage lisible du tag pédagogique

---

## 📘 Spécification ICF

Le format ICF suit une structure TLV avec :
- URL, titre, langue, durée de rétention
- Tag pédagogique (cycle, matière, sous-classe)
- Expiration
- Signature cryptographique (hash + clé d’autorité)

Voir le document `SPEC-ICF.md` pour la spécification complète.

---

## 🔐 Dépendances

- Python 3.8+
- Installer les dépendances avec `pip install -r requirements.txt`

---

## 📄 Licences

Ce projet est publié dans le cadre de l’initiative **Balabewi / IOBEWI**, et se divise en deux volets complémentaires :

- 🧩 **Code source & hardware** — sous licence [**MPL 2.0**](https://www.mozilla.org/MPL/2.0/),  
  vous pouvez librement utiliser, modifier et redistribuer les fichiers sources (Python, firmware, PCB...) à condition de publier les fichiers modifiés sous la même licence.

- 📘 **Spécification du format ICF / BCF** — sous licence [**CC-BY-SA 4.0**](https://creativecommons.org/licenses/by-sa/4.0/),  
  vous pouvez copier, adapter et partager la documentation et les formats, à condition de citer la source et de partager vos contributions sous la même licence.