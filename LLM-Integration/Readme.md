1. **Create the Required Directory**:
   Ensure the directory for saving enriched logs exists:
   ```bash
   sudo mkdir -p /opt/ollama/cloudtrail/
   ```

2. **Set Permissions**:
   Set the appropriate permissions for the directory:
   ```bash
   sudo chmod 777 /opt/ollama/cloudtrail/
3. **Run the Script**:
   Execute the script to process the sample log and generate the enriched log file:
   ```bash
   python3 /opt/ollama/model.py
   ```
4. **Check Output**:
   The enriched log file will be saved in the `/opt/ollama/cloudtrail/` directory with the name format `cloudtrail_enriched_YYYY-MM-DD.json`.
