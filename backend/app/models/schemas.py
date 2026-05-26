from pydantic import BaseModel
from typing import List, Optional


class InvoiceCreate(BaseModel):
    file_name: str


class InvoiceOut(BaseModel):
    id: int
    file_name: str
    status: str

    class Config:
        from_attributes = True

class PdfScanCheckOut(BaseModel):
    is_scanned: bool
    total_text_chars: int
    page_count: int

class PdfTextOut(BaseModel):
    text: str
    source: str
    is_scanned: bool
    total_text_chars: int
    page_count: int

class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None
    tax_rate: Optional[float] = None

class InvoiceExtracted(BaseModel):
    invoice_number: Optional[str] = None
    issue_date: Optional[str] = None
    due_date: Optional[str] = None
    vendor_name: Optional[str] = None
    vendor_tax_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_tax_id: Optional[str] = None
    currency: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    withholding: float = 0.0
    total: Optional[float] = None
    line_items: List[LineItem] = []

class InvoiceValidationOut(BaseModel):
    is_valid: bool
    errors: list[str]

class TextChunkOut(BaseModel):
    chunk_id: str
    content: str
    start_index: int | None = None