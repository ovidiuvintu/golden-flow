
import logging

logger = logging.getLogger(__name__)

class TreatmentService:
    def __init__(self):
        pass

    # Public interface methods
    def list_treatments(self) -> None:
        pass

    async def start_treatment(self) -> None:
        pass

    def stop_treatment(self) -> None:
        pass 

    def change_state(self) -> None:
        pass      
    
    # Private helper methods
    def _insert_treatment(self) -> None:
        pass

    def _update_treatment_state(self) -> None:
       pass

    def _get_treatment(self) -> None:
        pass

    def _stream_worker(self) -> None:
        pass
