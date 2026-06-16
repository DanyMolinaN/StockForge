import sys
import traceback
from PySide6.QtWidgets import QApplication
from backend.repositories.product_repo import SQLiteProductRepository
from backend.repositories.user_repo import SQLiteUserRepository
from backend.services.auth_service import AuthService
from frontend.main_window import MainWindow

if __name__ == "__main__":
    try:
        print("✓ Iniciando aplicación...")
        app = QApplication(sys.argv)
        print("✓ QApplication creado")
        
        # Inyección de dependencias
        db_path = "stockforge.db"
        print(f"✓ Cargando base de datos: {db_path}")
        product_repo = SQLiteProductRepository(db_path)
        print("✓ ProductRepository inicializado")
        
        user_repo = SQLiteUserRepository(db_path)
        print("✓ UserRepository inicializado")
        
        auth_service = AuthService(user_repo)
        print("✓ AuthService inicializado")
        
        print("✓ Creando MainWindow...")
        window = MainWindow(product_repo, auth_service)
        print("✓ MainWindow creado")
        
        print("✓ Mostrando ventana...")
        window.show()
        print("✓ Ventana visible - Iniciando event loop...")
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)