import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QListWidgetItem, QStackedWidget)
from PyQt5.QtGui import QFont

from agent import init_agent
from workspace import init_workspace
from ui_chat import ChatPage
from ui_apps import AppListPage
from ui_skills import SkillsPage


class AgentGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize workspace on app startup
        init_workspace()
        
        # Initialize agent
        try:
            init_agent()
            self.agent_ready = True
        except Exception as e:
            self.agent_ready = False
            self.error_message = str(e)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AI Agent Chat")
        self.setGeometry(100, 100, 1000, 600)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left sidebar menu
        self.menu_list = QListWidget()
        self.menu_list.setMaximumWidth(150)
        self.menu_list.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                border-right: 1px solid #444;
            }
            QListWidget::item {
                padding: 10px;
                color: #ffffff;
                border: none;
            }
            QListWidget::item:selected {
                background-color: #0e639c;
                border-left: 3px solid #007acc;
            }
            QListWidget::item:hover {
                background-color: #2d2d30;
            }
        """)
        
        # Add menu items
        menu_items = ["AI会话", "应用列表", "技能中心"]
        for item in menu_items:
            self.menu_list.addItem(QListWidgetItem(item))
        
        self.menu_list.itemClicked.connect(self.on_menu_clicked)
        main_layout.addWidget(self.menu_list)
        
        # Right content area (stacked widget for switching views)
        self.stacked_widget = QStackedWidget()
        
        # Page 1: AI Chat
        self.chat_page = ChatPage(
            agent_ready=self.agent_ready, 
            status_callback=self.update_status
        )
        self.stacked_widget.addWidget(self.chat_page)
        
        # Page 2: Application List
        self.app_page = AppListPage()
        self.stacked_widget.addWidget(self.app_page)
        
        # Page 3: Skills
        self.skills_page = SkillsPage()
        self.stacked_widget.addWidget(self.skills_page)
        
        # Set initial page
        self.stacked_widget.setCurrentIndex(0)
        main_layout.addWidget(self.stacked_widget)
        
        # Status bar
        if not self.agent_ready:
            self.statusBar().showMessage(f"Error: {self.error_message}")
        else:
            self.statusBar().showMessage("Ready")
    
    def on_menu_clicked(self, item):
        """Handle menu item clicks"""
        index = self.menu_list.row(item)
        self.stacked_widget.setCurrentIndex(index)
    
    def update_status(self, message):
        """Update status bar message"""
        self.statusBar().showMessage(message)


def main():
    app = QApplication(sys.argv)
    window = AgentGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
