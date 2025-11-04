"""
OAuth authentication for Gosset API
"""
import os
import time
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import requests


API_BASE_URL = os.environ.get("OAUTH_BASE_URL", "https://api.gosset.ai")
REDIRECT_URI = "http://localhost:8765/callback"


class CallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback"""
    auth_code = None
    
    def do_GET(self):
        # Parse query parameters
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        if 'code' in params:
            CallbackHandler.auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html><body>
                <h1>Authorization successful!</h1>
                <p>You can close this window and return to the terminal.</p>
                </body></html>
            """)
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error = params.get('error', ['Unknown error'])[0]
            self.wfile.write(f"<html><body><h1>Authorization failed: {error}</h1></body></html>".encode())
    
    def log_message(self, format, *args):
        pass  # Suppress logging


def get_oauth_token(base_url=None, quiet=False):
    """
    Get OAuth token through interactive browser flow
    
    Args:
        base_url: Optional custom API base URL
        quiet: If True, suppress informational output
        
    Returns:
        str: OAuth access token if successful, None otherwise
    """
    if base_url is None:
        base_url = API_BASE_URL
    
    if not quiet:
        print("=" * 70)
        print("Interactive OAuth Token Acquisition")
        print("=" * 70)
        print()
    
    # Step 1: Register a client
    if not quiet:
        print("Step 1: Registering OAuth client...")
    
    try:
        register_response = requests.post(
            f"{base_url}/oauth/register",
            json={"redirect_uris": [REDIRECT_URI]},
            headers={"Content-Type": "application/json"}
        )
        
        if register_response.status_code != 201:
            if not quiet:
                print(f"✗ Failed to register client: {register_response.text}")
            return None
        
        client_data = register_response.json()
        client_id = client_data["client_id"]
        client_secret = client_data["client_secret"]
        
        if not quiet:
            print(f"✓ Client registered: {client_id}")
    except Exception as e:
        if not quiet:
            print(f"✗ Error registering client: {e}")
        return None
    
    # Step 2: Start local server for callback
    if not quiet:
        print("\nStep 2: Starting local callback server...")
    
    server = HTTPServer(('localhost', 8765), CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    if not quiet:
        print(f"✓ Callback server running on {REDIRECT_URI}")
    
    # Step 3: Open browser for authorization
    if not quiet:
        print("\nStep 3: Opening browser for authorization...")
    
    # Build authorization URL
    auth_url = f"{base_url}/oauth/authorize"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": "read write",
        "state": "test123"
    }
    
    auth_url_with_params = f"{auth_url}?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    if not quiet:
        print(f"Authorization URL: {auth_url_with_params}")
        print("\nOpening browser... (if it doesn't open, copy the URL above)")
    
    webbrowser.open(auth_url_with_params)
    
    # Wait for callback
    if not quiet:
        print("\nWaiting for authorization...")
    
    timeout = 120  # 2 minutes
    start_time = time.time()
    
    while CallbackHandler.auth_code is None and (time.time() - start_time) < timeout:
        time.sleep(0.5)
    
    server.shutdown()
    
    if not CallbackHandler.auth_code:
        if not quiet:
            print("✗ Authorization timeout or failed")
        return None
    
    if not quiet:
        print(f"✓ Authorization code received")
    
    # Step 4: Exchange code for token
    if not quiet:
        print("\nStep 4: Exchanging code for access token...")
    
    try:
        token_response = requests.post(
            f"{base_url}/oauth/token",
            data={
                "grant_type": "authorization_code",
                "code": CallbackHandler.auth_code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": REDIRECT_URI
            }
        )
        
        if token_response.status_code != 200:
            if not quiet:
                print(f"✗ Failed to get token: {token_response.text}")
            return None
        
        token_data = token_response.json()
        access_token = token_data["access_token"]
        
        if not quiet:
            print("\n" + "=" * 70)
            print("SUCCESS! Your OAuth token:")
            print("=" * 70)
            print(f"\n{access_token}\n")
            print("To use this token, run:")
            print(f"export GOSSET_OAUTH_TOKEN='{access_token}'")
            print("\nOr add to your ~/.bashrc or ~/.zshrc")
            print("=" * 70)
        
        return access_token
        
    except Exception as e:
        if not quiet:
            print(f"✗ Error getting token: {e}")
        return None

