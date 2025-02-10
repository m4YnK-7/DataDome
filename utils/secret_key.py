import secrets

def generate_secret_key():
    return secrets.token_hex(32)  # Generates a 64-character hex string

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated Secret Key:", secret_key)