from pydantic import BaseModel,ValidationError, validator
from typing import Union

class Claims(BaseModel):
    service_date:str
    submitted_procedure: str
    quadrant: Union[str, None] 
    plan_group:  Union[str, None] 
    subscriber: str
    provider_npi: str
    provider_fees: str
    allowed_fees: str
    member_coinsurance: str
    member_copay: str

    @validator('submitted_procedure')
    def start_with_d(cls, v):
        if 'D' not in v[0]:
            raise ValueError('must start with D')
        return v
    
    @validator('provider_npi')
    def count_len(cls, v):
        if len(v) != 10:
            raise ValueError('provider NPI must be lenght 10')
        return v
    

