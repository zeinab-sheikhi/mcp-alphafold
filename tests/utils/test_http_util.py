import pytest
from ssl import SSLContext, TLSVersion
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from datetime import datetime, timedelta
from mcp_alphafold.utils.http_util import (
    get_ssl_context,
)


@pytest.fixture
def mock_cert_files(tmp_path):
    """Create valid self-signed certificate and private key for testing"""
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Generate certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"test.local"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=1)
    ).sign(private_key, hashes.SHA256())

    # Write certificate and private key to files
    cert_file = tmp_path / "cert.pem"
    key_file = tmp_path / "key.pem"
    
    cert_file.write_bytes(cert.public_bytes(Encoding.PEM))
    key_file.write_bytes(
        private_key.private_bytes(
            Encoding.PEM,
            PrivateFormat.PKCS8,
            NoEncryption()
        )
    )
    
    return str(cert_file), str(key_file)


def test_get_ssl_context(mock_cert_files, monkeypatch):
    cert_file, key_file = mock_cert_files
    monkeypatch.setenv("SSL_CERT_FILE", cert_file)
    monkeypatch.setenv("SSL_KEY_FILE", key_file)

    context = get_ssl_context(cert_file, key_file)
    assert isinstance(context, SSLContext)
    assert context.maximum_version == TLSVersion.TLSv1_3


def test_get_ssl_context_file_not_found():
    with pytest.raises(FileNotFoundError):
        get_ssl_context("nonexistent_cert.pem", "nonexistent_key.pem")

