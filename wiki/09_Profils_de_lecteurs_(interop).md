Profils de lecteurs (interop)

- **Reader-L0** : Parse TLV, affiche `URL/Titre`, `Langue`, `Expiration` si présents. Affiche un état de confiance (*Non vérifié* si pas de signature).
- **Reader-L1** : En plus, calcule `0xF2`, vérifie `0xF3` avec la clé liée à `0xF4`. Affiche *Validé (autorité X)* / *Signature invalide* / *Autorité inconnue*.
- **Reader-L2** : En plus, déchiffre `0xE1–0xEF` si applicable. L’échec de déchiffrement **ne bloque pas** l’affichage des métadonnées publiques.

---