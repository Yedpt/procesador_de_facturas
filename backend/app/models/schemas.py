from pydantic import BaseModel


class InvoiceCreate(BaseModel):
    file_name: str


class InvoiceOut(BaseModel):
    id: int
    file_name: str
    status: str

    class Config:
        from_attributes = True