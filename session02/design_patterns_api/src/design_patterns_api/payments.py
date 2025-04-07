from abc import ABC, abstractmethod

def paypal_payment():
    return {"message": "Processing PayPal payment"}
def gpay_payment():
    return {"message": "Processing Google Wallet payment"}
def applepay_payment():
    return {"message": "Processing Apple Pay payment"}
def mbway_payment():
    return {"message": "Processing MB Way payment"}

class PaymentService(ABC):
    @abstractmethod
    def process(*args, **kwargs) -> str:
        return NotImplemented

class PaypalService(PaymentService):
    def process(self, *args, **kwargs) -> str:
        return paypal_payment()
    
class ApplePayService(PaymentService):
    def process(self, *args, **kwargs) -> str:
        return applepay_payment()
    
class MbwayService(PaymentService):
    def process(self, *args, **kwargs) -> str:
        return mbway_payment()
    
class GpayService(PaymentService):
    def process(self, *args, **kwargs) -> str:
        return gpay_payment()

class PaymentGateway:
    registry = {
        "paypal": PaypalService,
        "gpay": gpay_payment,
        "applepay": ApplePayService,
        "mbway": mbway_payment
    }

    @classmethod
    def build (cls, method: str) -> PaymentService:
        return cls.registry.get(method, None)()