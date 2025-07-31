# 📦 IOBEWI Capsule Format (ICF)

Ce repository contient la librairie Python et la ligne de commande permettant de 
manipuler le **IOBEWI Capsule Format (ICF)**. Ce format TLV signé a été conçu
pour encoder de manière compacte et sécurisée des métadonnées sur des puces RFID
(utilisées notamment dans le projet Balabewi).

- La [documentation utilisateur de la CLI](cli/README.md) décrit en détail
  les commandes disponibles et fournit plusieurs exemples d'usage.
- La [spécification complète du format ICF](doc/SPEC-ICF.md) présente la structure
  des capsules et les mécanismes cryptographiques employés.

## 🔧 Installation rapide


Ce projet requiert Python 3.8 ou plus. Il peut être installé
directement depuis les sources grâce au fichier `pyproject.toml` :

```bash
pip install .
```
Cela installera automatiquement la dépendance [`cryptography`].

## 📄 Licence

Le code source est distribué sous licence **MPL 2.0**. La spécification du format
est publiée sous licence **CC‑BY‑SA 4.0**.

## 🧪 Tests

Les tests unitaires peuvent être exécutés avec `pytest` :

```bash
pytest tests
```

Si la dépendance [`cryptography`] n'est pas disponible, les tests utilisent
automatiquement le stub situé dans `tests/cryptography_stub`.
