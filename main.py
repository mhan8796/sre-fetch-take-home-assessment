import yaml
import requests
import time
import sys
from urllib.parse import urlparse
from collections import defaultdict

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')  # Default to GET if not specified
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')

    # Ensure body is parsed as JSON if it's a string
    json_body = None
    if body:
        try:
            import json
            json_body = json.loads(body)
        except json.JSONDecodeError:
            json_body = None

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=json_body, timeout=0.5)
        elapsed = (time.time() - start_time) * 1000  # ms

        if 200 <= response.status_code < 300 and elapsed <= 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            parsed_url = urlparse(endpoint['url'])
            domain = parsed_url.hostname  # Ignores port, as required
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability (drop decimals as instructed)
        for domain, stats in domain_stats.items():
            availability = int((100 * stats["up"]) / stats["total"])  # Drop decimals
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")