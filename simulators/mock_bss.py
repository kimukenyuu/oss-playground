import os
import requests
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_test_cases() -> dict:
    test_cases = {}
    if not os.path.exists(DATA_DIR):
        print(f"❌ ERROR: Data directory not found -> {DATA_DIR}")
        return test_cases

    json_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.json')])
    if not json_files:
        print(f"⚠️ WARNING: No .json files found in {DATA_DIR}")
        return test_cases
        
    for idx, filename in enumerate(json_files, start=1):
        file_path = os.path.join(DATA_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                test_cases[str(idx)] = json.load(f)
            except json.JSONDecodeError:
                print(f"❌ ERROR: Invalid JSON format in {filename}")
                
    return test_cases

def run_bss_client():
    print("=========================================")
    print("🧑‍💼 [Mock BSS] File-Driven Provisioning Simulator")
    print("=========================================")
    
    test_cases = load_test_cases()
    if not test_cases:
        return
        
    # 🔄 Added a continuous loop for multiple requests!
    while True:
        print("\n-----------------------------------------")
        print("📋 [Available Test Cases]")
        for key, case in test_cases.items():
            desc = case.get('desc', 'No Description Provided')
            print(f" [{key}] {desc}")
        print(" [q] Quit Simulator")
        
        choice = input("\nSelect a test case to execute (or 'q' to quit): ").strip().lower()
        
        # Exit condition
        if choice in ['q', 'quit', 'exit']:
            print("\n👋 Exiting Mock BSS Simulator. Goodbye!")
            break
            
        if choice not in test_cases:
            print("❌ Invalid selection. Please try again.")
            continue
            
        selected_case = test_cases[choice]
        remote_id = selected_case.get("remote_id", "")
        circuit_id = selected_case.get("circuit_id", "")
        payload = selected_case.get("payload", {})

        url = f"http://localhost:8000/api/v1/olts/{remote_id}/onus/{circuit_id}"
        headers = {
            "x-request-id": f"BSS-REQ-20260616-{choice.zfill(3)}",
            "Content-Type": "application/json"
        }
        
        print(f"\n🚀 [Mock BSS] Transmitting Request: [{selected_case.get('desc', '')}]...")
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            print(f"✅ [Mock BSS] Received Response from OSS Core! (HTTP Status: {response.status_code})")
            print("🧾 [Unified Receipt]:")
            
            try:
                print(json.dumps(response.json(), indent=4, ensure_ascii=False))
            except json.decoder.JSONDecodeError:
                print(response.text)
                
        except requests.exceptions.ConnectionError:
            print("\n❌ [ERROR] Connection failed. Is the OSS Core (uvicorn) currently running?")

if __name__ == "__main__":
    run_bss_client()