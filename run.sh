#!/bin/bash

# =========================================================================
# OSS Provisioning Cluster One-Click Runner
# =========================================================================

echo "🚀 Starting OSS Provisioning Cluster..."

# [Cleanup Function for Graceful Shutdown]
# Prevents zombie processes when the BSS simulator is closed (via 'q' or Ctrl+C).
cleanup() {
    echo -e "\n🧹 Shutting down cluster... Safely terminating background servers (EMS, OSS)."
    # Kill background processes using the stored PIDs
    kill $EMS_PID $OSS_PID 2>/dev/null
    echo "👋 All systems successfully terminated. Goodbye!"
    exit
}
# Trap EXIT and interrupt signals to trigger the cleanup function
trap cleanup EXIT INT TERM


# 🏢 [1. Run Mock EMS in Background]
echo "🏢 [1/3] Starting Mock EMS Server in background..."
python simulators/mock_ems.py > ems.log 2>&1 &
EMS_PID=$!
echo "   ✅ Done (Log: ems.log / PID: $EMS_PID)"


# 🧠 [2. Run OSS Core Engine in Background]
echo "🧠 [2/3] Starting OSS Core Engine in background..."
cd oss-core
uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../oss.log 2>&1 &
OSS_PID=$!
cd ..
echo "   ✅ Done (Log: oss.log / PID: $OSS_PID)"


# ⏳ Wait for servers to fully boot up and bind to ports
echo "⏳ Waiting for servers to boot up (2 seconds)..."
sleep 2


# 🧑‍💼 [3. Run Interactive BSS Simulator in Foreground]
echo "🧑‍💼 [3/3] Launching Interactive BSS Simulator..."
echo "---------------------------------------------------"
# This process runs in the foreground and waits for user input.
# Once it exits, the script ends, triggering the cleanup trap above.
python simulators/mock_bss.py