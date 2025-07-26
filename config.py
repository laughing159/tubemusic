import os
from typing import Dict, Any
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class AutomationConfig(BaseModel):
    # Browser settings
    headless: bool = False
    implicit_wait: int = 10
    page_load_timeout: int = 30
    
    # Proxy settings (optional)
    proxy_host: str = ""
    proxy_port: int = 0
    
    # Rate limiting
    min_delay: float = 2.0
    max_delay: float = 5.0
    
    # User agent rotation
    rotate_user_agents: bool = True
    
    # Output settings
    log_level: str = "INFO"
    output_file: str = "registered_accounts.json"
    
    # Security settings
    use_undetected_chrome: bool = True
    disable_images: bool = True
    disable_javascript: bool = False

class AccountData(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str = ""
    recovery_email: str = ""
    birth_date: str = ""
    
def get_config() -> AutomationConfig:
    return AutomationConfig()

# Default credentials (should be moved to .env file)
DEFAULT_SETTINGS = {
    "gmail": {
        "base_url": "https://accounts.google.com/signup",
        "required_fields": ["first_name", "last_name", "email", "password", "phone"],
        "verification_required": True
    },
    "cursor": {
        "base_url": "https://cursor.sh/sign-up",
        "required_fields": ["email", "password"],
        "verification_required": True
    }
}