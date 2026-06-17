# OSS Provisioning Playground

A lightweight, role-based microservice architecture designed to simulate the end-to-end telecommunication provisioning flow (**BSS → OSS → EMS**).\
This project demonstrates how synchronous HTTP client requests are translated into TL1 network commands and transmitted via TCP sockets.

---

<br/><br/>
## 🏗️ System Architecture & Directory Structure

The project is structured as a monorepo, separating the core orchestration logic from the simulator components to decouple responsibilities.

```text
oss-playground/
│
├── oss-core/                 # Main Operations Support System (OSS) Core Engine
│   ├── app/
│   │   ├── controllers/      # Inbound/Outbound Adapters
│   │   │   ├── bss_controller.py # FastAPI Router handling incoming HTTP POST requests from BSS
│   │   │   └── ems_controller.py # Manages outbound TCP socket connections to EMS
│   │   │
│   │   ├── services/         # Core Business Logic
│   │   │   └── oss_orchestrator.py # Evaluates metadata, determines EMS target, and drives the workflow
│   │   │
│   │   ├── translators/      # Data Structure Translators (Encoders/Decoders)
│   │   │   ├── tl1_encoder.py    # Encodes JSON payload to vendor-specific TL1 commands
│   │   │   └── tl1_decoder.py    # Parses raw TL1 completion lines into structured JSON
│   │   │
│   │   ├── models/           # Pydantic Schemas
│   │   │   └── schemas.py    # Request/Response data models
│   │   │
│   │   └── main.py           # Application entry point and FastAPI server initialization
│   │
│   ├── tests/                # Automated Test Suites (Pytest)
│   │   ├── unit/             # Unit Tests (isolated logic tests, ...)
│   │   └── integration/      # Integration Tests (API flow tests with EMS mocking, ...)
│   │
│   └── requirements.txt      # Core backend dependencies (FastAPI, Uvicorn, Pydantic, requests...)
│
├── simulators/               # Environment Simulators (Mock Systems)
│   ├── data/                 # JSON payload files for BSS testing
│   │   ├── case1_nokia.json
│   │   ├── case2_huawei.json
│   │   └── case3_invalid_serialNum.json
│   │
│   ├── mock_bss.py           # Mock BSS Client (Loads JSON files and sends HTTP requests)
│   ├── mock_ems.py           # Mock EMS Server (Listens on TCP socket and returns COMPLD)
│   └── requirements.txt      # Simulator dependencies

```


<br/><br/><br/><br/>
## 🔄 Provisioning Data Flow


### Reception (```oss-core/app/receivers/http_receiver.py```):

Receives and validates the JSON payload against the Pydantic data schemas.

### Orchestration (```services/oss_orchestrator.py```):

Acts as the central controller. It evaluates the equipment metadata, determines the appropriate EMS vendor, and delegates tasks to the translation and transmission layers.

### Encoding (```translators/tl1_encoder.py```):

Parses the validated JSON and constructs a corresponding raw TL1 telecommunication command string (e.g., ENT-ONT).

### Transmission (```controllers/ems_controller.py```):

Opens a raw TCP socket connection to mock_ems.py and streams the encoded TL1 payload.

### Decoding Response & Egress(```translators/tl1_decoder.py```):

mock_ems.py returns a raw TL1 text response. The decoder parses this text into a unified JSON status map, which the orchestrator packages into a final receipt and sends back to the BSS.




<br/><br/><br/><br/>
## ⚙️ Dependencies
### 1. OSS Core Engine (oss-core/requirements.txt)
The core service utilizes the following ecosystem components:

* fastapi (v0.104.1): Modern web framework for building APIs.

* uvicorn (v0.24.0.post1): High-performance ASGI server to run FastAPI.

* pydantic (v2.5.2): Strict data validation using Python type hints.

* pytest (v7.4.3): Framework for writing and running automated test suites.

* httpx (v0.25.2): Async HTTP client required by FastAPI TestClient for integration tests.

### 2. Simulators Cluster (simulators/requirements.txt)
The test simulators run on a minimal dependency environment:

* mock_ems.py: Relies solely on Python's built-in socket module (no external package dependencies).

* mock_bss.py: Requires requests (v2.31.0) to execute standard synchronous HTTP network calls.


<br/><br/><br/><br/>
## 🚀 Getting Started
### Prerequisites

Python 3.10 or higher
<br/>

### Quick Start with Shell Script (Recommended)
You can automatically spin up the entire cluster (install dependencies, launch mock systems, run tests, and perform a clean shutdown) using the automated script:

  ```Bash
  # 1. Grant execute permission to the shell script
  chmod +x run.sh


  # 2. Execute the single-click cluster runtime
  ./run.sh
  ```

<br/>

### Manual Orchestration (Step-by-Step)
If you prefer to run and trace each component manually, open three separate terminal windows and execute them in the following chronological order:

* **Step 0: Install dependencies for each environment (First time only)**
  ```bash
  # Install Simulator dependencies
  pip install -r simulators/requirements.txt

  # Install OSS Core dependencies (fastapi, uvicorn, etc.)
  pip install -r oss-core/requirements.txt
  ```

* **Step 1: Spin up the simulated EMS**

   ```Bash
  # No external packages needed (uses built-in socket)
  python simulators/mock_ems.py
  ```

* **Step 2: Launch the main OSS Core Server**

  ```Bash
  cd oss-core
  uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
  ```

* **Step 3: Trigger the Provisioning Process from BSS Client**

  ```Bash
  python simulators/mock_bss.py
  ```

<br/><br/><br/><br/>
## 🧪 Running Tests

The project includes a comprehensive test suite using `pytest`. The tests are divided into Unit Tests (fast, logic-focused) and Integration Tests (API flow, mocked EMS).

To run the tests, navigate to the `oss-core` directory and execute:
```Bash
cd oss-core
```

# 1. Run ALL tests
```Bash
pytest -v
```

# 2. Run ONLY Unit Tests (Extremely fast, no mocking needed)
```Bash
pytest tests/unit/ -v
```

# 3. Run ONLY Integration Tests (Tests the full API flow)
```Bash
pytest tests/integration/ -v
```