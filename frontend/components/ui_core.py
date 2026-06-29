# frontend/components/ui_core.py

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QTableWidget, QHeaderView, QWidget
)

class CardPanel(QFrame):
    def __init__(self, margins=12, spacing=12):
        super().__init__()
        self.setProperty("role", "card")
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(margins, margins, margins, margins)
        self.content_layout.setSpacing(spacing)

    def add_widget(self, widget, stretch=0):
        self.content_layout.addWidget(widget, stretch)

    def add_layout(self, layout, stretch=0):
        self.content_layout.addLayout(layout, stretch)


class PageHeader(QWidget):
    def __init__(self, title_text: str, subtitle_text: str = None):
        super().__init__()
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        lbl_title = QLabel(title_text)
        lbl_title.setProperty("role", "h1")
        text_layout.addWidget(lbl_title)
        
        if subtitle_text:
            lbl_subtitle = QLabel(subtitle_text)
            lbl_subtitle.setProperty("role", "body")
            text_layout.addWidget(lbl_subtitle)
            
        self.main_layout.addLayout(text_layout)
        self.main_layout.addStretch()
        
        self.actions_layout = QHBoxLayout()
        self.main_layout.addLayout(self.actions_layout)

    def add_action(self, widget):
        self.actions_layout.addWidget(widget)


class StandardTable(QTableWidget):
    def __init__(self, headers: list[str]):
        super().__init__(0, len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)