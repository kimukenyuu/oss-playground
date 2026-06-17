import socket
import logging
import os
from dotenv import load_dotenv

# Setup logger for the sender layer
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load environment variables from .env file (if exists)
load_dotenv()

class EmsController:
    """
    Handles outbound TCP socket communication to the EMS server.
    Receives TL1 commands, transmits them over the network, and returns the raw string response.
    """
    def __init__(self, host: str = None, port: int = None):
        # In a real environment, this IP/Port would be dynamically fetched from the DB (e.g., t_oss_addr_mst).
        # For this playground, it defaults to the local mock EMS simulator
        # if environment variables are not set, 127.0.0.1 and 9999 will be used.
        self.host = host or os.getenv("TARGET_EMS_HOST", "127.0.0.1")
        self.port = port or int(os.getenv("TARGET_EMS_PORT", 9999))

    def send_tl1_commands(self, commands: list[str]) -> str:
        """
        Establishes a socket connection and sends a sequence of TL1 commands.
        Returns the raw response from the last executed command.
        """
        raw_response = ""
        
        try:
            logger.info(f"Establishing TCP connection to EMS at {self.host}:{self.port}...")
            
            # 1. Create a TCP/IP socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5.0) # 5 seconds timeout
                s.connect((self.host, self.port))
                logger.info("Connection established successfully.")
                
                # 2. Iterate and send commands sequentially
                for cmd in commands:
                    logger.info(f"Transmitting TL1 Payload: {cmd}")
                    
                    # Encode string to bytes before sending over TCP
                    s.sendall(cmd.encode('utf-8'))
                    
                    # 3. Receive the response from the EMS
                    data = s.recv(4096)
                    raw_response = data.decode('utf-8')
                    logger.info(f"Raw Response from EMS: {raw_response.strip()}")
                    
                    # Stop the sequence if the EMS denies a command
                    if "DENY" in raw_response.upper():
                        logger.error("Command execution denied by EMS. Halting sequence.")
                        break
                        
        except ConnectionRefusedError:
            logger.error("Connection refused. Make sure the mock_ems.py simulator is running.")
            raw_response = "DENY: CONNECTION REFUSED\n/* Is the mock EMS running? */\n;"
        except Exception as e:
            logger.error(f"Socket communication error: {e}")
            raw_response = f"DENY: SOCKET ERROR - {str(e)}\n;"
            
        return raw_response

# Singleton instance for the orchestrator to use
ems_controller = EmsController()