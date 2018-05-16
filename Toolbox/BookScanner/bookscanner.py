#!/usr/bin/env python3
# coding : utf-8

import gphoto2 as gp
import argparse
import subprocess
import os
from threadutils import run_async
import time
import cv2
import numpy as np


def get_bool(prompt):
    while True:
        try:
            return {"true": True, "false": False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input please enter True or False!")


class Scanner():
    def __init__(self, book, page):
        self.scanning = True
        self.camera_list = []
        self.book = book
        self.page = page
        self.current_page = self.page

    def key_event(self, key):
        if key != -1:
            print(key)
            if key == 99:  # c
                thread_list = self.scan()
                print("before sleep")
                time.sleep(3)
                print("after sleep")
            elif key == 114: #r
                if get_bool("rescan ?"):
                    self.current_page -= len(self.camera_list)
                    self.scan()
                else:
                    pass

            elif key == 113 or key == 27 :  # q escape
                self.scanning = False

    def scan(self):
        thread_list = []
        print(self.camera_list)
        for camera in self.camera_list:
            print(camera["name"])

            thread = self.capture(camera)
            thread_list.append(thread)

            # subprocess.call(['xdg-open', target])
            # gp.check_result(gp.gp_camera_exit(camera))
        self.current_page += len(self.camera_list)
        return thread_list

    @run_async
    def capture(self, cam):
        file_path = gp.check_result(gp.gp_camera_capture(
            cam["gp"], gp.GP_CAPTURE_IMAGE))

        if cam["right"]:
            num_page = self.current_page + 1
            current_name = "L"+str(num_page)
        else:
            num_page = self.current_page + 2
            current_name = "R"+str(num_page)
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = self.book + "/" + current_name
        print('Copying image to', target)
        try:
            camera_file = gp.check_result(
                gp.gp_camera_file_get(cam["gp"], file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
        except gp.GPhoto2Error:
            print("nooonnn!  : ", file_path.folder, file_path.name)
        gp.check_result(gp.gp_file_save(camera_file, target))
        # time.sleep(1)
        # img = cv2.imread(target)
        # cv2.imshow(cam["name"], img)
        # current_image = file_path

    def start(self):
        right = True
        autodetected = gp.check_result(gp.gp_camera_autodetect())
        for i, cam in enumerate(autodetected):
            name, addr = cam
            if i == 0:
                right = get_bool(name + " connect in " + addr + " is Right cam ? (show left page) ")
            else:
                right = not self.camera_list[i-1]["right"]
            # camera_list.append((name, addr))camera = gp.Camera()
            # search ports for camera port name
            camera = gp.Camera()
            port_info_list = gp.PortInfoList()
            port_info_list.load()
            idx = port_info_list.lookup_path(addr)
            camera.set_port_info(port_info_list[idx])
            camera.init()
            self.camera_list.append({"gp":camera, "name":name, "right":right})

        if not self.camera_list:
            print('No camera detected')
        else:
            canvas = np.zeros((512, 512, 3), np.uint8)
            while self.scanning:
                cv2.imshow('canvas', canvas)
                self.key_event(cv2.waitKey(100))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--page", default=0, help="number of the first page scanned")
    parser.add_argument("-b", "--book", help="book name for output folder name")
    args = parser.parse_args()

    subprocess.call(["mkdir", "-p", args.book])

    scanner = Scanner(args.book, int(args.page))
    # scanner.scan_num = int(args.page)
    scanner.start()
