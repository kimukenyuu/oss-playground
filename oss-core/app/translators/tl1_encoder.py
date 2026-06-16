import logging
from app.models.schemas import OnuProvisioningPayload

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Tl1Encoder:
    """
    Domain service dedicated to outbound translation (Encoding).
    Converts logical Python models into vendor-specific raw TL1 command streams.
    """

    @staticmethod
    def encode_provisioning_cmd(
        vendor: str, 
        remote_id: str, 
        circuit_id: str, 
        payload: OnuProvisioningPayload
    ) -> list[str]:
        """
        Encodes the incoming Python payload into vendor-specific TL1 commands.
        Returns a list of commands since provisioning usually requires a sequence of multiple commands.
        """
        commands = []
        logger.info(f"Encoding TL1 commands for {vendor} equipment...")

        if vendor == "Huawei":
            # TL1 syntax for Huawei equipment (example)
            commands.append(f"ENT-ONT::{remote_id}:{circuit_id}::SRN={payload.serialNo},MODE={payload.mode};")
            commands.append(f"CRT-SERVICEPORT::{remote_id}:{circuit_id}::VLAN={payload.vlanId},SPEED={payload.nwSpeed};")
            
        elif vendor == "Nokia":
            # TL1 syntax for Nokia equipment (example)
            commands.append(f"ENT-ONTUPROP::{remote_id}:{circuit_id}::SERNUM={payload.serialNo};")
            commands.append(f"ENT-VLANCROSS::{remote_id}:{circuit_id}::VLANID={payload.vlanId};")
            
        else:
            logger.error(f"Unknown vendor: {vendor}")
            raise ValueError("Unsupported equipment vendor")

        return commands
    
# Singleton instance for the orchestrator to use
encoder = Tl1Encoder()