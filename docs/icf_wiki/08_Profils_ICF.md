Profils ICF

### 8.1 ICF-Full (recommandé NTAG215/216)
**Requis :**
- `0x01` URL **ou** `0x03` Titre (au moins un des deux)
- `0xF2` Hash (SHA-256) calculé **sur tous les TLV précédents**
- `0xF3` Signature Ed25519 **du hash** (valeur de `0xF2`)
- `0xF4` AuthorityID (8 octets)

**Optionnels :**
- `0x02` Langue (2 lettres)
- `0x04` Tag pédagogique (3 octets : cycle, matière, sous-classe)
- `0x05` Rétention (jours)
- `0x06` Expiration (u32 epoch)
- `0xE0` Type badge (0=ressource, 1=config, 2=admin)
- `0xE1–0xEF` Payload système (JSON ou binaire, usage lecteur)

**Ordre recommandé :**
```
[0x01?] [0x02?] [0x03?] [0x04?] [0x05?] [0x06?] [0xE0?] [0xE1–0xEF?] [0xF2] [0xF3] [0xF4] [0xFF?]
```

### 8.2 ICF-Lite (NTAG213)
**Requis :**
- `0x01` URL **ou** `0x03` Titre

**Optionnels :**
- `0x02` Langue, `0x06` Expiration, `0x04` Tag pédagogique

**Sécurité :**
- Pas d’obligation de `0xF2/0xF3/0xF4`. Le lecteur **doit** afficher l’état *Non vérifié* si la signature est absente.

---