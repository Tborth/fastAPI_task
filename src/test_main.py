from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from  db import Base
from  main import app
from route import  get_db
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


    
data={"service_date":"3/28/18 0:00",
    "submitted_procedure":"D0180",
    "quadrant":"UR",
    "plan_group":"GRP-1000",
    "subscriber":"3730189502",
    "provider_npi":"1497775530",
    "provider_fees":"$100.00",
    "allowed_fees":"$100.00",
    "member_coinsurance":"$0.00",
    "member_copay":"$0.00" }

def test_create_claim():
    response = client.post("/claim_process/claims",json=data)
    # print(response.json())
    assert response.status_code == 201
    assert response.json() ==  {"service_date":"3/28/18 0:00",
                                                        "submitted_procedure":"D0180",
                                                        "quadrant":"UR",
                                                        "plan_group":"GRP-1000",
                                                        "subscriber":"3730189502",
                                                        "provider_npi":"1497775530",
                                                        "provider_fees":100.00,
                                                        "allowed_fees":100.00,
                                                        "member_coinsurance":0.00,
                                                        "member_copay":0.00}

def test_upload():
    print(dir_path)
    with open(dir_path+"/"+"test_file/" "claim_1234.csv","rb") as file:
        response = client.post(
        "/claim_process/upload", files={"file": ("filename", file)})
        assert response.status_code == 201
        assert response.json() == {"4346": {
                                "service date": "3/28/18 0:00",
                                "submitted procedure": {},
                                "quadrant": "",
                                "Plan/Group #": "GRP-1000",
                                "Subscriber#": "3730189502",
                                "Provider NPI": "149777553",
                                "provider fees": "$130.00 ",
                                "Allowed fees": "$65.00 ",
                                "member coinsurance": "$16.25 ",
                                "member copay": "$0.00 "
                            },
                            "D0180": {
                                "service date": "3/28/18 0:00",
                                "submitted procedure": "D0180",
                                "quadrant": "",
                                "Plan/Group #": "GRP-1000",
                                "Subscriber#": "3730189502",
                                "Provider NPI": "1497775530",
                                "provider fees": "$100.00 ",
                                "Allowed fees": "$100.00 ",
                                "member coinsurance": "$0.00 ",
                                "member copay": "$0.00 "
                            },
                            "D0210": {
                                "service date": "3/28/18 0:00",
                                "submitted procedure": "D0210",
                                "quadrant": "",
                                "Plan/Group #": "GRP-1000",
                                "Subscriber#": "3730189502",
                                "Provider NPI": "1497775530",
                                "provider fees": "$108.00 ",
                                "Allowed fees": "$108.00 ",
                                "member coinsurance": "$0.00 ",
                                "member copay": "$0.00 "
                            }
                            }

def test_generate():
    response = client.get("/claim_process/generate")
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_compute():
    # case 1
    response = client.get("/claim_process/compute/<submitted_procedure>?submitted_procedure=D0180")
    assert response.status_code == 200
    assert response.json() == {'fees': 0.0} 
    
    # case 2
    response = client.get("/claim_process/compute/<submitted_procedure>?submitted_procedure=B0180")
    assert response.status_code == 200
    assert response.json() == {"fees": "does not avaliable"}
    


