import time

import json
import re

from typing import Callable

from threading import Thread
from core.base import ComputerInfo, Stat, ProcessStat, MonitoringResponse, ResponseType
from .system_info import get_system_info

from core.serializers import DataclassJSONEncoder
from .fake_server import FakeServer


class Agent:
    def __init__(self, sensors: dict[str,Callable], send_rate: float):
        self.sensors = sensors
        self.computer_info = get_system_info()
        self.sensors_result = {}

        if(send_rate <= 0):
            raise ValueError("Send rate must be positive number")
        self.send_rate = send_rate

        self.started = False
        self.thread = None
        self.encoder = DataclassJSONEncoder()
        #Temp
        self.server = FakeServer()
    
    def run(self):
        self.send(self.computer_info)
        while self.started:
            for i in self.sensors:
                self.sensors_result[i] = self.sensors[i]()
            #Temporary
            self.send(self.sensors_result)
            self.receive()
            time.sleep(self.send_rate)
            
    
    def send(self, result):
        #Temporary
        new_result = json.dumps(result, ensure_ascii=False, indent=2, cls=DataclassJSONEncoder)
        print("Send result:", new_result)
        print("Send size: ", len(new_result))
        self.server.send(result)
    
    def receive(self):
        #Temp
        result = json.loads(self.server.receive())
        result = MonitoringResponse(ResponseType(result['type']), result['comment'])
        self.interact(result)
    
    def _notify(self, text: str):
        #Temp
        print(f'<< {text} >>')
    
    def _ask(self, text: str):
        #Temp
        res = input(f'?? {text} ??')
        return bool(res)

    def interact(self, result: MonitoringResponse):
        if result.type != ResponseType.OK:
            self._notify(result.comment)

        if result.type == ResponseType.SUSPICIOUS_PROCESS:
            r = self._ask("Do you want to kill")
            if r:
                pid = self._get_pid(result)
                self._kill_process(pid)

    def _get_pid(self, result: MonitoringResponse):
        pid_matches = re.findall(r'pid:(\d+)', result.comment)
        return (pid_matches or None) and int(pid_matches[0])
    
    def _kill_process(self, pid):
        ...
        if pid is None:
            self._notify('Nothing to kill')
        else:
            self._notify(f'!Killed in pid: {pid} {type(pid)}')
    
    def start(self):
        if not self.started:
            self.started = True
            self.run()
            #self.thread = Thread(target=self.run, daemon=True)
            #self.thread.start()
            #self.thread.join()
    
    def stop(self):
        self.started = False