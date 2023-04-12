from sqlalchemy import Column,Integer,String,Float,Date

from db import Base

class Claims(Base):
    __tablename__ = 'claims'
    
    id = Column(Integer,primary_key =True)
    service_date = Column(String(150))
    submitted_procedure =  Column(String(150))
    quadrant = Column(String(150))
    plan_group = Column(String(150))
    subscriber = Column(String(150))
    provider_npi= Column(String(150))
    provider_fees=Column(Float)
    allowed_fees= Column(Float)
    member_coinsurance = Column(Float)
    member_copay= Column(Float)
    
    def __repr__(self):
        return '<claim %r ' % (self.id)
    
class ClaimsIds(Base):
    __tablename__ = 'claimsids'
    
    id = Column(Integer,primary_key =True)
    generated_id =Column(Integer, unique =True)
    
    def __repr__(self):
        return '<claimid %r ' % (self.generated_id)