import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Just an abstration for now

class MqttService:
    
    def __init__(self, broker_url: Optional[str] = None):
        self.broker_url = broker_url

    def publish(self, topic: str, payload: Dict[str, Any]) -> None:
        # TODO: Implement mqtt publish
        logger.info("Publish to %s: %s", topic, payload)

