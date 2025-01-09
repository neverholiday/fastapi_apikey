#!/usr/bin/env python3

import uuid

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from pydantic import BaseModel

API_KEY = "this is a secret"

class StudentCreateRequest(BaseModel):
    name: str

class StudentCreateResponse(BaseModel):
    id: str
    name: str


app = FastAPI()

header_scheme = APIKeyHeader(name='x-api-key')

def api_key_auth(api_key:str=Depends(header_scheme)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

@app.get("/healthz", dependencies=[Depends(api_key_auth)])
async def healthcheck():
    return {"message": "healthy"}

@app.post('/api/v1/students/create', dependencies=[Depends(api_key_auth)])
async def create_student(req:StudentCreateRequest):
    return StudentCreateResponse(
        id=str(uuid.uuid4()),
        name=req.name
    )
