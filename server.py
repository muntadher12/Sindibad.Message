#!/usr/bin/env python3
import os
import http.server
import socketserver
from urllib.parse import urlparse
import re

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        
        # If requesting the main page, inject environment variables
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            try:
                # Read the HTML file
                with open('index.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Get environment variables
                api_key = os.environ.get('VITE_FIREBASE_API_KEY', '')
                project_id = os.environ.get('VITE_FIREBASE_PROJECT_ID', '')
                app_id = os.environ.get('VITE_FIREBASE_APP_ID', '')
                
                print(f"Environment variables:")
                print(f"  API Key: {'[SET]' if api_key else '[NOT SET]'}")
                print(f"  Project ID: {project_id if project_id else '[NOT SET]'}")
                print(f"  App ID: {'[SET]' if app_id else '[NOT SET]'}")
                
                # Replace the environment variables in the script
                env_script = f'''
        // Set up environment variables from server
        window.ENV = {{
            VITE_FIREBASE_API_KEY: '{api_key}',
            VITE_FIREBASE_PROJECT_ID: '{project_id}',
            VITE_FIREBASE_APP_ID: '{app_id}'
        }};
        
        console.log('Environment variables loaded from server:', {{
            hasApiKey: !!window.ENV.VITE_FIREBASE_API_KEY,
            hasProjectId: !!window.ENV.VITE_FIREBASE_PROJECT_ID,
            hasAppId: !!window.ENV.VITE_FIREBASE_APP_ID,
            projectId: window.ENV.VITE_FIREBASE_PROJECT_ID
        }});'''
                
                # Replace the placeholder environment script
                pattern = r'(<!-- Environment Variables Script -->.*?</script>)'
                replacement = f'''<!-- Environment Variables Script -->
    <script>{env_script}
    </script>'''
                
                html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(html_content.encode('utf-8'))))
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
                
            except Exception as e:
                print(f"Error serving index.html: {e}")
                # Fallback to default behavior
                super().do_GET()
        else:
            # For all other files, use default behavior
            super().do_GET()

def run_server(port=5000):
    handler = CustomHTTPRequestHandler
    
    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"Server running at http://0.0.0.0:{port}/")
        print("Environment variables status:")
        print(f"  VITE_FIREBASE_API_KEY: {'SET' if os.environ.get('VITE_FIREBASE_API_KEY') else 'NOT SET'}")
        print(f"  VITE_FIREBASE_PROJECT_ID: {os.environ.get('VITE_FIREBASE_PROJECT_ID', 'NOT SET')}")
        print(f"  VITE_FIREBASE_APP_ID: {'SET' if os.environ.get('VITE_FIREBASE_APP_ID') else 'NOT SET'}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()