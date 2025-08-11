ICF sur NDEF

- **Record type** : MIME
- **MIME type** : `application/vnd.icf+tlv`
- **Payload** : octets TLV ICF complets (incluant `0xF2`, `0xF3`, `0xF4` si présents)
- **Message recommandé** : un seul record MIME

**Remarque :** NDEF n’implique **aucune** réaffectation de tags TLV ICF. Les en-têtes NDEF ne sont pas signés ; la confiance repose sur `0xF2/0xF3/0xF4` à l’intérieur du payload ICF.

---