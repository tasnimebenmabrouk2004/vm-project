from sqlalchemy.orm import Session
from . import models, schemas

def get_vms(db: Session):
    return db.query(models.VM).all()

def get_vm(db: Session, vm_id: int):
    return db.query(models.VM).filter(models.VM.id == vm_id).first()

def create_vm(db: Session, vm: schemas.VMCreate):
    db_vm = models.VM(**vm.dict())
    db.add(db_vm)
    db.commit()
    db.refresh(db_vm)
    return db_vm

def delete_vm(db: Session, vm_id: int):
    vm = db.query(models.VM).filter(models.VM.id == vm_id).first()
    if vm:
        db.delete(vm)
        db.commit()
    return vm

def update_vm(db: Session, vm_id: int, updated: schemas.VMUpdate):
    vm = db.query(models.VM).filter(models.VM.id == vm_id).first()
    if vm:
        for key, value in updated.dict().items():
            setattr(vm, key, value)
        db.commit()
        db.refresh(vm)
    return vm

def toggle_vm_status(db: Session, vm_id: int):
    vm = db.query(models.VM).filter(models.VM.id == vm_id).first()
    if vm:
        vm.status = "running" if vm.status == "stopped" else "stopped"
        db.commit()
        db.refresh(vm)
    return vm
