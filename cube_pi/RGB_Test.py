import time
from CubeRaspberryLib import CubeRaspberry 

if __name__ ==  '__main__':
    bot = CubeRaspberry (i2c_bus=1)
    while True:
        bot.set_RGB_Effect(0) # 关闭特效5秒 Turn off the effect for 5 seconds
        time.sleep(5)
        bot.set_RGB_Effect(1) # 单色呼吸灯5秒 Monochromatic breathing lamp for 5 sec
        time.sleep(5)
        bot.set_RGB_Effect(2) # 跑马灯5秒 Marquee for 5 seconds
        time.sleep(5)
        bot.set_RGB_Effect(3) # 彩虹灯5秒 Rainbow lights for 5 seconds
        time.sleep(5)
        bot.set_RGB_Effect(4) # 炫彩灯5秒 Dazzle lights for 5 seconds
        time.sleep(5)
        bot.set_RGB_Effect(5) # 流水灯5秒 Running water lamp for 5 seconds
        time.sleep(5)
        bot.set_RGB_Effect(6) # 循环呼吸灯5秒 Circulate the lamp for 5 sec
        time.sleep(5)