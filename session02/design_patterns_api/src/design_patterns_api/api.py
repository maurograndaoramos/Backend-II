from fastapi import FastAPI, HTTPException

from design_patterns_api.factory import ShapeFactory
from design_patterns_api.observer import ObserverA, ObserverB, Subject
from design_patterns_api.payments import PaymentGateway, PaymentService

api = FastAPI()

@api.get("/")
def index():
    return "Hello"

@api.post("/pay")
def process_payment(method:str):
    payment_service: PaymentService = PaymentGateway.build(method=method)
    payment_service.process()
    return

@api.post("/create_shape/{shape_type}")
def create_shape(shape_type: str):
    try:
        shape = ShapeFactory.create_shape(shape_type)
        return {"message": shape.process()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
subject = Subject()
observer_a = ObserverA()
observer_b = ObserverB()

subject.attach(observer_a)
subject.attach(observer_b)

@api.post("/notify")
def notify_observers(message: str):
    subject.notify(message)
    return {"message": "Observers notified"}

@api.post("/detach/{observer_id}")
def detach_observer(observer_id: str):
    if observer_id == "ObserverA":
        subject.detach(observer_a)
        return {"message": "Observer A detached"}
    elif observer_id == "ObserverB":
        subject.detach(observer_b)
        return {"message": "Observer B detached"}
    else:
        raise HTTPException(status_code=404, detail="Observer not found")