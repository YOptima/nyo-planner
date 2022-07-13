import uuid

# Logging Configurations
import logging
logger = logging.getLogger(__name__)

# Get Unique Integer ID
# -- Generated from UUID 
# -- Maximum 128bit size supported
def getUniqueId(nbits: int = 32) -> int:
    
    if nbits > 128: nbits = 128
    if nbits < 0: nbits = 0

    # Calculate nBit Id
    # -- nBit = 3 => (2^3 - 1) = 7 = (111)
    unique_id = uuid.uuid4().int
    masking_bits = (( 1 << nbits ) - 1)
    final_id = unique_id & masking_bits

    return final_id