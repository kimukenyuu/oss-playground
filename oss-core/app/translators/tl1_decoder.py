import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Tl1Decoder:
    """
    Domain service dedicated to inbound translation (Decoding).
    Parses downstream raw text streams into clear, uniform system status maps.
    """

    @staticmethod
    def decode_response(raw_tl1_response: str) -> dict:
        """
        Interprets raw TL1 completion lines into structured outcome messages.
        """
        logger.info("Decoding downstream text payload into structured status map...")
        result = {
            "status": "UNKNOWN",
            "message": raw_tl1_response.replace("\n", " ").strip()
        }

        if "COMPLD" in raw_tl1_response.upper():
            result["status"] = "SUCCESS"
        elif "DENY" in raw_tl1_response.upper():
            result["status"] = "ERROR"

        return result

# Singleton instance for the orchestrator to use
decoder = Tl1Decoder()