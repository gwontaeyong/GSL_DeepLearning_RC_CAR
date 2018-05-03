import threading, time

class Panel_Thread(threading.Thread):
    def __init__(self):
        super(Panel_Thread, self).__init__()
        self._stop_event = threading.Event()
        self.flag = True
        print("Panel_Thread start")
        global rc_car

    def run(self):
        while self.flag:
            print("speed : ", rc_car.speed, "direct : ", rc_car.angle)
            # time.sleep(1)

    def __del__(self):
        print('판넬 종료')

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()