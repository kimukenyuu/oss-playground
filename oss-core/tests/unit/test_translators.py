import pytest
from app.translators.tl1_encoder import encoder
from app.translators.tl1_decoder import decoder
from app.models.schemas import OnuProvisioningPayload

def test_tl1_encoder_nokia_logic():
    # 1. Given: Prepare mock payload data
    mock_payload = OnuProvisioningPayload(
        serialNo="1234567890ABCDEF",
        onuModel="NOK_MODEL",
        mode="BRIDGE",
        nwSpeed="10G",
        vlanId=99
    )
    
    # 2. When: Execute encoder for Nokia equipment
    result_commands = encoder.encode_provisioning_cmd(
        vendor="Nokia",
        remote_id="NKA-TEST-01",
        circuit_id="1-1-1-1",
        payload=mock_payload
    )
    
    # 3. Then: Verify the generated TL1 commands
    assert len(result_commands) == 2
    assert "ENT-ONTUPROP::NKA-TEST-01" in result_commands[0]
    assert "SERNUM=1234567890ABCDEF" in result_commands[0]
    assert "ENT-VLANCROSS" in result_commands[1]


def test_tl1_decoder_success_response():
    # 1. Given: Mock successful response from EMS (COMPLD)
    mock_raw_response = " RID: NKA-TEST Time: 2099-12-31\nM 001 COMPLD\n;"
    
    # 2. When: Execute decoder parsing
    parsed_result = decoder.decode_response(mock_raw_response)
    
    # 3. Then: Verify it returns SUCCESS
    assert parsed_result["status"] == "SUCCESS"


def test_tl1_decoder_failure_response():
    # 1. Given: Mock failed response from EMS (DENY)
    mock_raw_response = " RID: NKA-TEST Time: 2099-12-31\nM 001 DENY\n/* INVALID SERIAL NUMBER */\n;"
    
    # 2. When: Execute decoder parsing
    parsed_result = decoder.decode_response(mock_raw_response)
    
    # 3. Then: Verify it interprets the denial as an ERROR
    assert parsed_result["status"] == "ERROR"