import argparse
import os
import sys

import pyadb.connect as connect


def loader(device_path, bytes_written, total_bytes):
    print(f">>> {bytes_written/total_bytes*100:2.2f}%")


def main():
    args = parse_args()
    
    print("Connecting")
    device = connect.tcp(args.ip)
    
    screenshot_location = '/storage/emulated/0/DCIM/screenshot.png'
    output = 'report.png'

    print("Taking screenshot")
    device.shell(f'screencap -p {screenshot_location}')
    
    print("Downloading screenshot")
    device.pull(screenshot_location, output, progress_callback=loader)
    
    print("Cleaning the room")
    device.shell(f'rm {screenshot_location}')
    
    os.system("echo Screenshot saved in %CD%")
    os.system("pause")
    
    
def parse_args():
    parser = argparse.ArgumentParser("screenshot")
    
    parser.add_argument("ip", type=str, help="Device IP")
    
    return parser.parse_args()