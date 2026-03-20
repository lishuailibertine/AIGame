"""Skill management for the AI agent"""
import re
from pathlib import Path
from workspace import get_workspace


class SkillManager:
    """Manage agent skills loaded from workspace"""
    
    def __init__(self):
        """Initialize skill manager"""
        self.workspace = get_workspace()
        self.skills_dir = self.workspace.skills_dir
        self.skills = []
        self.load_skills()
    
    def _parse_skill_md(self, skill_dir):
        """Parse SKILL.md file from skill directory"""
        skill_md_file = skill_dir / "SKILL.md"
        
        if not skill_md_file.exists():
            return None
        
        try:
            with open(skill_md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            skill_info = {
                "name": skill_dir.name,
                "path": str(skill_dir),
                "skill_md_path": str(skill_md_file),
                "type": "skill_dir"
            }
            
            # Extract YAML frontmatter if exists
            if content.startswith("---"):
                match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
                if match:
                    frontmatter = match.group(1)
                    # Parse YAML-like key-value pairs
                    for line in frontmatter.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            skill_info[key.strip()] = value.strip()
                
                # Extract description from first markdown heading/paragraph
                body = content[match.end():].strip()
            else:
                body = content
            
            # Extract title from first markdown heading
            title_match = re.search(r'^#+\s+(.+)$', body, re.MULTILINE)
            if title_match and "title" not in skill_info:
                skill_info["title"] = title_match.group(1)
            
            # Extract description from first paragraph
            para_match = re.search(r'^(?!#+)(.+?)(?:\n\n|\Z)', body, re.MULTILINE)
            if para_match and "description" not in skill_info:
                description = para_match.group(1).strip()
                if description and not description.startswith('#'):
                    skill_info["description"] = description
            
            return skill_info
        except Exception as e:
            print(f"Error parsing skill {skill_dir.name}: {str(e)}")
            return None
    
    def load_skills(self):
        """Load all skills from the skills directory"""
        self.skills = []
        
        if not self.skills_dir.exists():
            return
        
        # Load all skill directories (each containing SKILL.md)
        for item in self.skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                skill = self._parse_skill_md(item)
                if skill:
                    self.skills.append(skill)
    
    def get_skills(self):
        """Get all loaded skills"""
        return self.skills
    
    def add_skill(self, skill_name, skill_md_content):
        """Add a new skill directory with SKILL.md file"""
        skill_dir = self.skills_dir / skill_name
        skill_md_file = skill_dir / "SKILL.md"
        
        try:
            skill_dir.mkdir(parents=True, exist_ok=True)
            with open(skill_md_file, 'w', encoding='utf-8') as f:
                f.write(skill_md_content)
            
            self.load_skills()
            return True
        except Exception as e:
            print(f"Error adding skill: {str(e)}")
            return False
    
    def remove_skill(self, skill_name):
        """Remove a skill directory from the workspace"""
        skill_dir = self.skills_dir / skill_name
        
        try:
            if skill_dir.exists() and skill_dir.is_dir():
                # Remove all files in the skill directory
                for file in skill_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                    elif file.is_dir():
                        import shutil
                        shutil.rmtree(file)
                # Remove the skill directory itself
                skill_dir.rmdir()
                self.load_skills()
                return True
        except Exception as e:
            print(f"Error removing skill: {str(e)}")
        
        return False
    
    def get_skill(self, skill_name):
        """Get a specific skill by name"""
        for skill in self.skills:
            if skill.get("name") == skill_name or skill.get("title") == skill_name:
                return skill
        return None
    
    def get_skill_content(self, skill_name):
        """Get the full content of a skill's SKILL.md file"""
        skill_dir = self.skills_dir / skill_name
        skill_md_file = skill_dir / "SKILL.md"
        
        try:
            if skill_md_file.exists():
                with open(skill_md_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading skill content: {str(e)}")
        
        return None


# Global skill manager instance
_skill_manager = None


def get_skill_manager():
    """Get or create global skill manager"""
    global _skill_manager
    if _skill_manager is None:
        _skill_manager = SkillManager()
    return _skill_manager


def load_skills():
    """Load all skills"""
    return get_skill_manager().get_skills()
