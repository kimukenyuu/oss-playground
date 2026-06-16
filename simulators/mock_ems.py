import socket
import logging
from datetime import datetime

# Setup clean logging format for the simulator
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("MockEMS")

def run_mock_ems(host: str = "127.0.0.1", port: int = 9999):
    """
    Simulates a telecom EMS (Element Management System) server.
    Listens on a raw TCP socket, receives TL1 commands from the OSS,
    and returns a standard valid TL1 completion response.
    """
    # Create a TCP/IP socket using IPv4
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow immediate reuse of the port after shutdown
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to the host and port, then start listening
        s.bind((host, port))
        s.listen()
        logger.info(f"🏢 [Mock EMS] is waiting at {host}:{port}...")
        
        while True:
            # Block and wait for an inbound connection from the OSS Core (tcp_sender)
            conn, addr = s.accept()
            
            with conn:
                logger.info(f"✅ [Mock EMS] successful connection from OSS (Client Address: {addr})")
                
                while True:
                    # Receive raw bytes data from the stream (up to 4096 bytes)
                    data = conn.recv(4096)
                    if not data:
                        # Break the inner loop if the connection is closed by the client
                        logger.info("ℹ️ [Mock EMS] OSS Core has closed the connection.")
                        break
                    
                    # Decode the incoming byte payload into a TL1 string
                    raw_cmd = data.decode('utf-8').strip()
                    logger.info(f"📥 [Mock EMS] received TL1 command:\n{raw_cmd}")

                    try:
                        if "::" in raw_cmd:
                            aid_block = raw_cmd.split("::")[1]
                            remoteID = aid_block.split(":")[0]
                    except Exception:
                        logger.warning("⚠️ [Mock EMS] Failed to parse RemoteID from TL1 command. Defaulting to UNKNOWN-OLT.")
                        remoteID = "UNKNOWN-OLT"
                        pass
                    
                    # Construct a standard mock TL1 response indicating successful execution (COMPLD)
                    # Real telecom equipment uses this exact trailing semicolon (;) format.
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    mock_tl1_response = (
                        f" RID: {remoteID} Time: {current_time}\n"
                        "M  001 COMPLD\n"
                        "/* SUCCESS: OPERATION COMPLETED SUCCESSFULLY */\n"
                        ";"
                    )
                    
                    # Send the response back to the OSS Core
                    logger.info("📤 [Mock EMS] COMPLD response being sent...")
                    conn.sendall(mock_tl1_response.encode('utf-8'))

if __name__ == "__main__":
    # Run the server on localhost port 9999 by default
    run_mock_ems()