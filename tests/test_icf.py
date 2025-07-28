import tempfile
import subprocess
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from icf.cli.icf import icfCapsule, BadgeType

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


def test_cli_list_tags_runs():
    """Ensure the CLI entry point exposes list-tags without import errors."""
    res = subprocess.run([
        sys.executable, '-m', 'icf.cli.icfcli', 'list-tags'
    ], capture_output=True, text=True)
    assert res.returncode == 0
    assert 'Cycles pédagogiques' in res.stdout
