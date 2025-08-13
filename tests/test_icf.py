import tempfile
import subprocess
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey
    )
    STUB = False
except ModuleNotFoundError:
    import tests.cryptography_stub as cryptography
    sys.modules['cryptography'] = cryptography
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey
    )
    STUB = True

from cli.icf import icfCapsule, BadgeType, Cycle, Matiere

class OpenSSLPrivateKey:
    def __init__(self):
        self.private_pem = subprocess.run([
            'openssl','genpkey','-algorithm','ed25519'], capture_output=True, check=True
        ).stdout
        self.public_pem = subprocess.run(
            ['openssl','pkey','-pubout'], input=self.private_pem,
            capture_output=True, check=True
        ).stdout
    def sign(self, data: bytes) -> bytes:
        with tempfile.NamedTemporaryFile('wb') as priv, \
             tempfile.NamedTemporaryFile('wb') as msg, \
             tempfile.NamedTemporaryFile('rb') as sig:
            priv.write(self.private_pem); priv.flush()
            msg.write(data); msg.flush()
            subprocess.run([
                'openssl','pkeyutl','-sign','-inkey',priv.name,
                '-in',msg.name,'-out',sig.name,'-rawin','-provider','default'
            ], check=True)
            sig.seek(0)
            return sig.read()
    def public_key(self) -> 'OpenSSLPublicKey':
        return OpenSSLPublicKey(self.public_pem)

class OpenSSLPublicKey:
    def __init__(self, pem: bytes):
        self.pem = pem
    def verify(self, signature: bytes, data: bytes) -> None:
        with tempfile.NamedTemporaryFile('wb') as pub, \
             tempfile.NamedTemporaryFile('wb') as msg, \
             tempfile.NamedTemporaryFile('wb') as sig:
            pub.write(self.pem); pub.flush()
            msg.write(data); msg.flush()
            sig.write(signature); sig.flush()
            res = subprocess.run([
                'openssl','pkeyutl','-verify','-pubin','-inkey',pub.name,
                '-sigfile',sig.name,'-in',msg.name,'-rawin','-provider','default'
            ], capture_output=True)
            if res.returncode != 0:
                raise ValueError('invalid signature')


def test_encode_verify_roundtrip():
    priv = OpenSSLPrivateKey()
    pub = priv.public_key()

    cap = icfCapsule()
    cap.set_url('https://example.com')
    cap.set_language('en')
    cap.set_title('Example')

    cap.finalize(priv, b'ABCDEFGH')
    encoded = cap.encode_full()

    decoded = icfCapsule.decode(encoded)

    assert decoded.verify(pub)


def test_badge_type_roundtrip():
    priv = OpenSSLPrivateKey()
    pub = priv.public_key()

    cap = icfCapsule()
    cap.set_badge_type(BadgeType.ADMINISTRATION)
    cap.set_url('https://example.com')
    cap.finalize(priv, b'ABCDEFGH')

    encoded = cap.encode_full()
    decoded = icfCapsule.decode(encoded)

    assert decoded.get_badge_type() == BadgeType.ADMINISTRATION
    assert decoded.verify(pub)


def test_system_payload_roundtrip():
    priv = OpenSSLPrivateKey()
    pub = priv.public_key()

    cap = icfCapsule()
    cap.set_badge_type(BadgeType.CONFIGURATION)
    cap.set_system_payload(b'{"volume":42}')
    cap.finalize(priv, b'ABCDEFGH')

    encoded = cap.encode_full()
    decoded = icfCapsule.decode(encoded)

    assert decoded.get_system_payload() == b'{"volume":42}'
    d = decoded.to_dict()
    assert d['system_payload'] == {"volume": 42}
    assert decoded.verify(pub)


def test_full_fields_roundtrip():
    """Roundtrip including all common TLV fields."""
    priv = OpenSSLPrivateKey()
    pub = priv.public_key()

    cap = icfCapsule()
    cap.set_badge_type(BadgeType.RESSOURCE)
    cap.set_url('https://example.com/page')
    cap.set_language('fr')
    cap.set_title('Titre')
    cap.set_tag(Cycle.CYCLE_2, Matiere.MATHEMATIQUES, 0x42)
    cap.set_retention(3)
    cap.set_expiration(1670000000)
    cap.finalize(priv, b'ABCDEFGH')

    encoded = cap.encode_full()
    decoded = icfCapsule.decode(encoded)

    d = decoded.to_dict()
    assert d['url'] == 'https://example.com/page'
    assert d['language'] == 'fr'
    assert d['title'] == 'Titre'
    assert d['tag'] == {
        'cycle': Cycle.CYCLE_2.value,
        'subject': Matiere.MATHEMATIQUES.value,
        'sub': 0x42,
    }
    assert d['retention'] == 3
    assert d['expires'] == 1670000000
    assert decoded.get_badge_type() == BadgeType.RESSOURCE
    assert decoded.verify(pub)


def test_binary_payload_admin():
    """System payload roundtrip with raw binary data for admin badges."""
    priv = OpenSSLPrivateKey()
    pub = priv.public_key()

    cap = icfCapsule()
    cap.set_badge_type(BadgeType.ADMINISTRATION)
    cap.set_system_payload(b"\x00\x01\x02")
    cap.finalize(priv, b'ABCDEFGH')

    decoded = icfCapsule.decode(cap.encode_full())
    assert decoded.get_badge_type() == BadgeType.ADMINISTRATION
    assert decoded.get_system_payload() == b"\x00\x01\x02"
    assert decoded.verify(pub)


def test_invalid_signature():
    """Verification must fail with the wrong public key."""
    priv1 = OpenSSLPrivateKey()
    priv2 = OpenSSLPrivateKey()

    cap = icfCapsule()
    cap.set_url('https://example.com')
    cap.finalize(priv1, b'ABCDEFGH')

    bad_pub = priv2.public_key()
    decoded = icfCapsule.decode(cap.encode_full())
    assert not decoded.verify(bad_pub)


def test_cli_list_tags_runs():
    """Ensure the CLI entry point exposes list-tags without import errors."""
    if STUB:
        cmd = [
            sys.executable,
            '-c',
            (
                'import sys, runpy, tests.cryptography_stub as cryptography; '
                'sys.modules["cryptography"] = cryptography; '
                'sys.argv=["cli.icfcli", "list-tags"]; '
                'runpy.run_module("cli.icfcli", run_name="__main__")'
            )
        ]
    else:
        cmd = [sys.executable, '-m', 'cli.icfcli', 'list-tags']
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert 'Cycles pédagogiques' in res.stdout


def run_cli(args):
    """Utility to invoke the icf CLI with or without the crypto stub."""
    if STUB:
        return subprocess.run(
            [
                sys.executable,
                '-c',
                (
                    'import sys, runpy, tests.cryptography_stub as cryptography; '
                    'sys.modules["cryptography"] = cryptography; '
                    'sys.argv=["cli.icfcli"] + ' + repr(args) + '; '
                    'runpy.run_module("cli.icfcli", run_name="__main__")'
                ),
            ],
            capture_output=True,
            text=True,
        )
    return subprocess.run(
        [sys.executable, '-m', 'cli.icfcli', *args],
        capture_output=True,
        text=True,
    )


def create_keypair(tmp):
    priv = os.path.join(tmp, 'priv.pem')
    pub = os.path.join(tmp, 'pub.pem')
    subprocess.run(['openssl', 'genpkey', '-algorithm', 'ed25519', '-out', priv], check=True)
    subprocess.run(['openssl', 'pkey', '-in', priv, '-pubout', '-out', pub], check=True)
    return priv, pub


def test_cli_encode_decode_roundtrip(tmp_path):
    if STUB:
        pytest.skip('cryptography not available')
    priv, pub = create_keypair(tmp_path)
    icf_file = tmp_path / 'test.icf'

    res = run_cli([
        'encode',
        '--url', 'https://example.com',
        '--private-key', str(priv),
        '--authority-id', '0011223344556677',
        '--output', str(icf_file),
    ])
    assert res.returncode == 0

    res = run_cli([
        'decode',
        '--input', str(icf_file),
        '--public-key', str(pub),
    ])
    assert res.returncode == 0
    assert '"url": "https://example.com"' in res.stdout


def test_cli_export_import_json(tmp_path):
    if STUB:
        pytest.skip('cryptography not available')
    priv, pub = create_keypair(tmp_path)
    icf_file = tmp_path / 'orig.icf'
    json_file = tmp_path / 'out.json'
    icf2 = tmp_path / 'new.icf'

    run_cli([
        'encode',
        '--url', 'https://example.com',
        '--private-key', str(priv),
        '--authority-id', '0011223344556677',
        '--output', str(icf_file),
    ])

    res = run_cli([
        'export-json',
        '--input', str(icf_file),
        '--output', str(json_file),
    ])
    assert res.returncode == 0 and json_file.exists()

    res = run_cli([
        'import-json',
        '--input', str(json_file),
        '--private-key', str(priv),
        '--authority-id', '0011223344556677',
        '--output', str(icf2),
    ])
    assert res.returncode == 0 and icf2.exists()

    res = run_cli(['decode', '--input', str(icf2), '--public-key', str(pub)])
    assert res.returncode == 0
    assert '"url": "https://example.com"' in res.stdout


def test_cli_validation_errors(tmp_path):
    if STUB:
        pytest.skip('cryptography not available')
    priv, _ = create_keypair(tmp_path)
    icf_file = tmp_path / 'x.icf'

    res = run_cli([
        'encode',
        '--badge-type', 'configuration',
        '--private-key', str(priv),
        '--authority-id', '0011223344556677',
        '--output', str(icf_file),
    ])
    assert res.returncode != 0

    res = run_cli([
        'encode',
        '--badge-type', 'configuration',
        '--payload', '{"a":1}',
        '--title', 'ignored',
        '--private-key', str(priv),
        '--authority-id', '0011223344556677',
        '--output', str(icf_file),
    ])
    assert 'Avertissement' in res.stdout
