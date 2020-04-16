import time


class Timer:
    def __init__(self):
        print("Timer init ...")
        self.timerIndex = {}
        self.timerUsedIndex = {}

    def start(self, key):
        self.timerIndex[key] = time.time()

    def getTime(self, key):
        return self.timerIndex[key]

    def getUsedTime(self, key):
        return self.timerUsedIndex[key]

    def stop(self, key):
        lasttime = self.timerIndex.get(key)

        if (lasttime):
            x= time.time() - lasttime
            self.timerUsedIndex[key]=x
            print(f"{key} time usage: {x} s")


if __name__ == "__main__":
    print("test timer:")
    t = Timer()
    t.start("hi")
    # time.sleep(1)
    t.stop("hi")
    print("finish")
