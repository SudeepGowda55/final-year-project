import json
   import requests
   import os
   import datetime

   MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
   MISTRAL_API_KEY = "" 
   MISTRAL_MODEL = "mistral-large-latest"

   SECURITY_PROMPT = """
   Analyze the provided AWS CloudTrail logs and generate a comprehensive security summary...
   """

   def query_mistral(log_entry):
       payload = {
           "model": MISTRAL_MODEL,
           "messages": [
               {
                   "role": "user",
                   "content": SECURITY_PROMPT + json.dumps(log_entry, indent=2)
               }
           ]
       }

       headers = {
           "Authorization": f"Bearer {MISTRAL_API_KEY}",
           "Content-Type": "application/json",
           "Accept": "application/json"
       }

       try:
           response = requests.post(MISTRAL_URL, json=payload, headers=headers)
           response_json = response.json()
           return response_json.get("choices", [{}])[0].get("message", {}).get("content", "No recommendation generated.")
       except Exception as e:
           print("Error querying Mistral:", e)
           return "AI analysis failed."

   def process_sample_log():
       SAMPLE_LOG_FILE = "/opt/ollama/cloudtrail/sample.json"
       SAVE_DIR = "/opt/ollama/cloudtrail/"

       os.makedirs(SAVE_DIR, exist_ok=True)

       if not os.path.exists(SAMPLE_LOG_FILE):
           print(f"Sample log file not found: {SAMPLE_LOG_FILE}")
           return

       today_date = datetime.datetime.now().strftime("%Y-%m-%d")
       save_path = os.path.join(SAVE_DIR, f"cloudtrail_enriched_{today_date}.json")

       with open(SAMPLE_LOG_FILE, "r") as infile, open(save_path, "w") as outfile:
           try:
               log_entry = json.load(infile)
               ai_recommendation = query_mistral(log_entry)
               log_entry["ai.agent.recommendations"] = ai_recommendation
               outfile.write(json.dumps(log_entry, indent=2) + "\n")
           except json.JSONDecodeError:
               print("Invalid JSON format in the sample log file.")

       print(f"Sample log enriched and saved to {save_path}")

   if __name__ == "__main__":
       process_sample_log()
