from passlib.context import CryptContext

from libs.database import db_session
from libs.models import AdminUser

pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
email = input("email:")
password = input("password:")
with db_session() as db:
    admin_user = AdminUser(email=email, hashed_password=pwd.hash(password), is_active=True, is_superuser=True)
    db.add(admin_user)
    db.commit()
