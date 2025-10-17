from enum import Enum

class PptSessionState(Enum):
    COMFIRMFILES="confirmFiles"
    COMFIRMTARGET="confirmTarget"
    COMFIRMOUTLINE="confirmOutline"
    GENERATEPPT="generatePPT"
    COMPLETEGENERATION="completeGeneration"
    
class ClassType(Enum):
    NEW_LESSON="新授课"
    REVIEW_LESSON="复习课"