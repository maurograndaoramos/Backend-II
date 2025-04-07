from fastapi import FastAPI
from design_patterns_api.payments import PaymentService, PaymentGateway



api = FastAPI()

@api.get("/")
def index():
    return "Hello"

@api.post("/pay")
def process_payment(method:str):
    payment_service: PaymentService = PaymentGateway.build(method=method)
    return payment_service.process()