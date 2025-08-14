Le format **ICF** (*Interoperable Capsule Format*) a pour but de fournir une méthode
**fiable, compacte et sécurisée** pour encoder et échanger des informations
sur des puces NFC/RFID (NTAG213, NTAG215/216).

Ses objectifs principaux sont :

- **Assurer l’interopérabilité** entre différents lecteurs, émetteurs et outils,
  en normalisant la structure et le codage des données.
- **S’adapter à des usages variés**, notamment dans les contextes scolaire,
  familial ou culturel, grâce à un mode *bridé* ou *ouvert* selon les politiques locales.
- **Offrir aux éditeurs et ayants droit un contrôle précis de l’usage** de leurs contenus
  via un champ `SourcePolicy`, permettant de définir directement dans la capsule
  des règles techniques signées : durée maximale de conservation locale, conditions de chiffrement
  (lié à l’appareil et/ou au badge), interdiction de cache persistant, obligation de revalidation, etc.
  Ces contraintes sont **techniquement appliquées** par tout lecteur compatible ICF,
  garantissant ainsi le respect contractuel et la protection des politiques de diffusion.
- **Garantir l’intégrité et l’authenticité** des données grâce à une empreinte 
  numérique (*hash*, `0xF2`) et une signature cryptographique (`0xF3`) vérifiée
  avec la clé d’une autorité de confiance (`0xF4`).
- **Optimiser l’usage de l’espace mémoire** disponible sur la puce,
  en définissant des profils adaptés :
  * **ICF-Full** pour NTAG215/216 (capacité étendue, sécurité complète)
  * **ICF-Lite** pour NTAG213 (capacité réduite, sécurité optionnelle)
- **Faciliter l’intégration** dans des systèmes et applications existants,
  notamment via l’encapsulation NDEF avec type MIME `application/vnd.icf+tlv`.