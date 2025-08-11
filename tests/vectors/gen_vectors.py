import json, hashlib, struct, time
from pathlib import Path
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
except Exception as e:
    raise RuntimeError("cryptography est requis (pip install cryptography)") from e

def tlv(tag, value: bytes) -> bytes:
    if not (0 <= tag <= 0xFF): raise ValueError("tag out of range")
    if not (0 <= len(value) <= 255): raise ValueError("TLV length must fit in 1 byte")
    return bytes([tag, len(value)]) + value

def build_lite(title=None, url=None, language=None, ped_tag=None, expiration=None):
    b = b""
    if url: b += tlv(0x01, url.encode())
    if language:
        lb = language.encode("ascii")
        if len(lb) != 2: raise ValueError("language must be 2 letters")
        b += tlv(0x02, lb)
    if title:
        tb = title.encode("utf-8")
        if len(tb) > 64: raise ValueError("title too long")
        b += tlv(0x03, tb)
    if ped_tag:
        c,s,sc = ped_tag
        b += tlv(0x04, bytes([c&0xFF, s&0xFF, sc&0xFF]))
    if expiration is not None:
        b += tlv(0x06, struct.pack(">I", expiration & 0xFFFFFFFF))
    return b

def build_full(url=None, title=None, language=None, ped_tag=None, retention=None, expiration=None, badge_type=None, sys_payload: bytes=None):
    b = b""
    if url:
        ub = url.encode("utf-8")
        if len(ub) > 200: raise ValueError("URL too long")
        b += tlv(0x01, ub)
    if language:
        lb = language.encode("ascii")
        if len(lb) != 2: raise ValueError("language must be 2 letters")
        b += tlv(0x02, lb)
    if title:
        tb = title.encode("utf-8")
        if len(tb) > 64: raise ValueError("title too long")
        b += tlv(0x03, tb)
    if ped_tag:
        c,s,sc = ped_tag
        b += tlv(0x04, bytes([c&0xFF, s&0xFF, sc&0xFF]))
    if retention is not None:
        b += tlv(0x05, bytes([retention & 0xFF]))
    if expiration is not None:
        b += tlv(0x06, struct.pack(">I", expiration & 0xFFFFFFFF))
    if badge_type is not None:
        b += tlv(0xE0, bytes([badge_type & 0xFF]))
    if sys_payload is not None:
        b += tlv(0xE1, sys_payload)
    f2 = hashlib.sha256(b).digest()
    b += tlv(0xF2, f2)
    SK = bytes.fromhex("9fbe9a6d13b3c6c6928c0f68a86dd84cd27b4589fdc2f40c79c1f854be431db7")
    sig = Ed25519PrivateKey.from_private_bytes(SK).sign(f2)
    b += tlv(0xF3, sig)
    b += tlv(0xF4, bytes.fromhex("0123456789abcdef"))
    return b

if __name__ == "__main__":
    out = Path(__file__).parent
    now = int(time.time())
    vecs = []
    lite_valid_1 = build_lite(title="Hello Lite 1", language="fr")
    lite_valid_2 = build_lite(url="https://lite.example/2", language="en", ped_tag=(1,2,3))
    full_valid_1 = build_full(url="https://example.com/1", title="Full One", language="fr", ped_tag=(2,1,0), expiration=now+3600, badge_type=0)
    full_valid_2 = build_full(url="https://example.com/2", title="Full Two", language="en", ped_tag=(3,4,5), retention=7, expiration=now+86400, badge_type=0)
    invalid_sig = bytearray(full_valid_1)
    idx = invalid_sig.find(b"\xF3")
    if idx != -1 and idx+1 < len(invalid_sig):
        L = invalid_sig[idx+1]
        start = idx+2
        if start+L <= len(invalid_sig):
            invalid_sig[start+L-1] ^= 0xFF
    invalid_missing_tag = bytearray(full_valid_2)
    idx2 = invalid_missing_tag.find(b"\xF2")
    if idx2 != -1 and idx2+1 < len(invalid_missing_tag):
        L2 = invalid_missing_tag[idx2+1]
        del invalid_missing_tag[idx2: idx2+2+L2]
    files = [
        ("lite_valid_1.icf", lite_valid_1, {"strict_verify": False, "profile": "lite"}),
        ("lite_valid_2.icf", lite_valid_2, {"strict_verify": False, "profile": "lite"}),
        ("full_valid_1.icf", full_valid_1, {"strict_verify": True, "profile": "full"}),
        ("full_valid_2.icf", full_valid_2, {"strict_verify": True, "profile": "full"}),
        ("invalid_sig.icf", bytes(invalid_sig), {"strict_verify": False, "error": "ICF_ERR_INVALID_SIGNATURE"}),
        ("invalid_missing_tag.icf", bytes(invalid_missing_tag), {"strict_verify": False, "error": "ICF_ERR_FORMAT"}),
    ]
    manifest = []
    for name, data, expect in files:
        (out / name).write_bytes(data)
        manifest.append({"file": name, "expected": expect})
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("OK - vectors regenerated")
