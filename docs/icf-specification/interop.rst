.. _interop:

Profils de lecteurs
===================

Cette section est **normative** pour l’interopérabilité. Elle définit des profils
de conformité pour les lecteurs ICF et leurs exigences minimales.

Profils
-------

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Profil
     - Comportement minimal
   * - **Reader-L0**
     - Parse TLV, affiche ``URL/Titre``, ``Langue``, ``Expiration`` si présents.
       Doit afficher un état de confiance (*Non vérifié* si pas de signature).
   * - **Reader-L1**
     - Calcule ``0xF2``, vérifie ``0xF3`` avec la clé liée à ``0xF4`` (table locale d’autorités).
       Affiche *Validé (autorité X)* / *Signature invalide* / *Autorité inconnue*.
   * - **Reader-L2**
     - En plus, tente le déchiffrement de ``0xE1-0xEF`` (si présent).
       L’échec de déchiffrement ne bloque pas l’affichage des métadonnées publiques.

Matrice de conformité
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 15 15

   * - Capacité
     - L0
     - L1
     - L2
     - Mode Libre
     - Mode Bridé
   * - Parse TLV + champs publics
     - Oui
     - Oui
     - Oui
     - Oui
     - Oui
   * - Calcul ``0xF2`` (SHA-256)
     - Non
     - Oui
     - Oui
     - Option
     - Requis
   * - Vérif ``0xF3`` via ``0xF4``
     - Non
     - Oui
     - Oui
     - Option
     - Requis
   * - Déchiffrement ``0xE1`` (ECIES/X25519)
     - Non
     - Non
     - Oui
     - Option
     - Selon politique
   * - Rejet capsule non signée
     - Non
     - Option
     - Option
     - Non
     - Oui

Politiques de lecture
---------------------

.. list-table:: Modes de fonctionnement
   :header-rows: 1
   :widths: 15 85

   * - Mode
     - Comportement
   * - **Libre**
     - Accepte tout tag TLV valide, signé ou non
   * - **Bridé**
     - Accepte uniquement les capsules **signées par une autorité reconnue**


Modes de lecture
================

Les modes de lecture définissent la **politique de validation appliquée par un lecteur**
lorsqu’il reçoit une capsule ICF.  
Ils influencent directement la manière dont le lecteur filtre ou accepte les données
en fonction de leur signature et de l’autorité émettrice.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Mode
     - Comportement
   * - **Libre**
     - Accepte tout tag TLV valide, qu'il soit signé ou non.
       Idéal pour la compatibilité maximale ou les phases de test.
   * - **Bridé**
     - Accepte uniquement les capsules **signées par une autorité reconnue**.
       Recommandé pour les environnements où la sécurité et la vérification
       des sources sont primordiales.

Ce choix de mode peut dépendre du contexte d’utilisation :
environnement éducatif contrôlé, diffusion publique de contenu, ou développement/test.

Mécanisme de vérification (lecteur)
===================================

Le lecteur peut être configuré en deux modes de fonctionnement, influençant la
gestion de la signature et la validation des capsules :

.. list-table:: Modes de fonctionnement
   :header-rows: 1
   :widths: 15 85

   * - Mode
     - Comportement
   * - **Libre**
     - Accepte tout tag TLV valide, qu'il soit signé ou non
   * - **Bridé**
     - Accepte uniquement les capsules **signées par une autorité reconnue**

Dans le mode **Bridé** :

* `0xF3` (signature) et `0xF4` (AuthorityID) doivent être présents,
* la signature est vérifiée via une clé publique préenregistrée dans le lecteur,
* l’identifiant `AuthorityID` permet de sélectionner la clé publique appropriée dans la liste embarquée.

Interprétation de ``SourcePolicy`` (0x07)
=========================================

Cette section précise comment un lecteur ICF doit interpréter et appliquer le champ
``SourcePolicy`` lorsqu’il est présent dans une capsule.

Règles d’interprétation
-----------------------

- **Absence de politique connue**
  → Rétention = 0, lecture uniquement pendant la session (*streaming* ou *buffer* temporaire).
- **Pas de durée de rétention stockée dans le badge**
  → Le champ ``0x07`` décrit uniquement la typologie de la source et les contraintes d’usage
    (flags, classe, identifiant d’accord).  
    La durée effective est fixée par le lecteur selon sa **politique locale**
    ou une **mise à jour distante**.
- **Mises à jour adaptatives**
  → Un accord avec un éditeur peut être modifié (durées, autorisations de cache, chiffrement…)
    via mise à jour distante, sans changement du badge déjà en circulation.
- **Revalidation**
  → Si un délai de revalidation > 0 est défini, le lecteur doit tenter périodiquement de
    rafraîchir la politique et/ou le média.  
    En cas d’échec, la lecture peut rester autorisée jusqu’à expiration de la dernière
    politique connue, sauf si la classe/flags imposent un blocage strict.
- **Flags contraignants**
  → Les combinaisons suivantes sont prioritaires sur toute règle locale :  
    * ``EPHEMERAL_ONLY`` ⇒ cache persistant interdit (rétention = 0)  
    * ``ALLOW_CACHE = 0`` ⇒ rétention = 0 même si la politique distante autorise le cache.
- **Identifiant d’accord**
  → Si présent, permet au lecteur d’associer le badge à un ensemble de règles prédéfinies,
    garantissant l’application cohérente de la rétention et du chiffrement.

.. note::
   En cas d’incohérence (par ex. flags inconnus ou identifiant d’accord non reconnu),
   le lecteur **doit** appliquer la politique la plus restrictive :
   pas de cache persistant, lecture en session uniquement.


Tolérance et validation
-----------------------

**1. Validation de la signature et de l’autorité**

- **Mode libre**  
  Le lecteur **peut** accepter une capsule valide sur le plan TLV, qu’elle soit **signée** ou non.  
  La présence d’une signature (`0xF3`) et d’un identifiant d’autorité (`0xF4`) est optionnelle.

- **Mode bridé**  
  Le lecteur **doit** accepter uniquement les capsules :
  
  * contenant `0xF3` (signature) et `0xF4` (identifiant d’autorité),  
  * dont la signature est vérifiée avec succès à l’aide de la clé publique associée à `0xF4` dans la table locale d’autorités.

**2. Gestion des champs TLV non reconnus**

Indépendamment du mode de lecture :

- Un lecteur **doit** traiter correctement tout type TLV qu’il ne connaît pas,  
  en l’ignorant proprement et en poursuivant le parsing, afin de garantir la compatibilité avec des extensions futures.  
- La présence de champs non reconnus **ne doit pas** invalider une capsule, sauf si la spécification impose explicitement leur absence pour un profil ou un mode donné.