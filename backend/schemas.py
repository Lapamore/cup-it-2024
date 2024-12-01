from typing import List, Dict
from pydantic import BaseModel

class SignaturesCommon(BaseModel):
    mobile: int
    web: int

class SignaturesSpecial(BaseModel):
    mobile: int
    web: int

class Signatures(BaseModel):
    common: SignaturesCommon
    special: SignaturesSpecial

class UserData(BaseModel):
    clientId: str
    organizationId: str
    segment: str
    role: str
    organizations: int
    currentMethod: str
    mobileApp: bool
    signatures: Signatures
    availableMethods: List[str]
    claims: int

class MethodResponse(BaseModel):
    method: str

class AvailableMethodsResponse(BaseModel):
    available_methods: List[str]

class RecommendationResponse(BaseModel):
    recommended_method: str
    confidence: float 
