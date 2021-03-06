import argparse
import os
import sys

from pathlib import Path
from pyadb.console import Loader
import pyadb.connect as connect


def main():
    args = parse_args()
    
    print("Connecting")
    device = connect.tcp(args.ip)
    
    screenshot_location = '/storage/emulated/0/DCIM/screenshot.png'
    
    report_dir = Path('report')
    report_dir.mkdir(exist_ok=True)
    
    output = report_dir / 'screenshot.png'

    print("Taking screenshot")
    device.shell(f'screencap -p {screenshot_location}')
    
    print("Downloading screenshot")
    device.pull(screenshot_location, output, progress_callback=Loader())
    
    print("Cleaning the room")
    device.shell(f'rm {screenshot_location}')
    
    os.system("echo Screenshot saved in %CD%")
    os.system("pause")
    
    
def parse_args():
    parser = argparse.ArgumentParser("screenshot")
    
    parser.add_argument("ip", type=str, help="Device IP")
    
    return parser.parse_args()