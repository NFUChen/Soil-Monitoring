import socket
import os

# Load environment variables from .env file
try:
    # Try to import dotenv
    import dotenv
except ImportError:
    # If dotenv is not installed, install it using pip
    os.system('pip install python-dotenv')
    import dotenv


def update_local_ip():
    dotenv.load_dotenv()

    # Get internal network IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print(f"setting ip: {ip}")
    s.close()

    # Update "LOCAL_IP" environment variable
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    with open(dotenv_path, 'r') as file:
        lines = file.readlines()
    
    with open(dotenv_path, 'w') as file:
        for line in lines:
            if line.startswith('LOCAL_IP='):
                # Replace the existing value
                line = f'LOCAL_IP={ip}\n'
            file.write(line)

    # Reload environment variables from the updated .env file
    dotenv.load_dotenv()

if __name__ == "__main__":
    update_local_ip()
