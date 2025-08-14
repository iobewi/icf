.. _source_policy:

SourcePolicy (``0x07``)
=======================

Le champ **SourcePolicy** (obligatoire) définit la *typologie*, 
les *contraintes d’usage* et, le cas échéant, un **identifiant d’accord** 
(*AgreementID*) permettant de lier la capsule à un contrat de diffusion précis.
Ces informations, signées via ``0xF3``, sont **inaltérables** par un lecteur 
ou un tiers non autorisé.

Par défaut, sans **AgreementID** ni autorisation explicite de cache,  
un contenu soumis à droits d’auteur est **lu uniquement en session**,  
sans stockage local. Lorsqu’un accord existe avec un éditeur, la politique appliquée
par le lecteur peut **autoriser et encadrer** un usage hors ligne du média.

Objectifs
---------

- **Renforcer la confiance** des ayants droit et producteurs : les règles techniques sont appliquées côté lecteur,
  sur la base d’une typologie et de contraintes clairement définies dans la capsule.
- **Décorréler les durées de rétention du badge** : permettre leur évolution
  sans modification du support physique.
- **Uniformiser le comportement** : un même type de ressource appliquera les mêmes règles
  sur tous les lecteurs à jour.

Règles d’interprétation
-----------------------

- **Absence de politique reconnue**
  → Rétention = 0, lecture uniquement pendant la session (*streaming* ou *buffer* temporaire).
- **Pas de durée de rétention stockée dans le badge**
  → Le champ ``0x07`` décrit uniquement la typologie de la source et les contraintes d’usage
    (flags, classe, identifiant d’accord).  
    La durée effective est fixée par le lecteur selon sa **politique locale**
    ou une **mise à jour distante**.
- **Mises à jour adaptatives**
  → Un accord avec un éditeur peut être modifié (durées, autorisations de cache, chiffrement…)
    via mise à jour distante, sans changement du badge déjà en circulation.
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