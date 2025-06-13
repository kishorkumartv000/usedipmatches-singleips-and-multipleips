import argparse
from typing import List, Dict, Tuple
import os

# Configuration - Directory structure for organized IP storage
BASE_DIR = "ip_data"
OPERATIONS = ["creating", "redeeming", "farming"]
COUNTRIES = ["India", "US", "Brazil"]

def setup_directories():
    """Create the directory structure if it doesn't exist"""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    
    for operation in OPERATIONS:
        op_path = os.path.join(BASE_DIR, operation)
        if not os.path.exists(op_path):
            os.makedirs(op_path)
        
        for country in COUNTRIES:
            country_file = os.path.join(op_path, f"{country}.txt")
            if not os.path.exists(country_file):
                open(country_file, 'a').close()

def load_ips_from_file(file_path: str) -> List[str]:
    """Load IPs from a file, one per line, ignoring empty lines."""
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def check_ip_operations(target_ip: str) -> Dict[str, List[str]]:
    """Check IP across all operations and countries."""
    results = {operation: [] for operation in OPERATIONS}
    
    for operation in OPERATIONS:
        for country in COUNTRIES:
            file_path = os.path.join(BASE_DIR, operation, f"{country}.txt")
            ip_list = load_ips_from_file(file_path)
            
            if target_ip in ip_list:
                results[operation].append(country)
    
    return results

def format_results(target_ip: str, results: Dict[str, List[str]]) -> str:
    """Format results in the requested output style."""
    output_lines = [f"Report for IP: {target_ip}\n" + "-"*40]
    
    for operation, countries in results.items():
        if countries:
            countries_str = ", ".join(countries)
            output_lines.append(f"This IP was used in {operation} accounts in: {countries_str}")
        else:
            output_lines.append(f"This IP was not used in {operation} accounts")
    
    return "\n".join(output_lines)

def main():
    # Setup directory structure first
    setup_directories()
    
    parser = argparse.ArgumentParser(description="Check IP against operations and countries")
    parser.add_argument("--ip", required=True, help="IP address to check")
    args = parser.parse_args()

    try:
        results = check_ip_operations(args.ip)
        print(format_results(args.ip, results))
        
        print("\nNote: To add IPs to the database, place them in the appropriate")
        print(f"files under the {BASE_DIR} directory structure (e.g., {BASE_DIR}/creating/India.txt)")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
