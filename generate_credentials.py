import os
import random
import string
import bcrypt

def generate_credentials():
    """Generate random username and password, hash password, and create .env file."""
    
    # Generate username: 'm' followed by 5 random digits
    username = 'm' + ''.join(random.choices(string.digits, k=5))
    
    # Generate password: 16 characters with letters, digits, and special characters
    password_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choices(password_chars, k=16))
    
    # Hash the password using bcrypt
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create .env file content
    env_content = f"""API_USERNAME={username}
API_PASSWORD={password}
API_PASSWORD_HASH={password_hash}
DATABASE_URL=sqlite:///./tournament_planner.db
"""
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    # Print credentials to console
    print("=" * 60)
    print("Tournament Planner API - Generated Credentials")
    print("=" * 60)
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Password Hash: {password_hash}")
    print(f"Database URL: sqlite:///./tournament_planner.db")
    print("=" * 60)
    print(".env file created successfully!")
    print("=" * 60)

if __name__ == "__main__":
    generate_credentials()
