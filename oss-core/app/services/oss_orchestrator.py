import logging
from app.models.schemas import OnuProvisioningPayload, OssResponse
from app.translators.tl1_encoder import encoder
from app.translators.tl1_decoder import decoder
from app.controllers.ems_controller import ems_controller

# Setup logger for the service (orchestration) layer
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ProvisioningOrchestrator:
    """
    Core business logic controller that orchestrates the provisioning flow.
    It evaluates the equipment metadata, determines the appropriate EMS vendor,
    and delegates tasks to the Translator and Controller layers.
    """
    
    @staticmethod
    def olt_onu_register(
        request_id: str,
        remote_id: str,
        circuit_id: str,
        payload: OnuProvisioningPayload
    ) -> OssResponse:
        """
        Handles the ONU registration (provisioning) process.
        """
        logger.info(f"[ReqID: {request_id}] Starting ONU registration for RemoteID: {remote_id}")

        # 1. Identify Target EMS based on Remote ID metadata
        olt_vendor = "Huawei"
        ems_model = "U2000"
        
        if "NKA" in remote_id or "NOKIA" in remote_id.upper():
            olt_vendor = "Nokia"
            ems_model = "U5520"

        logger.info(f"[ReqID: {request_id}] Routing request to {olt_vendor} {ems_model} handler...")
        
        # 2. Call Encoder to translate payload into TL1 commands
        tl1_requests = encoder.encode_provisioning_cmd(
            vendor=olt_vendor,
            remote_id=remote_id,
            circuit_id=circuit_id,
            payload=payload
        )
        
        # 3. Call EMS Controller to transmit commands to the EMS and get the raw response
        raw_response = ems_controller.send_tl1_commands(tl1_requests)
        
        # 4. Call Decoder again to parse the raw response
        parsed_result = decoder.decode_response(raw_response)
        
        # Identify the last executed command for the receipt
        last_executed_cmd = tl1_requests[-1] if tl1_requests else "NONE"
        
        # 5. Return the standard OSS Response back to the receiver
        return OssResponse(
            errCode=0 if parsed_result["status"] == "SUCCESS" else 100,
            errMsg=f"Operation finished with status: {parsed_result['status']}",
            worthRetrying="false",
            requestInfo={
                "requestId": request_id,
                "remoteId": remote_id,
                "circuitId": circuit_id,
                "serialNo": payload.serialNo,
                "onuModel": payload.onuModel,
                "mode": payload.mode,
                "nwSpeed": payload.nwSpeed,
                "vlanId": payload.vlanId
            },
            operationInfo={
                "oltVendor": olt_vendor,
                "emsModel": ems_model
            },
            tl1CmdExecInfo={
                "lastCmd": last_executed_cmd,
                "lastResponse": parsed_result["message"]
            }
        )

# Singleton instance for the ems_controller to use
orchestrator = ProvisioningOrchestrator()