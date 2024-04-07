"""maze_escaper controller."""

from controller import Robot
MAX_SPEED = 6.28

def read_sensors(sensors):
    left_wall = sensors[5].getValue() > 80
    left_corner = sensors[6].getValue() > 80
    front_wall = sensors[7].getValue() > 80

    return left_wall, left_corner, front_wall

def turn_right_completely():
    left_speed = MAX_SPEED
    right_speed = -MAX_SPEED
    
    return left_speed, right_speed  

def turn_right():
    left_speed = MAX_SPEED
    right_speed = MAX_SPEED/8
    
    return left_speed, right_speed
    
def slightly_turn_left():
    left_speed = MAX_SPEED/8
    right_speed = MAX_SPEED
    
    return left_speed, right_speed
    
def get_directions(front_wall, left_wall, left_corner):

    if front_wall: # Completely turn right
        left_speed, right_speed = turn_right_completely()
    
    else:
            
        if left_wall: # Turn left slightly
            left_speed, right_speed = slightly_turn_left()
                
        else: # Turn right
            left_speed, right_speed = turn_right()
                
        if left_corner: # Turn right
            left_speed, right_speed = turn_right()
            
    return left_speed, right_speed


def escape_the_maze(robot):

    timestep = int(robot.getBasicTimeStep())
    
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0) 

    # Enable the sensors
    ps_sensors = []  
    for i in range(8):
        sensor_name = 'ps' + str(i)
        ps_sensors.append(robot.getDevice(sensor_name))
        ps_sensors[i].enable(timestep)
    
    while robot.step(timestep) != -1:
    
        # Check if the sensors detected something                        
        left_wall, left_corner, front_wall = read_sensors(ps_sensors)
         
        # Initialize the speed for both sides
        left_speed = MAX_SPEED
        right_speed = MAX_SPEED
        
        # Check the conditions and get directions
        left_speed, right_speed = get_directions(front_wall, left_wall, left_corner)
        
        # Set the new speeds
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
        
##################################################################
        
r = Robot()
escape_the_maze(r)
   