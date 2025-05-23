import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec
from cryptography.hazmat.backends import default_backend

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key, private_key.public_key()

def generate_dsa_keys():
    private_key = dsa.generate_private_key(
        key_size=2048,
        backend=default_backend()
    )
    return private_key, private_key.public_key()

def generate_ecdsa_keys():
    private_key = ec.generate_private_key(
        ec.SECP256R1(),
        backend=default_backend()
    )
    return private_key, private_key.public_key()

def serialize_key(key, is_private=True):
    if is_private:
        return key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
    else:
        return key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

priv_key, pub_key = None, None

st.title("Asymmetric Encryption/Decryption")

# Sidebar Inputs
with st.sidebar:
    st.title("Input:")    
    algorithm = st.selectbox("Select Algorithm", ["RSA", "DSA", "ECDSA"])
    message = st.text_input("Message (Optional)")

    if st.button("Generate Keys"):
        if algorithm == "RSA":
            priv_key, pub_key = generate_rsa_keys()
        elif algorithm == "DSA":
            priv_key, pub_key = generate_dsa_keys()
        elif algorithm == "ECDSA":
            priv_key, pub_key = generate_ecdsa_keys()
        else:
            st.error("Unsupported algorithm selected.")
            st.stop()
            
if priv_key and pub_key:
    st.subheader("Private Key")
    st.code(serialize_key(priv_key, is_private=True))
        
    st.subheader("Public Key")
    st.code(serialize_key(pub_key, is_private=False))
else:
    st.info("Please generate keys from the sidebar.")

        
if message:
    st.markdown("### Message")
    st.write(message)