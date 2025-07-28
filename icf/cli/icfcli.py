"""
icfcli.py – Interface CLI pour le IOBEWI Capsule Format (BCF / ICF)

Permet de :
- générer une capsule signée (`write`)
- lire et vérifier une capsule (`read`)
- afficher les tags pédagogiques (`list-tags`)
- exporter une capsule au format JSON (`export-json`)
- importer et signer une capsule depuis JSON (`import-json`)
"""

import argparse
import json
import sys
from pathlib import Path
from icf import icfCapsule, Cycle, Matiere, BadgeType
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization


def parse_badge_type(value: str) -> BadgeType:
    """Parse a badge type from CLI argument."""
    v = value.strip().lower()
    mapping = {
        'ressource': BadgeType.RESSOURCE,
        'resource': BadgeType.RESSOURCE,
        'configuration': BadgeType.CONFIGURATION,
        'config': BadgeType.CONFIGURATION,
        'administration': BadgeType.ADMINISTRATION,
        'admin': BadgeType.ADMINISTRATION,
    }
    if v.isdigit():
        try:
            return BadgeType(int(v))
        except ValueError:
            raise argparse.ArgumentTypeError('Badge type invalide')
    if v in mapping:
        return mapping[v]
    raise argparse.ArgumentTypeError(
        'Badge type invalide (ressource|configuration|administration|0|1|2)')


def load_private_key(path: str) -> Ed25519PrivateKey:
    """Charge une clé privée Ed25519 depuis un fichier PEM."""
    with open(path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def load_public_key(path: str) -> Ed25519PublicKey:
    """Charge une clé publique Ed25519 depuis un fichier PEM."""
    with open(path, 'rb') as f:
        return serialization.load_pem_public_key(f.read())


def write_capsule(args):
    """
    Encode une capsule ICF à partir des paramètres CLI et la signe avec une clé privée.
    Le résultat est écrit sous forme binaire TLV dans un fichier `.icf`.
    """
    cap = icfCapsule()
    cap.set_url(args.url)
    if args.language:
        cap.set_language(args.language)
    if args.title:
        cap.set_title(args.title)
    if args.badge_type is not None:
        cap.set_badge_type(args.badge_type)
    if args.retention is not None:
        cap.set_retention(args.retention)
    if args.tag:
        try:
            cycle_val, subject_val, sub = map(int, args.tag.split(','))
            cycle = Cycle(cycle_val)
            subject = Matiere(subject_val)
            cap.set_tag(cycle, subject, sub)
        except (ValueError, KeyError):
            print("Erreur : --tag doit être au format cycle,matière,sous-classe avec des valeurs valides.")
            sys.exit(1)
    if args.expires:
        cap.set_expiration(args.expires)

    private_key = load_private_key(args.private_key)
    authority_id = bytes.fromhex(args.authority_id)
    cap.finalize(private_key, authority_id)

    encoded = cap.encode_full()
    with open(args.output, 'wb') as f:
        f.write(encoded)
    print(f"Capsule écrite dans {args.output}")


def read_capsule(args):
    """
    Lit et décode une capsule ICF depuis un fichier `.icf`.
    Vérifie la signature si une clé publique est fournie.
    Affiche les données au format JSON.
    """
    data = Path(args.input).read_bytes()
    cap = icfCapsule.decode(data)

    if args.public_key:
        pub = load_public_key(args.public_key)
        is_valid = cap.verify(pub)
        print(f"Signature valide : {is_valid}")

    btype = cap.get_badge_type()
    if btype is None:
        btype = BadgeType.RESSOURCE
    print(f"Type de badge : {btype}")

    print("📦 Contenu capsule (JSON) :")
    print(json.dumps(cap.to_dict(), indent=2))

    print("\nTag pédagogique (décodé) :", cap.tag_str())


def list_tags(args):
    """
    Affiche la liste des cycles et matières pédagogiques supportés dans les tags ICF.
    Utilise les enums `Cycle` et `Matiere`.
    """
    print("🎓 Cycles pédagogiques disponibles :")
    for cycle in Cycle:
        print(f"  {cycle.value:02X} — {cycle.name.replace('_', ' ').title()} — {str(cycle)}")

    print("\nMatières disponibles :")
    for mat in Matiere:
        print(f"  {mat.value:02X} — {mat.name.replace('_', ' ').title()} — {str(mat)}")


def export_json(args):
    """
    Convertit une capsule ICF (`.icf`) en fichier JSON lisible (`.json`).
    Ne nécessite pas de clé.
    """
    data = Path(args.input).read_bytes()
    cap = icfCapsule.decode(data)
    output = Path(args.output)
    output.write_text(json.dumps(cap.to_dict(), indent=2), encoding='utf-8')
    print(f"Capsule exportée au format JSON : {output}")


def import_json(args):
    """
    Charge une capsule à partir d’un fichier JSON et génère un fichier `.icf` signé.
    Nécessite une clé privée et un identifiant d’autorité.
    """
    cap = icfCapsule.load_json(args.input)
    private_key = load_private_key(args.private_key)
    authority_id = bytes.fromhex(args.authority_id)
    cap.finalize(private_key, authority_id)
    encoded = cap.encode_full()
    Path(args.output).write_bytes(encoded)
    print(f"Capsule signée et encodée depuis JSON : {args.output}")


def main():
    """Point d’entrée CLI, définition des commandes disponibles."""
    parser = argparse.ArgumentParser(description='icf Capsule CLI')
    sub = parser.add_subparsers(dest='cmd', required=True)

    # Commande write
    write = sub.add_parser('write', help='Encode and sign a capsule')
    write.add_argument('--url', required=True)
    write.add_argument('--language')
    write.add_argument('--title')
    write.add_argument('--badge-type', type=parse_badge_type,
                       help='ressource, configuration ou administration')
    write.add_argument('--retention', type=int)
    write.add_argument('--tag', help='cycle,subject,sub (ex: 2,6,66)')
    write.add_argument('--expires', type=int, help='UNIX timestamp')
    write.add_argument('--private-key', required=True)
    write.add_argument('--authority-id', required=True, help='8-byte hex (ex: 0123456789ABCDEF)')
    write.add_argument('--output', required=True, help='Output capsule file')
    write.set_defaults(func=write_capsule)

    # Commande read
    read = sub.add_parser('read', help='Decode and verify a capsule')
    read.add_argument('--input', required=True)
    read.add_argument('--public-key', help='PEM file to verify signature')
    read.set_defaults(func=read_capsule)

    # Commande list-tags
    list_tag = sub.add_parser('list-tags', help='Liste les cycles et matières pédagogiques disponibles')
    list_tag.set_defaults(func=list_tags)

    # Commande export-json
    export_json_cmd = sub.add_parser('export-json', help='Exporte une capsule ICF vers un fichier JSON')
    export_json_cmd.add_argument('--input', required=True, help='Fichier .icf à décoder')
    export_json_cmd.add_argument('--output', required=True, help='Fichier de sortie .json')
    export_json_cmd.set_defaults(func=export_json)

    # Commande import-json
    import_json_cmd = sub.add_parser('import-json', help='Charge un JSON, signe et génère une capsule ICF')
    import_json_cmd.add_argument('--input', required=True, help='Fichier JSON source')
    import_json_cmd.add_argument('--private-key', required=True, help='Clé privée PEM')
    import_json_cmd.add_argument('--authority-id', required=True, help='8-byte hex (ex: 0123456789ABCDEF)')
    import_json_cmd.add_argument('--output', required=True, help='Fichier de sortie .icf')
    import_json_cmd.set_defaults(func=import_json)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
