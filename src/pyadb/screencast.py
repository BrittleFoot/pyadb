import argparse
import os

from pyadb.console import Loader
import pyadb.connect as connect

from adb_shell.adb_device import AdbDevice


class Screencast:

    def __init__(self, device):
        self.device : AdbDevice = device
        self.cast_location = "/storage/emulated/0/DCIM/screencast.mp4"

    def start(self):
        self.device.shell("content insert --uri content://settings/system --bind name:s:show_touches --bind value:i:1")
        
        print('Screen recording started')
        result = self.device.shell(
            f"screenrecord --bugreport --verbose --time-limit 60 {self.cast_location}", 
            timeout_s=None,
            read_timeout_s=None,
            transport_timeout_s=None
        )
        
        print('Screen recording result:')
        print(result)
        
    def stop(self):
        self.device.shell("pkill -2 screenrecord")
        
        print("Pulling screen records")
        self.device.pull(self.cast_location, "report/screencast.mp4", progress_callback=Loader())
        
        print("Delete record")
        self.device.shell(f'rm {self.cast_location}')


def main():
    args = parse_args()

    caster = Screencast(connect.tcp(args.ip))
    
    caster.start()
    os.system('pause')
    caster.stop()


def parse_args():
    parser = argparse.ArgumentParser("screenshot")
    
    parser.add_argument("ip", type=str, help="Device IP")
    
    return parser.parse_args()