import sys
import traceback
from PySide6.QtWidgets import QApplication
from backend.core.database import DatabaseManager
from backend.repositories.product_repo import SQLiteProductRepository
from backend.repositories.user_repo import SQLiteUserRepository
from backend.services.auth_service import AuthService
from frontend.main_window import MainWindow

# 1. IMPORTAR EL NUEVO REPOSITORIO
from backend.repositories.permission_repo import SQLitePermissionRepository

if __name__ == "__main__":
    try:
        print("✓ Iniciando aplicación...")
        app = QApplication(sys.argv)
        
        db_path = "stockforge.db"
        db_manager = DatabaseManager(db_path)
        
        product_repo = SQLiteProductRepository(db_manager)
        user_repo = SQLiteUserRepository(db_manager)
        
        # 2. INICIALIZAR EL REPOSITORIO DE PERMISOS
        permission_repo = SQLitePermissionRepository(db_path)
        print("✓ PermissionRepository inicializado")       
        
        # 3. INYECTAR AMBOS REPOSITORIOS EN AUTH_SERVICE
        auth_service = AuthService(user_repo, permission_repo)
        print("✓ AuthService inicializado")       
        
        window = MainWindow(product_repo, auth_service)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)