from fastapi import APIRouter, Header, Path, Body
from app.models.schemas import OnuProvisioningPayload, OssResponse
from app.services.oss_orchestrator import orchestrator

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
    Delegates the actual processing to the service layer (oss_interface).
    """
    # Pass the extracted parameters to the core business logic and return the result to BSS
    return orchestrator.olt_onu_register(
        request_id=x_request_id,
        remote_id=remote_id,
        circuit_id=circuit_id,
        payload=payload
    )