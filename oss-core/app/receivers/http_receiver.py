from fastapi import APIRouter, Header, Path, Body
from app.models.schemas import OnuProvisioningPayload, OssResponse

# Create a router instance for handling BSS requests
router = APIRouter(
    prefix="/api/v1",
    tags=["BSS Provisioning API"]
)

@router.post(
    "/olts/{remote_id}/onus/{circuit_id}",
    response_model=OssResponse,
    summary="Register a new ONU",
    description="Receives an ONU provisioning request from BSS and initiates the TL1 execution sequence."
)
async def register_onu(
    remote_id: str = Path(..., description="Target OLT Remote ID (e.g., LABC501a-OLT01z)"),
    circuit_id: str = Path(..., description="Target Circuit ID (Frame-Slot-Port-ONU)"),
    payload: OnuProvisioningPayload = Body(..., description="ONU details (Serial, Model, etc.)"),
    x_request_id: str = Header(..., description="Unique transaction ID provided by BSS")
):
    """
    Controller logic to handle the incoming HTTP request.
    Currently returns a mock successful response.
    """
    # TODO: Pass the extracted parameters to the core business logic (e.g., NuroOssIfImpl)
    
    # Return a dummy response indicating the request was received
    return OssResponse(
        errCode=0,
        errMsg="Success. Received provisioning request.",
        worthRetrying="false",
        requestInfo={
            "requestId": x_request_id,
            "remoteId": remote_id,
            "circuitId": circuit_id,
            "serialNo": payload.serialNo
        }
    )