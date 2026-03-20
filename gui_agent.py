import sys
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QPushButton, QLabel)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor

from main import init_agent, chat


class AgentWorker(QObject):
    """Worker thread for agent responses to avoid blocking GUI"""
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, message):
        super().__init__()
        self.message = message
    
    def run(self):
        try:
            response = chat(self.message)
            self.response_ready.emit(response)
        except Exception as e:
            self.error_occurred.emit(f"Error: {str(e)}")


class AgentGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker_thread = None
        
        # Initialize agent
        try:
            init_agent()
            self.agent_ready = True
        except Exception as e:
            self.agent_ready = False
            self.error_message = str(e)
            self.statusBar().showMessage(f"Error: {self.error_message}")
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AI Agent Chat")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("AI Agent Conversation")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #2b2b2b; color: #ffffff; font-size: 11pt; padding: 5px;")
        main_layout.addWidget(self.chat_display)
        
        # Input area layout
        input_layout = QHBoxLayout()
        
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(80)
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.setStyleSheet("font-size: 11pt;")
        input_layout.addWidget(self.input_field)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setMaximumWidth(100)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("font-weight: bold; font-size: 11pt;")
        input_layout.addWidget(self.send_button)
        
        main_layout.addLayout(input_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def send_message(self):
        """Handle sending a message to the agent"""
        if not self.agent_ready:
            self.chat_display.append("<b>Error:</b> Agent not initialized. Check your API key.")
            return
        
        message = self.input_field.toPlainText().strip()
        if not message:
            return
        
        # Display user message
        self.chat_display.append(f"<b>You:</b> {message}")
        self.input_field.clear()
        self.send_button.setEnabled(False)
        self.statusBar().showMessage("Waiting for response...")
        
        # Create and start worker thread
        self.worker = AgentWorker(message)
        self.worker_thread = threading.Thread(target=self.worker.run)
        self.worker.response_ready.connect(self.on_response)
        self.worker.error_occurred.connect(self.on_error)
        self.worker_thread.start()
    
    def on_response(self, response):
        """Handle agent response"""
        self.chat_display.append(f"<b>Agent:</b> {response}")
        self.send_button.setEnabled(True)
        self.statusBar().showMessage("Ready")
        self.input_field.setFocus()
    
    def on_error(self, error):
        """Handle agent error"""
        self.chat_display.append(f"<b style='color: red;'>Error:</b> {error}")
        self.send_button.setEnabled(True)
        self.statusBar().showMessage("Error occurred")


def main():
    app = QApplication(sys.argv)
    window = AgentGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
