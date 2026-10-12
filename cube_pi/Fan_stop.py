from CubeRaspberryLib import CubeRaspberry

if __name__ ==  '__main__':
	bot = CubeRaspberry(i2c_bus=1)
	bot.set_Fan(0)