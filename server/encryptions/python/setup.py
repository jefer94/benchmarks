from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat

private_key = Ed25519PrivateKey.generate()

with open(".ed25519.private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=Encoding.PEM, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption()
    ))

with open(".ed25519.public_key.pem", "wb") as f:
    f.write(private_key.public_key().public_bytes(
        encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo
    ))

with open(".ed25519.private_key", "wb") as f:
    f.write(private_key.private_bytes(
        # encoding=Encoding.PEM, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption()
        encoding=Encoding.Raw, format=PrivateFormat.Raw, encryption_algorithm=NoEncryption()
    ))

with open(".ed25519.public_key", "wb") as f:
    f.write(private_key.public_key().public_bytes(
        # encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo
        encoding=Encoding.Raw, format=PublicFormat.Raw
    ))

# from cryptography.hazmat.primitives.asymmetric.dsa import DSAPrivateKey, generate_private_key
# from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat

# private_key = generate_private_key(2048)

# with open(".dsa2048.private_key.pem", "wb") as f:
#     f.write(private_key.private_bytes(encoding=Encoding.PEM, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption()))

# with open(".2048.public_key.pem", "wb") as f:
#     f.write(private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo))

# private_key = generate_private_key(4096)

# with open(".dsa4096.private_key.pem", "wb") as f:
#     f.write(private_key.private_bytes(encoding=Encoding.PEM, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption()))

# with open(".dsa4096.public_key.pem", "wb") as f:
#     f.write(private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo))

