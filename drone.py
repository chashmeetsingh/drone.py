import enum
import signal
import time
import threading
import os

# Directions enum
class Direction(enum.Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    FORWARD = 4
    BACKWARD = 5

# Engine status enum
class EngineStatus(enum.Enum):
    ON = 1
    OFF = 0

# engine class
class Engine:
    # initialize power and status
    def __init__(self, power = 100):
        self.power = power
        self.status = EngineStatus.OFF

        self.handle_power()

    # try to turn the engine on else throw an exception
    def on(self):
        if self.power >= 1:
            self.status = EngineStatus.ON
        else:
            raise Exception('Engine power low.')

    # switch off the engine
    def off(self):
        self.status = EngineStatus.OFF

    # method to reduce power by one unit every second (for handling power consumption)
    def handle_power(self):
        timer = threading.Timer(1.0, self.handle_power)
        timer.start()
        if self.power == 0:
            timer.cancel()
            print Exception('Engine power low.')
            return
        self.power -= 1

# gyroscope class (currently handling x,y,z coordinates)
class Gyroscope:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0      

# drone status enum
class DroneStatus(enum.Enum):
    OFF = 0
    HOVERING = 1
    MOVING = 2

# drone class
class Drone:
    # drone engine(4), status and gyroscope initializer
    def __init__(self, engines = [Engine() for i in range(4)]):
        self.engines = engines
        self.status = DroneStatus.OFF
        self.gyroscope = Gyroscope()

    # method to set the status of the drone
    def set_drone_status(self, status):
        # if turning off, first turn off all the engines
        if status == DroneStatus.OFF:
            for engine in self.engines:
                engine.off()
        self.status = status

    # method to check if the drone is operational
    def is_operational(self):
        for engine in self.engines:
            try:
                engine.on()
            except Exception as e:
                print(e)    
                return False
        return True

    # method to take off to a certain altitude
    def take_off(self, altitude):
        print('Performing checks...')

        print("Turning engines on.")
        if not self.is_operational(): return
        print('Drone lift off.')

        self.move(Direction.UP, altitude)
        print('Drone take off complete.\n')

    # assuming movement in unrestricted space
    def move(self, direction, units, not_landing = True):
        if not_landing and not self.is_operational():
            self.land()
            os._exit(1)
        
        print('Started moving...')
        self.set_drone_status(DroneStatus.MOVING)
        if direction == Direction.BACKWARD:
            self.move_backward(units)
        if direction == Direction.FORWARD:
            self.move_forward(units)
        if direction == Direction.UP:
            self.move_up(units)
        if direction == Direction.DOWN:
            self.move_down(units)
        if direction == Direction.LEFT:
            self.move_left(units)
        if direction == Direction.RIGHT:
            self.move_right(units)
        self.set_drone_status(DroneStatus.HOVERING)
        print('Moving complete...')
    
    # move forward by units
    def move_forward(self, units):
        print('move_forward.')
        while units != 0:
            time.sleep(1)
            self.gyroscope.z += 1
            units = abs(units) - 1

    #move backward by units
    def move_backward(self, units):
        print('move_backward.')
        while units != 0:
            time.sleep(1)
            self.gyroscope.z -= 1
            units = abs(units) - 1
    
    # move left by units
    def move_left(self, units):
        print('move_left.')
        while units != 0:
            time.sleep(1)
            self.gyroscope.x -= 1
            units = abs(units) - 1
    
    #move right by units
    def move_right(self, units):
        print('move_right.')
        while units != 0:
            time.sleep(1)
            self.gyroscope.x += 1
            units = abs(units) - 1

    # move up by units
    def move_up(self, units):
        print('move_up.')
        while units != 0:
            time.sleep(1)
            self.gyroscope.y += 1
            units = abs(units) - 1

    # move down by units   
    def move_down(self, units):
        print('move_down.')
        while units != 0:
            time.sleep(1)
            self.gyroscope.y -= 1
            units = abs(units) - 1

    def stabilize(self):
        print('stabilize')
        #TODO

    # prints the drone status to console
    def drone_status(self):
        print('Getting Status....................')

        print('Drone Status: %s \n' % self.status)
        for idx, engine in enumerate(self.engines):
            print('Engine %d:' % (idx+1))
            print('  Power: %d' % engine.power)
            print('  Status: %s\n' % engine.status)

        print('Gyroscope Status:')
        print('X coordinate: %d' % self.gyroscope.x)
        print('Y coordinate: %d' % self.gyroscope.y)
        print('Z coordinate: %d' % self.gyroscope.z)
        print('.................................\n\n')

    # performs drone landing
    def land(self):
        print('Landing started...')
        self.stabilize()

        # move drone only if on the coordinate system point is != 0
        if self.gyroscope.x != 0:
            self.move(Direction.LEFT, self.gyroscope.x, not_landing=False) if self.gyroscope.x >= 0 else self.move(Direction.RIGHT, self.gyroscope.x, not_landing=False) 
        
        if self.gyroscope.z != 0:
            self.move(Direction.BACKWARD, self.gyroscope.z, not_landing=False) if self.gyroscope.z >= 0 else self.move(Direction.FORWARD, self.gyroscope.z, not_landing=False) 
        
        if self.gyroscope.y != 0:
            self.move(Direction.DOWN, self.gyroscope.y, not_landing=False) if self.gyroscope.y >= 0 else self.move(Direction.UP, self.gyroscope.y, not_landing=False) 

        self.set_drone_status(DroneStatus.OFF)

# TEST 1 ===================== (assuming all engines are functional)
drone = Drone()
drone.drone_status()
drone.take_off(10)
drone.drone_status()

drone.move(Direction.UP, 5)
drone.move(Direction.LEFT, 4)
drone.move(Direction.FORWARD, 1)
drone.drone_status()
drone.land()
drone.drone_status()
os._exit(1)

#Test 2 ===================== (assuming engines have limited power)
# drone = Drone(engines=[Engine(15), Engine(10), Engine(15), Engine(15)])
# drone.drone_status()
# drone.take_off(10)
# drone.drone_status()

# drone.move(Direction.UP, 5)
# drone.drone_status()
# os._exit(1)