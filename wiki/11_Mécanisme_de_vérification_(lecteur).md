Mécanisme de vérification (lecteur)

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