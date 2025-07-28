import subprocess
import tempfile

class Ed25519PrivateKey:
    def __init__(self):
        self._pem = subprocess.run([
            'openssl','genpkey','-algorithm','ed25519'
        ], capture_output=True, check=True).stdout
        self._pub = subprocess.run(
            ['openssl','pkey','-pubout'], input=self._pem,
            capture_output=True, check=True
        ).stdout

    def sign(self, data: bytes) -> bytes:
        with tempfile.NamedTemporaryFile('wb') as priv, \
             tempfile.NamedTemporaryFile('wb') as msg, \
             tempfile.NamedTemporaryFile('rb') as sig:
            priv.write(self._pem); priv.flush()
            msg.write(data); msg.flush()
            subprocess.run([
                'openssl','pkeyutl','-sign','-inkey',priv.name,
                '-in',msg.name,'-out',sig.name,'-rawin','-provider','default'
            ], check=True)
            sig.seek(0)
            return sig.read()

    def public_key(self):
        return Ed25519PublicKey(self._pub)

class Ed25519PublicKey:
    def __init__(self, pem: bytes):
        self._pem = pem

    def verify(self, signature: bytes, data: bytes) -> None:
        with tempfile.NamedTemporaryFile('wb') as pub, \
             tempfile.NamedTemporaryFile('wb') as msg, \
             tempfile.NamedTemporaryFile('wb') as sig:
            pub.write(self._pem); pub.flush()
            msg.write(data); msg.flush()
            sig.write(signature); sig.flush()
            res = subprocess.run([
                'openssl','pkeyutl','-verify','-pubin','-inkey',pub.name,
                '-sigfile',sig.name,'-in',msg.name,'-rawin','-provider','default'
            ], capture_output=True)
            if res.returncode != 0:
                raise ValueError('invalid signature')
