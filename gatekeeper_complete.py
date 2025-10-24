#!/usr/bin/env python3
"""
GameOn Gatekeeper Token Generator with CapMonster Cloud Integration
================================================================

A complete Python solution for bypassing GameOn's Turnstile captcha protection 
using CapMonster Cloud automated captcha solving service.

This script demonstrates:
1. Fingerprint generation (matching JavaScript logic)
2. CapMonster Cloud Turnstile captcha solving
3. Complete GameOn gatekeeper token generation
4. Example product carting workflow

Usage:
    python gameon_complete.py
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
GAMEON_GATEKEEPER_URL = "https://gatekeeper.gameon.games/api/gatekeeper-token"
GAMEON_CART_URL = "https://www.gameon.games/cart/add.js"

# Example Product Configuration
EXAMPLE_PRODUCT_ID = "55041037336956"  # Example variant ID
EXAMPLE_QUANTITY = 1

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

class GameOnClient:
    """Complete GameOn integration with fingerprint, captcha solving, and carting"""
    
    def __init__(self):
        self.fp_generator = FingerprintGenerator()
        self.capsolver = CapMonsterCloudSolver(CAPMONSTER_CLOUD_API_KEY)
        self.session = tls_client.Session(
            client_identifier="chrome_120",
            random_tls_extension_order=True
        )
        
        # Set realistic headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://www.gameon.games',
            'Referer': 'https://www.gameon.games/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        })
        
    def generate_gatekeeper_token(self) -> Optional[Dict]:
        """
        Generate complete gatekeeper token with fingerprint and Turnstile solving
        
        Returns:
            Dictionary containing gatekeeper token and related data
        """
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🎮 GameOn Gatekeeper Token Generation")
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
            return None
        
        # Step 3: Generate gatekeeper token
        print(f"\n{Fore.BLUE}🎫 Step 3: Generating gatekeeper token...")
        
        gatekeeper_payload = {
            "shopDomain": "store-gameon-games.myshopify.com",
            "ttlMinutes": 10,
            "turnstileToken": turnstile_token,
            "fingerprint": fingerprint,
            "variantId": EXAMPLE_PRODUCT_ID
        }
        
        try:
            response = self.session.post(
                GAMEON_GATEKEEPER_URL,
                json=gatekeeper_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    gatekeeper_token = data.get("gatekeeperToken")
                    cart_token = data.get("cartToken")
                    
                    print(f"{Fore.GREEN}✅ Gatekeeper token generated successfully!")
                    print(f"{Fore.GREEN}Token: {gatekeeper_token[:50]}...")
                    print(f"{Fore.GREEN}Cart Token: {cart_token}")
                    
                    return {
                        "success": True,
                        "gatekeeper_token": gatekeeper_token,
                        "cart_token": cart_token,
                        "fingerprint": fingerprint,
                        "turnstile_token": turnstile_token,
                        "ttl_minutes": data.get("ttlMinutes"),
                        "expires_at": data.get("expiresAt"),
                        "release_id": data.get("releaseId")
                    }
                else:
                    print(f"{Fore.RED}❌ Gatekeeper token generation failed")
                    print(f"{Fore.RED}Response: {data}")
                    return None
            else:
                print(f"{Fore.RED}❌ HTTP Error: {response.status_code}")
                print(f"{Fore.RED}Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}❌ Request failed: {e}")
            return None
    
    def add_to_cart(self, gatekeeper_data: Dict) -> bool:
        """
        Add example product to cart using gatekeeper token
        
        Args:
            gatekeeper_data: Data from gatekeeper token generation
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n{Fore.BLUE}🛒 Step 4: Adding product to cart...")
        
        cart_payload = {
            "id": EXAMPLE_PRODUCT_ID,
            "quantity": EXAMPLE_QUANTITY,
            "properties": {},
            "gatekeeper_token": gatekeeper_data["gatekeeper_token"]
        }
        
        try:
            response = self.session.post(
                GAMEON_CART_URL,
                json=cart_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "items" in data:
                    print(f"{Fore.GREEN}✅ Product added to cart successfully!")
                    print(f"{Fore.GREEN}Cart items: {len(data['items'])}")
                    print(f"{Fore.GREEN}Total: {data.get('total_price', 'N/A')}")
                    return True
                else:
                    print(f"{Fore.RED}❌ Cart addition failed")
                    print(f"{Fore.RED}Response: {data}")
                    return False
            else:
                print(f"{Fore.RED}❌ HTTP Error: {response.status_code}")
                print(f"{Fore.RED}Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Cart request failed: {e}")
            return False
    
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
    """Main function demonstrating complete GameOn workflow"""
    print(f"{Fore.MAGENTA}🚀 GameOn Complete Workflow with CapMonster Cloud")
    print(f"{Fore.MAGENTA}{'='*60}")
    
    # Check if API key is configured
    if CAPMONSTER_CLOUD_API_KEY == "YOUR_CAPMONSTER_CLOUD_API_KEY_HERE":
        print(f"{Fore.RED}❌ Please configure your CapMonster Cloud API key!")
        print(f"{Fore.YELLOW}💡 Edit the CAPMONSTER_CLOUD_API_KEY variable at the top of this file.")
        return
    
    # Initialize GameOn client
    gameon = GameOnClient()
    
    # Test API connection first
    if not gameon.test_api_connection():
        print(f"{Fore.RED}❌ Cannot proceed without valid API connection")
        return
    
    print(f"\n{Fore.CYAN}🎯 Starting complete GameOn workflow...")
    
    # Generate gatekeeper token
    gatekeeper_data = gameon.generate_gatekeeper_token()
    
    if gatekeeper_data:
        print(f"\n{Fore.GREEN}🎉 Gatekeeper token generated successfully!")
        
        # Add product to cart
        cart_success = gameon.add_to_cart(gatekeeper_data)
        
        if cart_success:
            print(f"\n{Fore.GREEN}🎉 Complete workflow successful!")
            print(f"{Fore.YELLOW}💡 This demonstrates the full GameOn integration process.")
            
            # Save complete session data
            session_data = {
                "gatekeeper_data": gatekeeper_data,
                "cart_success": cart_success,
                "workflow_completed": True,
                "timestamp": int(time.time() * 1000)
            }
            
            with open("complete_session_data.json", "w") as f:
                json.dump(session_data, f, indent=2)
            print(f"{Fore.BLUE}💾 Complete session data saved to complete_session_data.json")
        else:
            print(f"{Fore.RED}❌ Cart addition failed, but gatekeeper token was generated")
    else:
        print(f"{Fore.RED}❌ Failed to generate gatekeeper token")

if __name__ == "__main__":
    main()
