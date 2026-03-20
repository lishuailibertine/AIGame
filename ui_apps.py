from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont


class AppListPage(QWidget):
    """Application list page"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the app list page UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Application List")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Application list
        self.app_list = QListWidget()
        self.app_list.setStyleSheet("""
            QListWidget {
                background-color: #f0f0f0;
                font-size: 11pt;
            }
            QListWidget::item:hover {
                background-color: #e0e0e0;
            }
            QListWidget::item:selected {
                background-color: #0e639c;
                color: white;
            }
        """)
        
        # Sample applications
        self.apps = [
            "AI Chat Assistant",
            "Weather Bot",
            "Task Manager",
            "Document Summarizer",
            "Code Generator"
        ]
        
        self.load_apps()
        layout.addWidget(self.app_list)
    
    def load_apps(self):
        """Load applications into the list"""
        for app in self.apps:
            self.app_list.addItem(QListWidgetItem(app))
    
    def add_app(self, app_name):
        """Add a new application to the list"""
        if app_name not in self.apps:
            self.apps.append(app_name)
            self.app_list.addItem(QListWidgetItem(app_name))
    
    def remove_app(self, app_name):
        """Remove an application from the list"""
        if app_name in self.apps:
            self.apps.remove(app_name)
            for i in range(self.app_list.count()):
                if self.app_list.item(i).text() == app_name:
                    self.app_list.takeItem(i)
                    break
