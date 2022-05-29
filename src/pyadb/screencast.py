import argparse
import asyncio
import logging
import os
import platform

from pyadb.console import Loader
import pyadb.connect as connect
import pyadb.shell as shell_cmd

from adb_shell.adb_device import AdbDevice


logging.basicConfig(level=logging.INFO)


class ThreadPoolAdbDevice:

    def __init__(self, device: AdbDevice):
        self._device: AdbDevice = device

    async def shell(self, command, timeout=None):
        return await asyncio.to_thread(
            self._device.shell,
            command,
            timeout_s=timeout,
            read_timeout_s=30,
            transport_timeout_s=timeout
        )

    async def pull(self, device_path, local_path, progress_callback=None):
        return await asyncio.to_thread(
            self._device.pull,
            device_path,
            local_path,
            progress_callback=progress_callback
        )


class Screencast:

    def __init__(self, device: AdbDevice, backup_device: AdbDevice):
        self.device: ThreadPoolAdbDevice = ThreadPoolAdbDevice(device)
        self.backup_device: ThreadPoolAdbDevice = ThreadPoolAdbDevice(backup_device)
        self.cast_location = "/storage/emulated/0/DCIM/screencast.mp4"

    async def preconfigure(self):
        logging.debug('Show touches')
        await self.device.shell(shell_cmd.show_touches())

    async def start(self):
        logging.debug('Screen recording started')
        return await self.device.shell(shell_cmd.screenrecord(self.cast_location, 20))

    async def stop(self):
        logging.debug('Killing screenrecord')
        # Use backup device because AdbDevice cannot use one to execute two commands in parallel
        await self.backup_device.shell("pkill -2 screenrecord")

    async def pull(self):
        logging.debug("Pulling screen records")
        await self.device.pull(self.cast_location, "report/screencast.mp4", Loader())

    async def cleanup(self):
        logging.debug("Cleaning up")
        await self.device.shell(shell_cmd.hide_touches())
        await self.device.shell(f'rm {self.cast_location}')


async def _main():
    args = parse_args()

    logging.info("Connecting")
    caster = Screencast(connect.tcp(args.ip), connect.tcp(args.ip))

    await caster.preconfigure()
    
    logging.info("Start recording")
    start = asyncio.create_task(caster.start())

    # insert your controlling code here
    print("Wait for 3 seconds")
    await asyncio.sleep(3)

    logging.info("Stop recording")
    await caster.stop()

    cleanup = asyncio.create_task(caster.cleanup())
    logging.info(await start)
    await cleanup


def parse_args():
    parser = argparse.ArgumentParser("screenshot")
    parser.add_argument("ip", type=str, help="Device IP")
    return parser.parse_args()


def main():
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(_main())


if __name__ == '__main__':
    main()
