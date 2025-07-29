"""
icf.py – IOBEWI Capsule Format (ICF v1)

Ce module implémente une capsule TLV (Type-Length-Value) signée et vérifiable,
destinée à encoder des métadonnées (URL, titre, langue, etc.) sur une puce RFID.

Utilisé dans le cadre du projet Balabewi.
"""

import hashlib
import struct
from enum import IntEnum
from typing import Optional, Dict, List, Union
import json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

# Mapping des types TLV utilisés
TLV_TYPES = {
    'url': 0x01,
    'language': 0x02,
    'title': 0x03,
    'badge_type': 0xE0,
    'system_payload': 0xE1,
    'tag': 0x04,
    'retention': 0x05,
    'expires': 0x06,
    'hash': 0xF2,
    'signature': 0xF3,
    'authority_id': 0xF4,
    'end': 0xFF,
}

class Cycle(IntEnum):
    """
    Enumération des cycles scolaires utilisés dans le champ 'tag' (octet 1).

    Permet de classifier un contenu en fonction du cycle pédagogique auquel il est destiné.
    Les valeurs sont définies par la spécification BCF (Balabewi Capsule Format v1).

    Attributs :
        NON_DEFINI     : 0x00 — Aucun cycle précisé.
        CYCLE_1        : 0x01 — Cycle 1 (maternelle).
        CYCLE_2        : 0x02 — Cycle 2 (CP, CE1, CE2).
        CYCLE_3        : 0x03 — Cycle 3 (CM1, CM2, 6e).
        CYCLE_4        : 0x04 — Cycle 4 (5e, 4e, 3e).
        LOCAL          : 0xFE — Réservé à un usage local.
        FUTUR          : 0xFF — Réservé à un usage futur.
    """
    NON_DEFINI = 0x00
    CYCLE_1 = 0x01
    CYCLE_2 = 0x02
    CYCLE_3 = 0x03
    CYCLE_4 = 0x04
    LOCAL = 0xFE
    FUTUR = 0xFF

    def __str__(self):
        labels = {
            Cycle.CYCLE_1: "Cycle 1 (maternelle)",
            Cycle.CYCLE_2: "Cycle 2 (CP à CE2)",
            Cycle.CYCLE_3: "Cycle 3 (CM1 à 6e)",
            Cycle.CYCLE_4: "Cycle 4 (5e à 3e)",
            Cycle.LOCAL: "Usage local",
            Cycle.FUTUR: "Réservé futur",
            Cycle.NON_DEFINI: "Non défini"
        }
        return labels.get(self, f"Cycle {self.value:02X}")

class Matiere(IntEnum):
    """
    Enumération des matières pédagogiques utilisées dans le champ 'tag' (octet 2).

    Sert à filtrer ou classer les contenus selon leur nature pédagogique.

    Attributs :
        NON_DEFINI           : 0x00 — Aucun thème défini.
        LECTURE_HISTOIRE     : 0x01 — Lecture ou histoire.
        SCIENCES_NATURE      : 0x02 — Sciences ou nature.
        MUSIQUE_CHANT        : 0x03 — Musique ou chant.
        LANGUE_ETRANGERE     : 0x04 — Langue vivante.
        PROJET_PERSONNALISE  : 0x05 — Projet ou activité personnalisée.
        MATHEMATIQUES        : 0x06 — Mathématiques.
        EDUCATION_CIVIQUE    : 0x07 — Enseignement civique.
        LOCAL                : 0xFE — Réservé à un usage local.
        FUTUR                : 0xFF — Réservé à un usage futur.
    """
    NON_DEFINI = 0x00
    LECTURE_HISTOIRE = 0x01
    SCIENCES_NATURE = 0x02
    MUSIQUE_CHANT = 0x03
    LANGUE_ETRANGERE = 0x04
    PROJET_PERSONNALISE = 0x05
    MATHEMATIQUES = 0x06
    EDUCATION_CIVIQUE = 0x07
    LOCAL = 0xFE
    FUTUR = 0xFF

    def __str__(self):
        labels = {
            Matiere.LECTURE_HISTOIRE: "Lecture / Histoire",
            Matiere.SCIENCES_NATURE: "Sciences / Nature",
            Matiere.MUSIQUE_CHANT: "Musique / Chant",
            Matiere.LANGUE_ETRANGERE: "Langue étrangère",
            Matiere.PROJET_PERSONNALISE: "Projet personnalisé",
            Matiere.MATHEMATIQUES: "Mathématiques",
            Matiere.EDUCATION_CIVIQUE: "Éducation civique",
            Matiere.LOCAL: "Usage local",
            Matiere.FUTUR: "Réservé futur",
            Matiere.NON_DEFINI: "Non défini"
        }
        return labels.get(self, f"Matière {self.value:02X}")


class BadgeType(IntEnum):
    """Type de badge RFID reconnu par le lecteur."""
    RESSOURCE = 0x00
    CONFIGURATION = 0x01
    ADMINISTRATION = 0x02

    def __str__(self):
        labels = {
            BadgeType.RESSOURCE: "ressource",
            BadgeType.CONFIGURATION: "configuration",
            BadgeType.ADMINISTRATION: "administration",
        }
        return labels.get(self, f"type {self.value:02X}")

class icfCapsule:
    """
    Représente une capsule ICF (IOBEWI Capsule Format) au format TLV.

    Elle permet de construire, signer, encoder, décoder et vérifier une capsule RFID.
    """
    def __init__(self):
        """Initialise une capsule vide avec dictionnaire interne des champs."""
        self.fields: Dict[int, bytes] = {}

    def set_badge_type(self, btype: 'BadgeType'):
        """Définit le type de badge (ressource, configuration, administration)."""
        self.fields[TLV_TYPES['badge_type']] = struct.pack('B', int(btype))

    def get_badge_type(self) -> Optional['BadgeType']:
        """Retourne le type de badge ou None s'il n'est pas défini."""
        raw = self.fields.get(TLV_TYPES['badge_type'])
        if not raw or len(raw) != 1:
            return None
        try:
            return BadgeType(raw[0])
        except ValueError:
            return None

    def set_url(self, url: str):
        """Définit l’URL cible du contenu."""
        self.fields[TLV_TYPES['url']] = url.encode('utf-8')

    def set_language(self, lang: str):
        """
        Définit la langue (code ISO-639-1 sur 2 caractères).

        :param lang: Exemple: 'fr' ou 'en'
        """
        assert len(lang) == 2
        self.fields[TLV_TYPES['language']] = lang.encode('utf-8')

    def set_title(self, title: str):
        """Définit le titre humainement lisible."""
        self.fields[TLV_TYPES['title']] = title.encode('utf-8')

    def set_retention(self, days: int):
        """
        Définit le nombre de jours de rétention du contenu.

        :param days: Nombre de jours (0–255)
        """
        self.fields[TLV_TYPES['retention']] = struct.pack('B', days)

    def set_tag(self, cycle: 'Cycle', subject: 'Matiere', sub: int):
        """
        Définit un tag pédagogique codé sur 3 octets :
        - cycle : instance de Cycle (enum)
        - subject : instance de Matiere (enum)
        - sub : valeur libre (0x00–0xFF)
        """
        self.fields[TLV_TYPES['tag']] = struct.pack('BBB', int(cycle), int(subject), sub)

    def set_system_payload(self, data: bytes):
        """Ajoute une charge utile système (configuration ou administration)."""
        self.fields[TLV_TYPES['system_payload']] = data

    def get_system_payload(self) -> Optional[bytes]:
        """Retourne la charge utile système si présente."""
        return self.fields.get(TLV_TYPES['system_payload'])

    def set_expiration(self, timestamp: int):
        """
        Définit la date d'expiration UNIX (4 octets big-endian).

        :param timestamp: Exemple: 1750000000
        """
        self.fields[TLV_TYPES['expires']] = struct.pack('>I', timestamp)

    def set_authority_id(self, authority: bytes):
        """
        Définit l'identifiant de l'autorité (8 octets).

        :param authority: bytes (len=8)
        """
        assert len(authority) == 8
        self.fields[TLV_TYPES['authority_id']] = authority

    def get_tag(self) -> Optional[tuple['Cycle', 'Matiere', int]]:
        """
        Retourne le champ 'tag pédagogique' décodé sous forme (Cycle, Matiere, sub).

        :return: tuple (Cycle, Matiere, sub) ou None si champ absent.
        """
        raw = self.fields.get(TLV_TYPES['tag'])
        if not raw or len(raw) != 3:
            return None
        cycle_val, matiere_val, sub = raw
        try:
            cycle = Cycle(cycle_val)
            matiere = Matiere(matiere_val)
        except ValueError:
            cycle = Cycle.NON_DEFINI
            matiere = Matiere.NON_DEFINI
        return (cycle, matiere, sub)

    def tag_str(self) -> str:
        """
        Retourne une chaîne lisible représentant le tag pédagogique.
        Exemple : "Cycle 2 / Mathématiques / sous-classe 0x42"
        """
        tag = self.get_tag()
        if not tag:
            return "Aucun tag pédagogique"
        cycle, matiere, sub = tag
        return f"{cycle.name.replace('_', ' ').title()} / {matiere.name.replace('_', ' ').title()} / sous-classe 0x{sub:02X}"


    def encode_unsigned(self) -> bytes:
        """
        Encode la capsule sans les champs hash/signature/authority_id/end.

        :return: Données binaires TLV pour hachage/signature.
        """
        out = bytearray()
        for k in sorted(self.fields.keys()):
            if k in (TLV_TYPES['hash'], TLV_TYPES['signature'], TLV_TYPES['authority_id'], TLV_TYPES['end']):
                continue
            val = self.fields[k]
            out += bytes([k, len(val)]) + val
        return bytes(out)


    def finalize(self, private_key: Ed25519PrivateKey, authority_id: bytes):
        """
        Signe la capsule avec une clé privée Ed25519 et ajoute les champs `hash`, `signature`, `authority_id`.

        :param private_key: Clé privée Ed25519.
        :param authority_id: Identifiant de l'autorité (8 octets).
        """
        raw = self.encode_unsigned()
        hash_val = hashlib.sha256(raw).digest()
        sig = private_key.sign(hash_val)
        self.fields[TLV_TYPES['hash']] = hash_val
        self.fields[TLV_TYPES['signature']] = sig
        self.fields[TLV_TYPES['authority_id']] = authority_id

    def encode_full(self, include_end: bool = True) -> bytes:
        """
        Encode tous les champs de la capsule (y compris hash et signature).

        :param include_end: Ajoute un champ `0xFF 0x00` de fin si True.
        :return: Données TLV complètes.
        """
        out = bytearray()
        for k in sorted(self.fields.keys()):
            val = self.fields[k]
            out += bytes([k, len(val)]) + val
        if include_end:
            out += bytes([TLV_TYPES['end'], 0])
        return bytes(out)

    @staticmethod
    def decode(data: bytes) -> 'icfCapsule':
        """
        Décode un flux binaire TLV en objet capsule.

        :param data: Données TLV
        :return: Instance de icfCapsule
        """
        i = 0
        cap = icfCapsule()
        while i < len(data):
            t = data[i]
            l = data[i + 1]
            v = data[i + 2:i + 2 + l]
            cap.fields[t] = v
            i += 2 + l
        return cap

    def to_dict(self) -> Dict:
        """Convertit la capsule en dictionnaire Python pour inspection ou export JSON."""
        d = {}
        for t, v in self.fields.items():
            if t == TLV_TYPES['url']:
                d['url'] = v.decode('utf-8')
            elif t == TLV_TYPES['language']:
                d['language'] = v.decode('utf-8')
            elif t == TLV_TYPES['title']:
                d['title'] = v.decode('utf-8')
            elif t == TLV_TYPES['badge_type']:
                d['badge_type'] = v[0]
            elif t == TLV_TYPES['system_payload']:
                try:
                    d['system_payload'] = json.loads(v.decode('utf-8'))
                except Exception:
                    d['system_payload'] = v.decode('utf-8', errors='replace')
            elif t == TLV_TYPES['retention']:
                d['retention'] = v[0]
            elif t == TLV_TYPES['tag']:
                d['tag'] = {'cycle': v[0], 'subject': v[1], 'sub': v[2]}
            elif t == TLV_TYPES['expires']:
                d['expires'] = struct.unpack('>I', v)[0]
            elif t == TLV_TYPES['hash']:
                d['hash'] = v.hex()
            elif t == TLV_TYPES['signature']:
                d['signature'] = v.hex()
            elif t == TLV_TYPES['authority_id']:
                d['authority_id'] = list(v)
        return d

    @staticmethod
    def from_dict(data: Dict) -> 'icfCapsule':
        """Construit une capsule à partir d’un dictionnaire Python."""
        cap = icfCapsule()
        if 'url' in data:
            cap.set_url(data['url'])
        if 'language' in data:
            cap.set_language(data['language'])
        if 'title' in data:
            cap.set_title(data['title'])
        if 'badge_type' in data:
            cap.set_badge_type(BadgeType(data['badge_type']))
        if 'system_payload' in data:
            payload = data['system_payload']
            if isinstance(payload, (dict, list)):
                cap.set_system_payload(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
            elif isinstance(payload, str):
                try:
                    cap.set_system_payload(bytes.fromhex(payload))
                except ValueError:
                    cap.set_system_payload(payload.encode('utf-8'))
            else:
                cap.set_system_payload(bytes(payload))
        if 'retention' in data:
            cap.set_retention(data['retention'])
        if 'tag' in data:
            tag = data['tag']
            cap.set_tag(tag['cycle'], tag['subject'], tag['sub'])
        if 'expires' in data:
            cap.set_expiration(data['expires'])
        if 'authority_id' in data:
            aid = data['authority_id']
            assert isinstance(aid, list) and len(aid) == 8
            cap.set_authority_id(bytes(aid))
        return cap

    @staticmethod
    def load_json(path: str) -> 'icfCapsule':
        """Charge une capsule depuis un fichier JSON."""
        import json
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return icfCapsule.from_dict(data)

    def verify(self, public_key: Ed25519PublicKey) -> bool:
        """
        Vérifie la signature de la capsule avec une clé publique.

        :param public_key: Clé publique Ed25519
        :return: True si la signature est valide, False sinon.
        """
        if TLV_TYPES['hash'] not in self.fields or TLV_TYPES['signature'] not in self.fields:
            return False
        raw = self.encode_unsigned()
        expected_hash = hashlib.sha256(raw).digest()
        if expected_hash != self.fields[TLV_TYPES['hash']]:
            return False
        try:
            public_key.verify(self.fields[TLV_TYPES['signature']], expected_hash)
            return True
        except Exception:
            return False
