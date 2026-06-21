from sqlalchemy import Column, BigInteger, Text, Date, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(BigInteger, primary_key=True, index=True)

    name = Column(Text)
    phone = Column(Text)
    seat_no = Column(Text, unique=True)

    plan = Column(Text)

    entry_date = Column(Date)

    fee_amount = Column(Numeric)

    fee_due_date = Column(Date)

    status = Column(Text)
    photo_url = Column(Text)
    id_photo_url = Column(Text)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(BigInteger, primary_key=True, index=True)

    student_id = Column(BigInteger)

    amount = Column(Numeric)

    payment_date = Column(Date)

    remarks = Column(Text)
