
from fastapi import FastAPI


tags_metadata = [
    {
        "name": "Upload",
        "description": "claim_process/Upload Used to create the add the data with csv file in claim table ",
    },
    {
        "name": "claims",
        "description": "/claim_process/claims",
        
    },
    {
        "name": "generate",
        "description": "/claim_process/generate Used to generate the unique id",
    },
    {
        "name": "compute",
        "description": "/claim_process/compute/<submitted_procedure> Used to compute the fees",
    },
]

app =FastAPI(openapi_tags=tags_metadata)

import uvicorn
from route import claim_process


app.include_router(claim_process)


if __name__ == "__main__":
    uvicorn.run(app,host='0.0.0.0',port=8001)
