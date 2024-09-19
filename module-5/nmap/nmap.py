import argparse
import socket
import concurrent.futures
from typing import Tuple, Optional

def scan_port(ip: str, port: int) -> Tuple[int, str, Optional[str]]:
    """
    Attempts to connect to a given port on the specified IP address and checks if the port is open or closed.

    Args:
        ip (str): The IP address to scan.
        port (int): The port number to scan.

    Returns:
        Tuple[int, str, Optional[str]]: 
            - The port number.
            - A string indicating whether the port is "open" or "closed".
            - An optional string indicating the service name for the first 100 ports, otherwise None.
    """
    try:
        # Attempt to establish a socket connection to the port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                service_name = None
                # For ports 1-100, try to identify the service running on the port
                if port <= 100:
                    try:
                        service_name = socket.getservbyport(port)
                    except OSError:
                        service_name = "Unknown service"
                return port, "open", service_name
            else:
                return port, "closed", None
    except Exception as e:
        return port, "error", str(e)

def resolve_target(target: str) -> str:
    """
    Resolves a domain name to an IP address. If the input is already an IP address, it returns the same.

    Args:
        target (str): The domain name or IP address to resolve.

    Returns:
        str: The resolved IP address.

    Raises:
        socket.gaierror: If the domain name cannot be resolved to an IP address.
    """
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"Error: Unable to resolve address {target}.")
        exit(1)

def port_scanner(target: str, port_range: str) -> None:
    """
    Scans the specified range of ports on a target IP or domain.

    Args:
        target (str): The target domain or IP address to scan.
        port_range (str): The range of ports to scan, specified as "min-max" or "-" for all ports.

    Returns:
        None
    """
    ip = resolve_target(target)
    print(f"Scanning target: {target} ({ip})")
    
    if port_range == '-':
        # If -p- is specified, scan all ports (1 to 65535)
        ports = range(1, 65536)
    else:
        try:
            min_port, max_port = map(int, port_range.split('-'))
            ports = range(min_port, max_port + 1)
        except ValueError:
            print("Error: Invalid port range.")
            exit(1)
    
    open_ports = []

    # Use threading for faster scanning
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port, status, service_name = future.result()
            if status == "open":
                if port <= 100 and service_name:
                    print(f"Port {port} is open (Service: {service_name})")
                else:
                    print(f"Port {port} is open")
                open_ports.append(port)
            elif status == "closed":
                print(f"Port {port} is closed")
            else:
                print(f"Error on port {port}: {service_name}")

if __name__ == "__main__":
    """
    Main entry point of the program. Parses command-line arguments and initiates the port scan.

    Args:
        - target (str): The domain or IP address to scan.
        - -p/--ports (str): The port range (e.g., "20-80") or "-" to scan all ports.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="A simple port scanner similar to nmap")
    parser.add_argument("target", help="IP address or domain name of the target")
    parser.add_argument("-p", "--ports", required=True, help="Port range (min-max) or - for all ports")
    
    args = parser.parse_args()
    
    port_scanner(args.target, args.ports)
