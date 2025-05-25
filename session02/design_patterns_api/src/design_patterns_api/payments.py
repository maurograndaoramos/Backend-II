from abc import ABC

class PaymentService(ABC):
    def process(*arg, **kwargs):
        return NotImplemented

class PayPalService(PaymentService):
    def process(*arg, **kwargs):
        return "Paypal"
        # ...
        # return super().process(**kwargs)

class ApplePayService(PaymentService):
    def process(*arg, **kwargs):
        return "ApplePay"
        # ...
        # return super().process(**kwargs)

class GPayService(PaymentService):

    def process(*arg, **kwargs):
        return super().process(**kwargs)
    
class MbService(PaymentService):

    def process(*arg, **kwargs):
        return super().process(**kwargs)
    
class PaymentGateway:
    registry = {
        "paypal":PayPalService,
        "applepay":ApplePayService,
    }
    @classmethod
    def build(cls, method:str)-> PaymentService:
        return cls.registry.get(method, None)()