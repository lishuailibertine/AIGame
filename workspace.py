import os
from pathlib import Path


class WorkspaceManager:
    """Manage application workspace directory for user data"""
    
    # Application name
    APP_NAME = "AIGame"
    
    def __init__(self):
        """Initialize workspace manager"""
        self.workspace_path = self._get_workspace_path()
        self.init_workspace()
    
    def _get_workspace_path(self):
        """Get workspace path based on OS"""
        home = Path.home()
        
        # Use platform-specific paths
        if os.name == 'nt':  # Windows
            workspace = home / "AppData" / "Local" / self.APP_NAME
        else:  # macOS and Linux
            # Prefer ~/.config/appname following XDG standards, but also support Library on macOS
            workspace = home / ".config" / self.APP_NAME.lower()
        
        return workspace
    
    def init_workspace(self):
        """Initialize workspace directories"""
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different purposes
        self.conversations_dir.mkdir(parents=True, exist_ok=True)
        self.configs_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def workspace_dir(self):
        """Get workspace root directory"""
        return self.workspace_path
    
    @property
    def conversations_dir(self):
        """Get conversations storage directory"""
        return self.workspace_path / "conversations"
    
    @property
    def configs_dir(self):
        """Get configs directory"""
        return self.workspace_path / "configs"
    
    @property
    def skills_dir(self):
        """Get skills directory"""
        return self.configs_dir / "skills"
    
    @property
    def data_dir(self):
        """Get data directory"""
        return self.workspace_path / "data"
    
    def get_conversation_path(self, conversation_id):
        """Get path for a specific conversation file"""
        return self.conversations_dir / f"{conversation_id}.json"
    
    def get_config_path(self, config_name):
        """Get path for a specific config file"""
        return self.configs_dir / f"{config_name}.json"
    
    def get_data_path(self, filename):
        """Get path for a data file"""
        return self.data_dir / filename
    
    def __str__(self):
        """Return workspace path as string"""
        return str(self.workspace_path)


# Global workspace instance
_workspace = None


def get_workspace():
    """Get or create global workspace manager"""
    global _workspace
    if _workspace is None:
        _workspace = WorkspaceManager()
    return _workspace


def init_workspace():
    """Initialize workspace on app startup"""
    return get_workspace()
