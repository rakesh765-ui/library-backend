from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    phone: str
    seat_no: str
    plan: str

    fee_amount: float

    entry_date: Optional[str] = None
    fee_due_date: Optional[str] = None

    status: Optional[str] = "Active"

    photo_url: Optional[str] = None
    id_photo_url: Optional[str] = None

class PaymentCreate(BaseModel):
    student_id: int
    amount: float
    payment_date: str
    remarks: str | None = None