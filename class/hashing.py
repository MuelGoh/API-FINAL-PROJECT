from passlib.context import CryptContext

# This next line creates an instance of the CryptContext Class and specifies using bcrypt as the hashing algorithm
# The deprecated parameter indicates that the library should automatically handle deprecated features
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# We use this password as an example to hash
password = "qwerty"

# This creates a hashed password
hashed_password = bcrypt_context.hash(password)

print(hashed_password)
# => $2b$12$bP4zk110DL0iL8Oi660e4uq5rfwn5Kr.k2m32VO3kZuni9UNjSVte

# The process to very if a password is correct:
verified = bcrypt_context.verify(password, "$2b$12$bP4zk110DL0iL8Oi660e4uq5rfwn5Kr.k2m32VO3kZuni9UNjSVte")

print(verified)
# => True
