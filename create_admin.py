from sqlmodel import Session, select
from app.db.database import engine
from app.models.models import User
from passlib.hash import bcrypt


def create_admin():
    admin_email = "admin@admin.com"
    admin_name = "Administrador"
    admin_password = "admin123"  # pode trocar depois

    with Session(engine) as session:
        # verifica se o admin já existe
        statement = select(User).where(User.email == admin_email)
        existing = session.exec(statement).first()

        if existing:
            print("🚨 Admin já existe!")
            return

        # cria hash da senha
        password_hash = bcrypt.hash(admin_password[:72])

        admin = User(
            name=admin_name,
            email=admin_email,
            password_hash=password_hash
        )

        session.add(admin)
        session.commit()
        session.refresh(admin)

        print("✅ Admin criado com sucesso!")
        print("Email:", admin_email)
        print("Senha:", admin_password)


if __name__ == "__main__":
    create_admin()
