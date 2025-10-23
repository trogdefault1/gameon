#!/usr/bin/env python3
"""
Simplified GameOn Fingerprint Generator & CapMonster Cloud Turnstile Solver
=======================================================================

This script focuses only on:
1. Fingerprint generation (matching JavaScript logic)
2. CapMonster Cloud Turnstile captcha solving
3. Basic API testing and validation

Stops before carting/login functionality.
"""

from __future__ import annotations

import json
import random
import time
import threading
from typing import Dict, Optional
import tls_client
from colorama import Fore, Style, init
import requests

# Initialize colorama
init(autoreset=True)

# =============================================================================
# CONFIGURATION - EDIT THESE VALUES
# =============================================================================

# CapMonster Cloud API Configuration
CAPMONSTER_CLOUD_API_KEY = "YOUR_CAPMONSTER_CLOUD_API_KEY_HERE"

# GameOn Configuration
GAMEON_WEBSITE_URL = "https://www.gameon.games/"
GAMEON_WEBSITE_KEY = "0x4AAAAAABww3o50PYtmz9wv"

# Processing Configuration
MAX_WORKERS = 1

class FingerprintGenerator:
    """Generates fingerprint IDs matching exact JavaScript logic"""
    
    @staticmethod
    def generate_fingerprint() -> str:
        """
        Generate fingerprint ID using the exact JavaScript logic:
        'fp_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now()
        """
        # Generate random string (equivalent to Math.random().toString(36).substr(2, 9))
        random_part = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=9))
        
        # Get current timestamp (equivalent to Date.now())
        timestamp = int(time.time() * 1000)
        
        # Combine: fp_ + random_part + _ + timestamp
        fingerprint = f"fp_{random_part}_{timestamp}"
        
        return fingerprint

class CapMonsterCloudSolver:
    """Handles CapMonster Cloud API integration for Turnstile solving"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.capsolver.com"
        
    def solve_turnstile(self, website_url: str, website_key: str) -> Optional[str]:
        """
        Solve Turnstile captcha using CapMonster Cloud
        
        Args:
            website_url: The website URL where the captcha appears
            website_key: The Turnstile site key
            
        Returns:
            Solved token if successful, None if failed
        """
        print(f"{Fore.CYAN}🔄 Creating Turnstile solving task...")
        
        # Create task
        task_id = self._create_task(website_url, website_key)
        if not task_id:
            return None
            
        # Poll for result
        print(f"{Fore.YELLOW}⏳ Polling for solution...")
        return self._get_task_result(task_id)
    
    def _create_task(self, website_url: str, website_key: str) -> Optional[str]:
        """Create a Turnstile solving task"""
        url = f"{self.base_url}/createTask"
        
        payload = {
            "clientKey": self.api_key,
            "task": {
                "type": "AntiTurnstileTaskProxyLess",
                "websiteURL": website_url,
                "websiteKey": website_key
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("errorId") != 0:
                error_desc = data.get('errorDescription', 'Unknown error')
                print(f"{Fore.RED}❌ CapMonster Cloud Error: {error_desc}")
                return None
                
            task_id = data.get("taskId")
            if task_id:
                print(f"{Fore.GREEN}✅ Task created successfully! Task ID: {task_id}")
                return task_id
            else:
                print(f"{Fore.RED}❌ No task ID returned")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}❌ Request failed: {e}")
            return None
        except json.JSONDecodeError:
            print(f"{Fore.RED}❌ Invalid JSON response")
            return None
    
    def _get_task_result(self, task_id: str) -> Optional[str]:
        """Poll for task result"""
        url = f"{self.base_url}/getTaskResult"
        
        max_polls = 30  # 30 seconds max
        poll_interval = 2  # 2 seconds
        
        for poll_count in range(max_polls):
            print(f"{Fore.YELLOW}  Poll {poll_count + 1}/{max_polls}...")
            time.sleep(poll_interval)
            
            payload = {"clientKey": self.api_key, "taskId": task_id}
            
            try:
                response = requests.post(url, json=payload, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("errorId") != 0:
                    error_desc = data.get('errorDescription', 'Unknown error')
                    print(f"{Fore.RED}❌ CapMonster Cloud Error: {error_desc}")
                    return None
                
                status = data.get("status")
                
                if status == "ready":
                    solution = data.get("solution", {}).get("token")
                    if solution:
                        print(f"{Fore.GREEN}✅ Turnstile solved successfully!")
                        print(f"{Fore.GREEN}Token: {solution[:50]}...")
                        return solution
                    else:
                        print(f"{Fore.RED}❌ Ready status but no token in solution")
                        return None
                
                elif status == "failed":
                    error_desc = data.get('errorDescription', 'Unknown error')
                    print(f"{Fore.RED}❌ Task failed: {error_desc}")
                    return None
                
                print(f"{Fore.YELLOW}  Status: {status}")
                
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}❌ Request failed: {e}")
                return None
            except json.JSONDecodeError:
                print(f"{Fore.RED}❌ Invalid JSON response")
                return None
        
        print(f"{Fore.RED}❌ Task timed out after {max_polls} polls")
        return None

class GameOnSimplified:
    """Simplified GameOn integration focusing on fingerprint and captcha solving"""
    
    def __init__(self):
        self.fp_generator = FingerprintGenerator()
        self.capsolver = CapMonsterCloudSolver(CAPMONSTER_CLOUD_API_KEY)
        
    def generate_session_data(self) -> Dict[str, str]:
        """
        Generate session data including fingerprint and solved Turnstile token
        
        Returns:
            Dictionary containing fingerprint and turnstile token
        """
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🎮 GameOn Simplified Session Generator")
        print(f"{Fore.CYAN}{'='*60}")
        
        # Step 1: Generate fingerprint
        print(f"\n{Fore.BLUE}📋 Step 1: Generating fingerprint...")
        fingerprint = self.fp_generator.generate_fingerprint()
        print(f"{Fore.GREEN}✅ Fingerprint generated: {fingerprint}")
        
        # Step 2: Solve Turnstile captcha
        print(f"\n{Fore.BLUE}🔐 Step 2: Solving Turnstile captcha...")
        turnstile_token = self.capsolver.solve_turnstile(GAMEON_WEBSITE_URL, GAMEON_WEBSITE_KEY)
        
        if not turnstile_token:
            print(f"{Fore.RED}❌ Failed to solve Turnstile captcha")
            return {}
        
        # Step 3: Prepare session data
        session_data = {
            "fingerprint": fingerprint,
            "turnstile_token": turnstile_token,
            "website_url": GAMEON_WEBSITE_URL,
            "website_key": GAMEON_WEBSITE_KEY,
            "generated_at": int(time.time() * 1000)
        }
        
        print(f"\n{Fore.GREEN}✅ Session data generated successfully!")
        print(f"{Fore.GREEN}📊 Session Summary:")
        print(f"   • Fingerprint: {fingerprint}")
        print(f"   • Turnstile Token: {turnstile_token[:50]}...")
        print(f"   • Website: {GAMEON_WEBSITE_URL}")
        print(f"   • Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return session_data
    
    def test_api_connection(self) -> bool:
        """Test CapMonster Cloud API connection"""
        print(f"{Fore.CYAN}🔍 Testing CapMonster Cloud API connection...")
        
        # Try to create a task (this will fail if API key is invalid)
        task_id = self.capsolver._create_task(GAMEON_WEBSITE_URL, GAMEON_WEBSITE_KEY)
        
        if task_id:
            print(f"{Fore.GREEN}✅ API connection successful!")
            return True
        else:
            print(f"{Fore.RED}❌ API connection failed!")
            return False

def main():
    """Main function"""
    print(f"{Fore.MAGENTA}🚀 GameOn Simplified Fingerprint & CapMonster Cloud Solver")
    print(f"{Fore.MAGENTA}{'='*60}")
    
    # Check if API key is configured
    if CAPMONSTER_CLOUD_API_KEY == "YOUR_CAPMONSTER_CLOUD_API_KEY_HERE":
        print(f"{Fore.RED}❌ Please configure your CapMonster Cloud API key in the script!")
        print(f"{Fore.YELLOW}💡 Edit the CAPMONSTER_CLOUD_API_KEY variable at the top of this file.")
        return
    
    # Initialize GameOn client
    gameon = GameOnSimplified()
    
    # Test API connection first
    if not gameon.test_api_connection():
        print(f"{Fore.RED}❌ Cannot proceed without valid API connection")
        return
    
    print(f"\n{Fore.CYAN}🎯 Generating session data...")
    
    # Generate session data
    session_data = gameon.generate_session_data()
    
    if session_data:
        print(f"\n{Fore.GREEN}🎉 Success! Session data ready for use.")
        print(f"{Fore.YELLOW}💡 This data can be used for further GameOn API calls.")
        
        # Save session data to file for reference
        with open("session_data.json", "w") as f:
            json.dump(session_data, f, indent=2)
        print(f"{Fore.BLUE}💾 Session data saved to session_data.json")
    else:
        print(f"{Fore.RED}❌ Failed to generate session data")

if __name__ == "__main__":
    main()
