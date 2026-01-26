from sqlalchemy.orm import Session
from app.database.db_connection import get_db
from app.models.usuario import Usuario
from app.auth_utils import pwd_context

def migrar_passwords():
    db: Session = next(get_db())
    usuarios = db.query(Usuario).all()

    for usuario in usuarios:
        if not usuario.password.startswith("$2b$"):
            print(f"🔒 Actualizando contraseña de: {usuario.username}")
            
        MAX_LENGTH = 72
        password = usuario.password[:MAX_LENGTH]
        usuario.password = pwd_context.hash(password)
        db.add(usuario)

    db.commit()
    print("✅ Contraseñas actualizadas correctamente.")

if __name__ == "__main__":
    migrar_passwords()
