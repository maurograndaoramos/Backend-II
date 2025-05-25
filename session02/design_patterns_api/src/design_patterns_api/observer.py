from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class ObserverA(Observer):
    def update(self, message: str):
        print(f"ObserverA received: {message}")

class ObserverB(Observer):
    def update(self, message: str):
        print(f"ObserverB received: {message}")