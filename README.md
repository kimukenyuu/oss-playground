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
├── .github/
│   └── workflows/
│       └── cicd_pipeline.yml # CI/CD automation pipeline workflow
│
├── oss-core/                 # Main Operations Support System (OSS) Core Engine
│   ├── app/
│   │   ├── decoders/         # Data Translators & Parsers
│   │   │   ├── __init__.py
│   │   │   └── tl1_translator.py # Encodes JSON to TL1 format / Decodes raw TL1 to JSON
│   │   │
│   │   ├── receivers/        # Inbound Adapters (Handles external ingress requests)
│   │   │   ├── __init__.py
│   │   │   └── http_receiver.py  # FastAPI Router handling HTTP PUT requests
│   │   │
│   │   ├── senders/          # Outbound Adapters (Handles egress network operations)
│   │   │   ├── __init__.py
│   │   │   └── tcp_sender.py     # Establishes TCP connections to transmit TL1 payloads
│   │   │
│   │   └── main.py           # Application entry point and server initialization
│   │
│   ├── tests/                # Automated integration and unit tests using pytest
│   └── requirements.txt      # Core backend dependencies (FastAPI, Uvicorn, Pydantic, pytest, httpx, ...)
│
├── simulators/               # Environment Simulators (Mock Systems)
│   ├── mock_bss.py           # Simulates BSS Server(Sends HTTP PUT requests to OSS Core)
│   ├── mock_ems.py           # Simulates EMS Server(Listens on raw TCP socket)
│   └── requirements.txt      # Simulator dependencies
│
└── run.sh                    # One-click automation shell script to run the entire cluster
```


<br/><br/><br/><br/>
## 🔄 Provisioning Data Flow


### Reception (```oss-core/app/receivers/http_receiver.py```):

Receives and validates the JSON payload against the Pydantic data schemas.

### Translation (```oss-core/app/decoders/tl1_translator.py```):

Parses the validated JSON and constructs a corresponding raw TL1 telecommunication command string (e.g., ADD-ONT).

### Transmission (```oss-core/app/senders/tcp_sender.py```):

Opens a raw TCP socket connection to mock_ems.py and streams the encoded TL1 payload.

### Response & Egress:

mock_ems.py processes the command, returning a raw TL1 text response (COMPLD / DENY). oss-core captures this raw string, transforms it back into a clean, unified JSON receipt, and returns it to mock_bss.py.




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
