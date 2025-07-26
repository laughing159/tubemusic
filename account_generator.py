import random
import string
from datetime import datetime, timedelta
from faker import Faker
from typing import List
from config import AccountData
from loguru import logger

class AccountGenerator:
    def __init__(self, locale='en_US'):
        self.fake = Faker(locale)
        
    def generate_email(self, domain: str = None) -> str:
        """Generate a realistic email address"""
        domains = domain if domain else [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
            'protonmail.com', 'icloud.com'
        ]
        
        if isinstance(domains, str):
            domains = [domains]
            
        username_styles = [
            f"{self.fake.first_name().lower()}.{self.fake.last_name().lower()}",
            f"{self.fake.first_name().lower()}{self.fake.last_name().lower()}",
            f"{self.fake.first_name().lower()}_{self.fake.last_name().lower()}",
            f"{self.fake.first_name().lower()}{random.randint(100, 9999)}",
            f"{self.fake.user_name()}{random.randint(10, 999)}"
        ]
        
        username = random.choice(username_styles)
        domain = random.choice(domains)
        
        return f"{username}@{domain}"
    
    def generate_password(self, length: int = 12, include_special: bool = True) -> str:
        """Generate a strong password"""
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*"
        
        # Ensure at least one character from each category
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits)
        ]
        
        if include_special:
            password.append(random.choice(special))
            all_chars = lowercase + uppercase + digits + special
        else:
            all_chars = lowercase + uppercase + digits
        
        # Fill the rest randomly
        for _ in range(length - len(password)):
            password.append(random.choice(all_chars))
        
        # Shuffle the password
        random.shuffle(password)
        return ''.join(password)
    
    def generate_phone(self, country_code: str = '+1') -> str:
        """Generate a phone number"""
        if country_code == '+1':  # US format
            area_code = random.randint(200, 999)
            exchange = random.randint(200, 999)
            number = random.randint(1000, 9999)
            return f"{country_code}({area_code}){exchange}-{number}"
        else:
            # Generic international format
            return self.fake.phone_number()
    
    def generate_birth_date(self, min_age: int = 18, max_age: int = 65) -> str:
        """Generate a birth date for someone between min_age and max_age"""
        today = datetime.now()
        min_birth = today - timedelta(days=max_age * 365)
        max_birth = today - timedelta(days=min_age * 365)
        
        birth_date = self.fake.date_between(start_date=min_birth, end_date=max_birth)
        return birth_date.strftime("%m/%d/%Y")
    
    def generate_account_data(self, email_domain: str = None) -> AccountData:
        """Generate complete account data"""
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        
        account_data = AccountData(
            email=self.generate_email(email_domain),
            password=self.generate_password(),
            first_name=first_name,
            last_name=last_name,
            phone=self.generate_phone(),
            recovery_email=self.generate_email(),
            birth_date=self.generate_birth_date()
        )
        
        logger.info(f"Generated account data for {first_name} {last_name}")
        return account_data
    
    def generate_multiple_accounts(self, count: int, email_domain: str = None) -> List[AccountData]:
        """Generate multiple account datasets"""
        accounts = []
        for i in range(count):
            try:
                account = self.generate_account_data(email_domain)
                accounts.append(account)
                logger.info(f"Generated account {i+1}/{count}")
            except Exception as e:
                logger.error(f"Failed to generate account {i+1}: {e}")
                continue
        
        return accounts
    
    def generate_gmail_specific_data(self) -> AccountData:
        """Generate data specifically formatted for Gmail registration"""
        return self.generate_account_data("gmail.com")
    
    def generate_cursor_specific_data(self) -> AccountData:
        """Generate data for Cursor registration (simpler requirements)"""
        account = self.generate_account_data()
        # Cursor might not need phone verification
        account.phone = ""
        return account