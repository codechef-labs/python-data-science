import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import http.server
import socketserver
import webbrowser
import traceback
import matplotlib.pyplot as plt

def execute_plotting_code(user_code):
    """Execute user's plotting code and return the plot image if successful"""
    try:
        # Create a namespace for execution
        namespace = {}
        
        # Execute user code in the namespace
        exec(user_code, namespace)
        
        # Save the plot to buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        
        # Encode the image
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')
        
        plt.close('all')
        
        return {
            'success': True,
            'image': graphic
        }
    except Exception:
        plt.close('all')
        # Print the traceback directly to terminal
        print("\nError in user code:")
        traceback.print_exc()
        return {
            'success': False
        }

user_code = ""
with open('main.py', 'r') as file:
    user_code = file.read()

# Execute the code and get the result
result = execute_plotting_code(user_code)

if result['success']:
    # Create HTML file with the plot
    with open('index.html', 'w') as file:
        file.write(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Plot Result</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    background-color: #f0f0f0;
                }}
                img {{
                    max-width: 95%;
                    height: auto;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 5px;
                    background-color: white;
                }}
            </style>
        </head>
        <body>
            <img src="data:image/png;base64,{result['image']}" />
        </body>
        </html>
        ''')
    
    # Set up and start the HTTP server
    PORT = 3000
    Handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\nServer started at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server...")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server...")
            httpd.shutdown()
            httpd.server_close()
            print("Server stopped.")
else:
    # Just exit if there was an error (error message already printed)
    exit(1)
