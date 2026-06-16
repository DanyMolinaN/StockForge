import sys
import traceback
from PySide6.QtWidgets import QApplication

# 1. Importamos nuestro nuevo DatabaseManager
from backend.core.database import DatabaseManager
from backend.repositories.product_repo import SQLiteProductRepository
from backend.repositories.user_repo import SQLiteUserRepository
from backend.services.auth_service import AuthService
from frontend.main_window import MainWindow

if __name__ == "__main__":
    try:
        print("✓ Iniciando aplicación...")
        app = QApplication(sys.argv)
        print("✓ QApplication creado")
        db_path = "stockforge.db"
        print(f"✓ Cargando base de datos: {db_path}")
        db_manager = DatabaseManager(db_path)
        print("✓ DatabaseManager inicializado")
        product_repo = SQLiteProductRepository(db_manager)
        print("✓ ProductRepository inicializado")       
        user_repo = SQLiteUserRepository(db_manager)
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