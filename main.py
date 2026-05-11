import sys
from PySide6.QtWidgets import QApplication
from app.backend.repositories.product_repo import SQLiteProductRepository
from app.frontend.main_window import MainWindow
# Codigo Nuevo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Inyección de dependencias
    repository = SQLiteProductRepository("stockforge.db")
    window = MainWindow(repository)
    
    window.show()
    sys.exit(app.exec())