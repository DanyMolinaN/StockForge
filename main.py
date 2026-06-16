# main.py

import sys
from PySide6.QtWidgets import QApplication
from backend.core.database import DatabaseManager
from backend.repositories.product_repo import SQLiteProductRepository
from backend.repositories.user_repo import SQLiteUserRepository
from backend.repositories.permission_repo import SQLitePermissionRepository
from backend.services.auth_service import AuthService
from frontend.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    db_manager = DatabaseManager("stockforge.db")
    user_repo = SQLiteUserRepository(db_manager)
    permission_repo = SQLitePermissionRepository(db_manager) 
    product_repo = SQLiteProductRepository(db_manager)
    auth_service = AuthService(user_repo, permission_repo)
    window = MainWindow(repository=product_repo, auth_service=auth_service)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()