import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import http.server
import socketserver

def execute_plotting_code(user_code):
    try:
        # Create a namespace for execution
        namespace = {}
        
        # Execute user code in the namespace
        exec(user_code, namespace)
        
        # Get the figure from the namespace and save it
        import matplotlib.pyplot as plt
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        plt.close('all')
        
        # Encode the image
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')
        
        return {
            'success': True,
            'image': graphic
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
    finally:
        plt.close('all')


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
            <title>Plot View</title>
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
    print(f"Error generating plot: {result['error']}")
