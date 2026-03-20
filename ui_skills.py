from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
                             QListWidgetItem, QPushButton, QScrollArea)
from PyQt5.QtGui import QFont
from skill_manager import get_skill_manager


class SkillsPage(QWidget):
    """Skills management page"""
    
    def __init__(self):
        super().__init__()
        self.skill_manager = get_skill_manager()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the skills page UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Local Skills")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Skills list
        self.skills_list = QListWidget()
        self.skills_list.setStyleSheet("""
            QListWidget {
                background-color: #f0f0f0;
                font-size: 11pt;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget::item:hover {
                background-color: #e0e0e0;
            }
            QListWidget::item:selected {
                background-color: #0e639c;
                color: white;
            }
        """)
        
        layout.addWidget(self.skills_list)
        
        # Button area
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_skills)
        button_layout.addWidget(refresh_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Load skills
        self.refresh_skills()
    
    def refresh_skills(self):
        """Refresh and display all available skills"""
        self.skills_list.clear()
        self.skill_manager.load_skills()
        skills = self.skill_manager.get_skills()
        
        if not skills:
            no_skills_item = QListWidgetItem("No skills available")
            no_skills_item.setFlags(no_skills_item.flags() & ~1)  # Disable selection
            self.skills_list.addItem(no_skills_item)
        else:
            for skill in skills:
                skill_name = skill.get("name", "Unknown")
                skill_title = skill.get("title", skill_name)
                skill_description = skill.get("description", "")
                
                # Display skill title and description
                display_text = skill_title
                if skill_description:
                    # Truncate long descriptions
                    desc = skill_description[:100]
                    if len(skill_description) > 100:
                        desc += "..."
                    display_text += f"\n{desc}"
                
                item = QListWidgetItem(display_text)
                self.skills_list.addItem(item)
    
    def get_selected_skill(self):
        """Get the currently selected skill"""
        current_item = self.skills_list.currentItem()
        if current_item:
            skill_name = current_item.text().split('\n')[0]
            return self.skill_manager.get_skill(skill_name)
        return None
