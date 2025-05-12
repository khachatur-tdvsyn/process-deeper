from random import choice
from queue import Queue
import json

from core.base import MonitoringResponse, ResponseType
from core.serializers import DataclassJSONEncoder

class FakeServer:
    def __init__(self):
        self.data = Queue()
        self.comments = {
            ResponseType.OK: "",
            ResponseType.WARNING: "Something happens",
            ResponseType.SUSPICIOUS_PROCESS: "This is a suspicious process with pid:",
            ResponseType.FULL_MEMORY: "Your memory is full!"
        }

    def send(self, request):
        print(request)
        self._resolve_result()
    
    def _resolve_result(self):
        #key = ResponseType.SUSPICIOUS_PROCESS
        key = choice(list(self.comments.keys()))
        self.data.put(MonitoringResponse(key, self.comments[key]))
    
    def receive(self):
        data = self.data.get()
        res = json.dumps(data, cls=DataclassJSONEncoder)
        return res