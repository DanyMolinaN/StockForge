APP_STYLE = """
QWidget {
    background-color: #f7f8fb;
    font-family: 'Inter', sans-serif;
    color: #1f2a37;
    font-size: 14px;
}
QFrame#panel {
    background-color: #ffffff;
    border: 1px solid #d7e0eb;
    border-radius: 12px;
}
QLabel#eyebrow {
    color: #3b82f6;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 12px;
}
QLabel#title {
    font-size: 24px;
    font-weight: bold;
}
QLineEdit, QDoubleSpinBox, QSpinBox {
    border: 1px solid #d7e0eb;
    border-radius: 8px;
    padding: 8px;
    background-color: #f1f5fb;
}
QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus {
    border-color: #3b82f6;
}
QPushButton#btnPrimary {
    background-color: #3b82f6;
    color: white;
    border-radius: 8px;
    padding: 12px 20px;
    font-weight: bold;
}
QPushButton#btnPrimary:hover {
    background-color: #2f6ad8;
}
QTableWidget {
    background-color: #ffffff;
    border: none;
    gridline-color: #d7e0eb;
}
QHeaderView::section {
    background-color: #ffffff;
    padding: 12px;
    border: none;
    border-bottom: 1px solid #d7e0eb;
    color: #6d7a8d;
    font-weight: bold;
    text-align: left;
}
"""