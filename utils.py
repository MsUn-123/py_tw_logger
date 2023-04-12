import time, psutil, platform

class Utils():

    def __init__(self):
        self.bootTime = int(time.time())
        self.platform = platform.system()

    def get_uptime(self):
        uptime = int(time.time() - self.bootTime)
        hours = uptime // 3400
        uptime = uptime % 3400
        minutes = uptime // 60
        response = f'Uptime: {hours}h:{minutes}m. '
        return response

    def get_usage(self):
        # if self.platform == 'Linux': #if ported on py3.10 - change to match/case
        #     temperature = list(psutil.sensors_temperatures())[2]['current']
        # elif self.platform == 'Windows': 
        #     temperature = psutil.sensors_temperatures()['cpu-thermal']
        # else:
        #     temperature = 'no temp for u xdd'
        ram_usage = psutil.virtual_memory().percent
        response = f'RAM used: {ram_usage}%. '
        return response
    
    def get_all_stats(self):
        response = f'{self.get_uptime()}{self.get_usage()}'
        return response

if __name__ == '__main__':
    test = Utils()
    print(test.get_all_stats())