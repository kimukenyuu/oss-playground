from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

# Create a mock client for FastAPI
client = TestClient(app)

@patch("app.services.oss_orchestrator.ems_controller.send_tl1_commands")
def test_register_onu_api_success(mock_send_tl1):
    # 1. Given: Mock EMS returning a successful COMPLD response
    mock_send_tl1.return_value = " RID: NKA-TEST Time: 2099-12-31\nM 001 COMPLD\n;"
    
    valid_payload = {
        "serialNo": "5A54454706100003",
        "onuModel": "ZF10002",
        "mode": "BRIDGE",
        "nwSpeed": "10G",
        "vlanId": 14
    }
    
    # 2. When: Send POST request simulating BSS
    response = client.post(
        "/api/v1/olts/NKA-Tokyo-OLT/onus/1-2-3-4",
        json=valid_payload,
        headers={"x-request-id": "TEST-REQ-SUCCESS"}
    )
    
    # 3. Then: Verify 200 OK and valid JSON receipt
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["errCode"] == 0
    assert response_data["operationInfo"]["oltVendor"] == "Nokia"
    assert "COMPLD" in response_data["tl1CmdExecInfo"]["lastResponse"]
    
    mock_send_tl1.assert_called_once()


@patch("app.services.oss_orchestrator.ems_controller.send_tl1_commands")
def test_register_onu_api_ems_deny(mock_send_tl1):
    # 1. Given: Mock EMS rejecting the command (DENY)
    mock_send_tl1.return_value = " RID: LABC501a Time: 2099-12-31\nM 001 DENY\n/* DUPLICATE MAC ADDRESS */\n;"
    
    valid_payload = {
        "serialNo": "5A54454706100003",
        "onuModel": "HG8145V5",
        "mode": "ROUTER",
        "nwSpeed": "1G",
        "vlanId": 20
    }
    
    # 2. When: Send POST request simulating BSS
    response = client.post(
        "/api/v1/olts/LABC501a-OLT01z/onus/0-1-15-33",
        json=valid_payload,
        headers={"x-request-id": "TEST-REQ-DENY"}
    )
    
    # 3. Then: HTTP is 200 OK, but business logic returns errCode 100 (Error)
    assert response.status_code == 200
    response_data = response.json()
    
    # Check business error code and message
    assert response_data["errCode"] == 100
    assert "ERROR" in response_data["errMsg"]
    assert "DENY" in response_data["tl1CmdExecInfo"]["lastResponse"]


def test_register_onu_validation_error():
    # 1. Given: Invalid payload (serial number length < 16)
    invalid_payload = {
        "serialNo": "SHORT_SN", 
        "onuModel": "ZF10002",
        "mode": "BRIDGE",
        "nwSpeed": "10G",
        "vlanId": 99
    }
    
    # 2. When: Send POST request
    response = client.post(
        "/api/v1/olts/NKA-Seoul-OLT/onus/1-1-1-1",
        json=invalid_payload,
        headers={"x-request-id": "TEST-REQ-INVALID"}
    )
    
    # 3. Then: Verify Pydantic validation catches it and returns 422 HTTP Error
    assert response.status_code == 422