from fastapi import FastAPI, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from fastapi.security.api_key import APIKeyHeader
from . import models, database, crud, schemas
from fastapi.middleware.cors import CORSMiddleware

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === API Key Config ===
API_KEY = "key1234567"  
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API key",
        )

# === DB Dependency ===
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "VM Management API (Secured)"}

# === ROUTES with Security ===

@app.post("/vms/", response_model=schemas.VMOut)
def create_vm(vm: schemas.VMCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    return crud.create_vm(db, vm)

@app.get("/vms/", response_model=list[schemas.VMOut])
def get_vms(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    return crud.get_vms(db)

@app.get("/vms/{vm_id}", response_model=schemas.VMOut)
def get_vm(vm_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    vm = crud.get_vm(db, vm_id)
    if vm is None:
        raise HTTPException(status_code=404, detail="VM not found")
    return vm

@app.put("/vms/{vm_id}", response_model=schemas.VMOut)
def update_vm(vm_id: int, updated_vm: schemas.VMUpdate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    vm = crud.update_vm(db, vm_id, updated_vm)
    if vm is None:
        raise HTTPException(status_code=404, detail="VM not found")
    return vm

@app.delete("/vms/{vm_id}")
def delete_vm(vm_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    vm = crud.delete_vm(db, vm_id)
    if vm is None:
        raise HTTPException(status_code=404, detail="VM not found")
    return {"message": f"VM {vm_id} deleted"}

@app.patch("/vms/{vm_id}/toggle_status", response_model=schemas.VMOut)
def toggle_status(vm_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    vm = crud.toggle_vm_status(db, vm_id)
    if vm is None:
        raise HTTPException(status_code=404, detail="VM not found")
    return vm
