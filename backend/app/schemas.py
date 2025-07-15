from pydantic import BaseModel

class VMBase(BaseModel):
    name: str
    os: str
    cpu: int
    ram: int

class VMCreate(VMBase):
    pass  #  creating a new VM

class VMUpdate(VMBase):
    pass  #  updating a VM

class VMOut(VMBase):#les reponses des api
    id: int
    status: str

    class Config:
        orm_mode = True
