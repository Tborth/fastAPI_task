

from fastapi import APIRouter,FastAPI,UploadFile,File,Request,Depends

from db import engine,sessionlocal
from sqlalchemy.orm import Session

from datetime import datetime
from schema import Claims
from typing import Union
import csv
import codecs
import random
import models

models.Base.metadata.create_all(bind=engine)
claim_process = APIRouter()
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
        

@claim_process.get("/")
def read_root():
    return {"message": "go to /docs"}


def dollor_float(value):
    return float(value[1:]) if float(value[1:]) else 0.0


@claim_process.post("/claim_process/claims",status_code=201)
def create_claim(claim: Claims,db: Session = Depends(get_db)):
    try:
        provider_fees= dollor_float( claim.provider_fees )
        allowed_fees=  dollor_float(claim.allowed_fees)
        member_coinsurance=   dollor_float(claim.member_coinsurance)
        member_copay= dollor_float(claim.member_copay)
        
        claims = models.Claims(service_date=claim.service_date,
                                    submitted_procedure=claim.submitted_procedure,
                                    quadrant=claim.quadrant,
                                    plan_group=claim.plan_group,
                                    subscriber=claim.subscriber,
                                    provider_npi=claim.provider_npi,
                                    provider_fees=provider_fees,
                                    allowed_fees=allowed_fees,
                                    member_coinsurance=member_coinsurance,
                                    member_copay=member_copay)
        db.add(claims)
        db.commit()
    except Exception as e:
        print(e)
        
    return {"service_date": claim.service_date, "submitted_procedure": claim.submitted_procedure,
            "quadrant":claim.quadrant,"plan_group":claim.plan_group,"subscriber":claim.subscriber,"provider_npi":claim.provider_npi,
            "provider_fees":provider_fees,"allowed_fees":allowed_fees,"member_coinsurance":member_coinsurance,"member_copay":member_copay}



#  upload the with the file
@claim_process.post("/claim_process/upload",status_code=201)
def upload(file: UploadFile = File(...),db: Session = Depends(get_db)):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
   
    
    data = {}
    try:
        for rows in csvReader:             
            key = rows['submitted procedure']  
            data[key] = rows 
            # remove the dollor sign
            provider_fees= dollor_float(rows['provider fees'])
            allowed_fees=  dollor_float(rows['Allowed fees'])
            member_coinsurance=  dollor_float(rows['member coinsurance'])
            member_copay= dollor_float(rows['member copay']) 
            # validation check for provider NPI and submitted procedure
            provider_npi=str(rows['Provider NPI']) if len(rows['Provider NPI']) == 10 else ValueError("provider NPI must be lenght 10")
            submitted_procedure=rows['submitted procedure'] = submitted_procedure=rows['submitted procedure'] if rows['submitted procedure'][0] =="D" else ValueError("must start with D")
            
            claims = models.Claims(service_date=rows['service date'],
                                submitted_procedure=submitted_procedure,
                                quadrant=rows['quadrant'],
                                plan_group=rows['Plan/Group #'],
                                subscriber=rows['Subscriber#'],
                                provider_npi=provider_npi,
                                provider_fees=provider_fees,
                                allowed_fees=allowed_fees,
                                member_coinsurance=member_coinsurance,
                                member_copay=member_copay)
            db.add(claims)
            db.commit()
        
        file.file.close()
    except Exception as e:
        print(e)
    return data
    
   
    

@claim_process.get("/claim_process/claims_all",tags=["address"])
async def home(request:Request,db:Session = Depends(get_db)):
    Claims = db.query(models.Claims)
    claim_list=[]
    for claims_obj in Claims:
        per=[]
       
        per.append(claims_obj.id)
        per.append(claims_obj.service_date)
        per.append(claims_obj.submitted_procedure)
        per.append(claims_obj.quadrant)
        per.append(claims_obj.plan_group)
        per.append(claims_obj.subscriber)
        per.append(claims_obj.provider_npi)
        per.append(claims_obj.provider_fees)
        per.append(claims_obj.allowed_fees)
        per.append(claims_obj.member_coinsurance)
        per.append(claims_obj.member_copay)
        claim_list.append(per)
    print(claim_list)
    return {"msg":claim_list,"respone_code":200}

@claim_process.get("/claim_process/generate",)
async def generate(db:Session = Depends(get_db)):
    while True:
        uid = str(random.randint(0, 999999)).zfill(6)
        ids = db.query(models.ClaimsIds).filter(models.ClaimsIds.generated_id == uid).one_or_none()
        print(ids)
        if ids:
            continue
        else:
            
            claims = models.ClaimsIds(generated_id=uid)
            db.add(claims)
            db.commit()
            return uid
        
@claim_process.get("/claim_process/generate/all")
async def generate_all(db:Session = Depends(get_db)):
    Claims = db.query(models.ClaimsIds)
    claim_list=[]
    for claims_obj in Claims:
        per=[] 
        per.append(claims_obj.generated_id)
        claim_list.append(per)
    return {"msg":claim_list}




@claim_process.get("/claim_process/compute/<submitted_procedure>")
async def compute(submitted_procedure:str,db:Session = Depends(get_db)):
    record = db.query(models.Claims).filter(models.Claims.submitted_procedure == submitted_procedure).all()
 
    if record:
        fees = float(record[0].provider_fees) + float(record[0].member_coinsurance) + float(record[0].member_copay) -  float(record[0].allowed_fees)
        return {"fees":fees}
    else:
        return {"fees": "does not avaliable"}
    