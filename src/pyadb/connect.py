import os

from os.path import join

from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner


USERPROFILE = os.environ['USERPROFILE']
ADB_KEY_DEFAULT_PATH = join(USERPROFILE, '.android', 'adbkey')


def __read_key(keypath=ADB_KEY_DEFAULT_PATH):
    with open(keypath) as privfd, open(keypath + '.pub') as pubfd:
        priv = privfd.read()
        pub = pubfd.read()
    
    return PythonRSASigner(pub, priv)


def tcp(ip: str) -> AdbDeviceTcp:
    device = AdbDeviceTcp(ip, 5555)
    device.connect([__read_key()])
    return device


def usb():
    device = AdbDeviceUsb()
    device.connect(rsa_keys=[__read_key()], auth_timeout_s=0.1)
    return device