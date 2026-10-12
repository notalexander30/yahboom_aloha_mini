#!/usr/bin/env python3
# coding=utf-8
import time
import os

import Adafruit_SSD1306 as SSD

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import smbus
import subprocess

# V1.0.1
class Yahboom_OLED:
    def __init__(self, i2c_bus=1, debug=False):
        self.__debug = debug
        self.__i2c_bus = i2c_bus
        self.__top = 0
        self.__x = 1
        self.str_Time  = 0
        self.bus = smbus.SMBus(1)
        self.hat_addr = 0x0d
        self.rgb_effect_reg = 0x04
        self.fan_reg = 0x08

        self.__total_last = 0
        self.__idle_last = 0
        self.fan_state = 2
        self.count = 0
        self.g_temp = 0
        self.g_temp1 = 0
        self.__str_CPU = "CPU:0%"

    def __del__(self):
        if self.__debug:
            print("---OLED-DEL---")

    # 初始化OLED，成功返回:True，失败返回:False
    # Initialize OLED, return True on success, False on failure
    def begin(self):
        try:
            self.__oled = SSD.SSD1306_128_32(
                rst=None, i2c_bus=self.__i2c_bus, gpio=1)
            self.__oled.begin()
            self.__oled.clear()
            self.__oled.display()
            self.__width = self.__oled.width
            self.__height = self.__oled.height
            self.__image = Image.new('1', (self.__width, self.__height))
            self.__draw = ImageDraw.Draw(self.__image)
            self.__font = ImageFont.load_default()
            if self.__debug:
                print("---OLED begin ok!---")
        except:
            if self.__debug:
                print("---OLED no found!---")

    # 清除显示。refresh=True立即刷新，refresh=False不刷新。
    # Clear the display.  Refresh =True Refresh immediately, refresh=False refresh not
    def clear(self, refresh=False):
        self.__draw.rectangle(
            (0, 0, self.__width, self.__height), outline=0, fill=0)
        if refresh:
            self.refresh()

    # 增加字符。start_x start_y表示开始的点。text是要增加的字符。
    # refresh=True立即刷新，refresh=False不刷新。
    # Add characters.  Start_x Start_y indicates the starting point.  Text is the character to be added
    # Refresh =True Refresh immediately, refresh=False refresh not
    def add_text(self, start_x, start_y, text, refresh=False):
        if start_x > 128 or start_x < 0 or start_y < 0 or start_y > 32:
            if self.__debug:
                print("oled text: x, y input error!")
            return
        x = int(start_x + self.__x)
        y = int(start_y + self.__top)
        self.__draw.text((x, y), str(text), font=ImageFont.truetype("/home/pi/RGB_Cooling_HAT/FangZhengHeiTiJianTi-1.ttf",10),fill=255)
        if refresh:
            self.refresh()

    # 写入一行字符text。refresh=True立即刷新，refresh=False不刷新。
    # line=[1, 4]
    # Write a line of character text.  Refresh =True Refresh immediately, refresh=False refresh not.
    def add_line(self, text, line=1, refresh=False):
        if line < 1 or line > 4:
            if self.__debug:
                print("oled line input error!")
            return
        y = int(8 * (line - 1))
        self.add_text(0, y, text, refresh)


    # 刷新OLED，显示内容
    # Refresh the OLED to display the content
    def refresh(self):
        self.__oled.image(self.__image)
        self.__oled.display()

    # 读取CPU占用率
    # Read the CPU usage rate
    def getCPULoadRate(self, index):
        count = 10
        if index == 0:
            f1 = os.popen("cat /proc/stat", 'r')
            stat1 = f1.readline()
            data_1 = []
            for i in range(count):
                data_1.append(int(stat1.split(' ')[i+2]))
            self.__total_last = data_1[0]+data_1[1]+data_1[2]+data_1[3] + \
                data_1[4]+data_1[5]+data_1[6]+data_1[7]+data_1[8]+data_1[9]
            self.__idle_last = data_1[3]
        elif index == 4:
            f2 = os.popen("cat /proc/stat", 'r')
            stat2 = f2.readline()
            data_2 = []
            for i in range(count):
                data_2.append(int(stat2.split(' ')[i+2]))
            total_now = data_2[0]+data_2[1]+data_2[2]+data_2[3] + \
                data_2[4]+data_2[5]+data_2[6]+data_2[7]+data_2[8]+data_2[9]
            idle_now = data_2[3]
            total = int(total_now - self.__total_last)
            idle = int(idle_now - self.__idle_last)
            usage = int(total - idle)
            usageRate = int(float(usage / total) * 100)
            self.__str_CPU = "CPU:" + str(usageRate) + "%"
            self.__total_last = 0
            self.__idle_last = 0
            # if self.__debug:
            #     print(self.__str_CPU)
        return self.__str_CPU

    # 读取系统时间
    # Read system time
    def getSystemTime(self):
        cmd = "date +%H:%M:%S"
        date_time = subprocess.check_output(cmd, shell=True)
        str_Time = str(date_time).lstrip('b\'')
        str_Time = str_Time.rstrip('\\n\'')
        # print(date_time)
        return str_Time

    # 读取内存占用率 和 总内存
    # Read the memory usage and total memory
    def getUsagedRAM(self):
        cmd = "free | awk 'NR==2{printf \"RAM:%2d%% --> %.1fGB \", 100*($2-$7)/$2, ($2/1048576.0)}'"
        FreeRam = subprocess.check_output(cmd, shell=True)
        str_FreeRam = str(FreeRam).lstrip('b\'')
        str_FreeRam = str_FreeRam.rstrip('\'')
        return str_FreeRam


    # 读取TF卡空间占用率 / TF卡总空间
    # Read the TF card space usage/TOTAL TF card space
    def getUsagedDisk(self):
        cmd = "df -h | awk '$NF==\"/\"{printf \"SDC:%s -->  %.1fGB\", $5, $2}'"
        Disk = subprocess.check_output(cmd, shell=True)
        str_Disk = str(Disk).lstrip('b\'')
        str_Disk = str_Disk.rstrip('\'')
        return str_Disk

    def setFanSpeed(self,speed):
        self.bus.write_byte_data(self.hat_addr, self.fan_reg, speed&0xff)
        
    def setRGBEffect(self,effect):
        self.bus.write_byte_data(self.hat_addr, self.rgb_effect_reg, effect&0xff)
        
    def stopRGBEffect(self):
        self.bus.write_byte_data(self.hat_addr, 0x07, 0x00)

    # 获取本机IP
    # Read the local IP address
    def getLocalIP(self):
        ip = os.popen(
            "/sbin/ifconfig eth0 | grep 'inet' | awk '{print $2}'").read()
        ip = ip[0: ip.find('\n')]
        if(ip == ''):
            ip = os.popen(
                "/sbin/ifconfig wlan0 | grep 'inet' | awk '{print $2}'").read()
            ip = ip[0: ip.find('\n')]
            if(ip == ''):
                ip = 'x.x.x.x'
        if len(ip) > 15:
            ip = 'x.x.x.x'
        return ip

    def gettemp(self):
        cmd = os.popen('vcgencmd measure_temp').readline()
        self.g_temp  = cmd.replace("temp=","Temp:").replace("'C\n","C")
        return self.g_temp
        
    def get_temp(self):
        cmd = os.popen('vcgencmd measure_temp').readline()
        self.g_temp1  = float(cmd.replace("temp=","").replace("'C\n",""))
        return self.g_temp1

    # oled主要运行函数，在while循环里调用，可实现热插拔功能。
    # Oled mainly runs functions that are called in a while loop and can be hot-pluggable
    def main_program(self):
        count1 = 0
        cpu_index = 0
        temp = 0
        temp1 = 0
        self.begin()
        while 1:
                
            self.clear()
            str_CPU = self.getCPULoadRate(cpu_index)
            str_Time = self.getSystemTime()
            temp = self.gettemp()
            temp1 = self.get_temp()
            #print(temp)
            if cpu_index == 0:
                str_FreeRAM = self.getUsagedRAM()
                str_Disk = self.getUsagedDisk()
                str_IP = "IPA -->" + self.getLocalIP()
            
            self.add_text(0, 0, str_CPU)
            self.add_text(50, 0, str(temp))
            self.add_line(str_FreeRAM, 2)
            self.add_line(str_Disk, 3)
            self.add_line(str_IP, 4)
            self.refresh()


            if temp1 >= 55:
                if self.fan_state != 1:
                    self.setFanSpeed(0x01)
                    self.fan_state = 1        
            elif temp1 <= 48:
                if self.fan_state != 0:
                    self.setFanSpeed(0x00)
                    self.fan_state = 0

            if count1 == 10:
                self.setRGBEffect(0x04)
            elif count1 == 20:
                self.setRGBEffect(0x02)
            elif count1 == 30:
                self.setRGBEffect(0x01)
            elif count1 == 40:
                self.setRGBEffect(0x03)
                count1 = 0
            count1 += 1
            time.sleep(.1)

            cpu_index = cpu_index + 1
            if cpu_index >= 5:
                cpu_index = 0
            time.sleep(.1)




if __name__ == "__main__":
    try:
        oled = Yahboom_OLED(debug=True)
        oled.setFanSpeed(0x00)
        oled.setRGBEffect(0x03)
        while True:
            oled.main_program()
            time.sleep(2)
    except KeyboardInterrupt:
        oled.clear(True)
        oled.stopRGBEffect()
        oled.setFanSpeed(0x00)
        del oled
        print(" Program closed! ")
        pass
