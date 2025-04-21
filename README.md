# sre-fetch-take-home-assessment

# Endpoint Availability Monitor

This script monitors the availability of HTTP endpoints defined in a YAML file. It logs cumulative availability percentages by domain every 15 seconds.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```



2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   
3. Run the script with a YAML config file:
   ```
   python main.py sample.yaml
   ```

## YAML Config Format
   ```
   - name: sample endpoint
  url: https://example.com
  method: POST
  headers:
    content-type: application/json
  body: '{"key":"value"}'
   ```


## Availability Criteria

- HTTP status code between 200 and 299

- Response time ≤ 500ms

## Behavior

- Evaluates endpoints every 15 seconds

- Calculates cumulative availability per domain (ignores ports)

- Prints whole number availability percentages (drops decimals)
