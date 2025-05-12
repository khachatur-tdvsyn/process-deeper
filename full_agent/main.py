import platform
from datetime import datetime

import agent.sensors as sensors

from agent.agent import Agent
from agent.system_info import get_system_info
from agent.settings import SEND_RATE, ENABLED_SENSORS

ALL_SENSORS = {
    'ram_info': sensors.sensor_ram_info,
    'rom_info': sensors.sensor_rom_info,
    'computer_stats': sensors.sensor_computer_stat,
    'process_stats': sensors.sensor_process_stat,
}
WORKING_SENSORS = {}

for i in ENABLED_SENSORS:
    WORKING_SENSORS[i] = ALL_SENSORS[i]

AGENT = Agent(
    WORKING_SENSORS,
    send_rate=SEND_RATE
)

def main():
    print("System Info Report")
    print(f"Generated on: {datetime.now()}")
    print(f"Platform: {platform.system()} {platform.release()}\n")

    AGENT.start()
    #k = input("Press enter to exit")
    AGENT.stop()
    
if __name__ == "__main__":
    main()