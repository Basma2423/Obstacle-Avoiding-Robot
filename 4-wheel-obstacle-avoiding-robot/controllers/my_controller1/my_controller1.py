from controller import Robot, DistanceSensor, Motor

# #Simulation step time
TIME_STEP = 64

MAX_SPEED = 6.28

# #Robot instance
robot = Robot()

ps = []
psNames = ["Rsensor", "Lsensor"]

for i in range(2):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(TIME_STEP)

front_left_motor = robot.getDevice("LFmotor")
front_right_motor = robot.getDevice("RFmotor")
rear_left_motor = robot.getDevice("LBmotor")
rear_right_motor = robot.getDevice("RBmotor")

front_right_motor.setPosition(float('inf'))
front_left_motor.setPosition(float('inf'))
rear_left_motor.setPosition(float('inf'))
rear_right_motor.setPosition(float('inf'))

front_right_motor.setVelocity(0.0)
front_left_motor.setVelocity(0.0)
rear_left_motor.setVelocity(0.0)
rear_right_motor.setVelocity(0.0)

def turn_right():
    rightSpeed = -0.8 * MAX_SPEED
    leftSpeed = 0.8 * MAX_SPEED
    return leftSpeed, rightSpeed
        
def turn_left():
     leftSpeed = -0.8 * MAX_SPEED
     rightSpeed = 0.8 * MAX_SPEED
     return leftSpeed, rightSpeed
        
def back_off():
    leftSpeed = -0.8 * MAX_SPEED
    rightSpeed = -0.8 * MAX_SPEED
    return leftSpeed, rightSpeed

    #############################################

while robot.step(TIME_STEP) != -1:

    # #read sensors outputs
    psValues = []
    for i in range(2):
        psValues.append(ps[i].getValue())

    # #detect obstacles
    right_obstacle = psValues[0] < 1000
    left_obstacle = psValues[1] < 1000

    # #initialize motor speeds at 50% of MAX_SPEED.
    left_speed = 0.8 * MAX_SPEED
    right_speed = 0.8 * MAX_SPEED

    if left_obstacle and right_obstacle:
        left_speed, right_speed = back_off()
        left_speed, right_speed = turn_right()
    elif left_obstacle:
        left_speed, right_speed = turn_right()
    elif right_obstacle:
        left_speed, right_speed = turn_left()


    # #write actuators inputs

    front_right_motor.setVelocity(right_speed)
    front_left_motor.setVelocity(left_speed)
    rear_left_motor.setVelocity(left_speed)
    rear_right_motor.setVelocity(right_speed)
    
    #############################################
