from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal
from models import Student, Payment
from schemas import StudentCreate
from schemas import PaymentCreate
from datetime import date
from sqlalchemy import text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Library API Running"}

@app.post("/students")
def add_student(student: StudentCreate):

    print("POST START")

    db = SessionLocal()

    print(student.dict())

    new_student = Student(
        name=student.name,
        phone=student.phone,
        seat_no=student.seat_no,
        plan=student.plan,
        fee_amount=student.fee_amount,
        entry_date=student.entry_date,
        fee_due_date=student.fee_due_date,
        status=student.status,
        photo_url=student.photo_url,
        id_photo_url=student.id_photo_url
    )

    print("BEFORE ADD")
    db.add(new_student)

    print("BEFORE COMMIT")
    db.commit()

    print("AFTER COMMIT")

    db.refresh(new_student)

    db.close()

    return {
        "message": "Student Added",
        "id": new_student.id
    }
@app.get("/students")
def get_students():

    db = SessionLocal()

    students = db.query(Student).all()

    result = []

    for s in students:
        result.append({
    "id": s.id,
    "name": s.name,
    "phone": s.phone,
    "seat_no": s.seat_no,
    "plan": s.plan,

    "fee_amount":
        float(s.fee_amount)
        if s.fee_amount else 0,

    "entry_date":
        str(s.entry_date)
        if s.entry_date else "",

    "fee_due_date":
        str(s.fee_due_date)
        if s.fee_due_date else "",

    "status": s.status
})

    db.close()

    return result

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: StudentCreate
):

    db = SessionLocal()

    existing = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not existing:
        db.close()
        return {
            "message": "Student not found"
        }

    existing.name = student.name
    existing.phone = student.phone
    existing.seat_no = student.seat_no
    existing.plan = student.plan
    existing.fee_amount = student.fee_amount
    existing.status = student.status

    db.commit()

    db.close()

    return {
        "message": "Updated"
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    db = SessionLocal()

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        db.close()
        return {
            "message": "Student not found"
        }

    db.delete(student)
    db.commit()

    db.close()

    return {
        "message": "Deleted"
    }

@app.get("/dashboard")
def dashboard():

    db = SessionLocal()

    students = db.query(Student).all()

    total_students = len(students)

    occupied_seats = len(students)

    due_students = 0
    overdue_students = 0

    today = date.today()

    for s in students:

        if s.fee_due_date:

            if s.fee_due_date <= today:
                overdue_students += 1

            elif (s.fee_due_date - today).days <= 7:
                due_students += 1

    db.close()

    return {
        "total_students": total_students,
        "occupied_seats": occupied_seats,
        "due_students": due_students,
        "overdue_students": overdue_students
    }


@app.get("/seats")
def seats():

    db = SessionLocal()

    students = db.query(Student).all()

    result = []

    for s in students:
        result.append({
            "seat_no": s.seat_no,
            "name": s.name,
            "phone": s.phone,
            "plan": s.plan
        })

    db.close()

    return result
@app.get("/settings")
def get_settings():

    db = SessionLocal()

    result = db.execute(
        text(
            "select total_seats from settings limit 1"
        )
    ).fetchone()

    db.close()

    return {
        "total_seats": result[0]
    }


@app.put("/settings")
def update_settings(data: dict):

    db = SessionLocal()

    db.execute(
        text(
            "update settings set total_seats=:n"
        ),
        {"n": data["total_seats"]}
    )

    db.commit()
    db.close()

    return {
        "message": "saved"
    }

@app.post("/payments")
def add_payment(payment: PaymentCreate):

    db = SessionLocal()

    new_payment = Payment(
        student_id=payment.student_id,
        amount=payment.amount,
        payment_date=payment.payment_date,
        remarks=payment.remarks
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    db.close()

    return {
        "message": "Payment Added"
    }

@app.get("/payments/{student_id}")
def get_payments(student_id: int):

    db = SessionLocal()

    payments = db.query(Payment)\
        .filter(Payment.student_id == student_id)\
        .all()

    db.close()

    return payments