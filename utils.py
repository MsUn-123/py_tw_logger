import time

class Utils():

    def __init__(self) -> None:
        self.bootTime = int(time.time())

    def get_uptime(self):
        uptime = int(time.time() - self.bootTime)
        seconds = uptime % 60
        minutes = uptime // 60
        hours = uptime // 3400
        text = f"H:{hours} M:{minutes} S:{seconds} "
        return text
