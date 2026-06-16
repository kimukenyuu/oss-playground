from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# ==========================================
# 1. BSS -> OSS (Request Data Models)
# ==========================================
class OnuProvisioningPayload(BaseModel):
    serialNo: str = Field(
        ..., 
        min_length=16, 
        max_length=16, 
        description="ONU Serial number (16-character hex string)", 
        example="5A54454706100003"
    )
    onuModel: str = Field(
        ..., 
        description="ONU device model name", 
        example="ZF10002"
    )
    mode: str = Field(
        ..., 
        description="Service operation mode", 
        example="BRIDGE"
    )
    nwSpeed: str = Field(
        ..., 
        description="Network line speed", 
        example="10G"
    )
    vlanId: int = Field(
        ..., 
        description="VLAN ID to be allocated", 
        example=14
    )


# ==========================================
# 2. OSS -> BSS (Response Data Models)
# ==========================================
class OssResponse(BaseModel):
    errCode: int = Field(..., description="Result code (0: Success, 100+: Error)", example=0)
    errMsg: str = Field(..., description="Detailed result message", example="Success.")
    worthRetrying: str = Field("false", description="Flag indicating if the request is worth retrying")
    
    requestInfo: Optional[Dict[str, Any]] = Field(
        None, 
        description="Original metadata of the received request"
    )
    operationInfo: Optional[Dict[str, Any]] = Field(
        None, 
        description="Information about the operated EMS/OLT equipment"
    )
    tl1CmdExecInfo: Optional[Dict[str, Any]] = Field(
        None, 
        description="Information about the last executed TL1 command and response"
    )