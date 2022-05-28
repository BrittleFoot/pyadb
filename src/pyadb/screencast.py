import argparse
import os

from pyadb.console import loader
import pyadb.connect as connect

from adb_shell.adb_device import AdbDevice


class Screencast:

    def __init__(self, device):
        self.device : AdbDevice = device
        self.cast_location = "/storage/emulated/0/DCIM/screencast.mp4"

    def start(self):
        self.device.shell("content insert --uri content://settings/system --bind name:s:show_touches --bind value:i:1")
        self.device.shell("screenrecord --bugreport --verbose {self.cast_location}", transport_timeout_s=None)
        
    def stop(self):
        self.device.shell("pkill -2 screenrecord")
        self.device.pull(self.cast_location, "report/screencast.mp4", progress_callback=loader)
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