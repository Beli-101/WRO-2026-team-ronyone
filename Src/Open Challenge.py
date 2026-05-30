"""Open Challenge controller."""

from controller import Robot
import math

robot = Robot()
timestep = 1

left_steer = robot.getDevice('left_steer')
right_steer = robot.getDevice('right_steer')
front_left = robot.getDevice('frontleft')
front_right = robot.getDevice('frontright')
rear_left = robot.getDevice('rearleft')
rear_right = robot.getDevice('rearright')
color_camera = robot.getDevice("colorcamera")
imu = robot.getDevice("IMU")

distance_front = robot.getDevice("front")
distance_front_left = robot.getDevice("front_left")
distance_front_right = robot.getDevice("front_right")
distance_back_left = robot.getDevice("back_left")
distance_back_right = robot.getDevice("back_right")

first_check = 0
smjer = None
smjer_color = None

imu.enable(timestep)
color_camera.enable(timestep)
distance_front.enable(timestep)
distance_front_left.enable(timestep)
distance_front_right.enable(timestep)
distance_back_left.enable(timestep)
distance_back_right.enable(timestep)

front_left.setPosition(float("inf"))
front_right.setPosition(float("inf"))
rear_left.setPosition(float("inf"))
rear_right.setPosition(float("inf"))

front_left.setVelocity(0.0)
front_right.setVelocity(0.0)
rear_left.setVelocity(0.0)
rear_right.setVelocity(0.0)

CRUISE_SPEED = 17
TURN_SPEED = 7
MAX_TURNS = 12

_set_vel = [m.setVelocity for m in [front_left, front_right, rear_left, rear_right]]
_imu_get = imu.getRollPitchYaw
_img_r   = color_camera.imageGetRed
_img_g   = color_camera.imageGetGreen
_img_b   = color_camera.imageGetBlue
_get_img = color_camera.getImage
_CAM_W   = color_camera.getWidth()
_TO_DEG  = 180 / math.pi #radian

def set_speed(v):
    for sv in _set_vel:
        sv(v)

def steer_right(angle):
    right_steer.setPosition(angle)
    left_steer.setPosition(angle * 0.7)

def steer_left(angle):
    right_steer.setPosition(-angle * 0.7)
    left_steer.setPosition(-angle)

def straight():
    left_steer.setPosition(0.0)
    right_steer.setPosition(0.0)

def angle_diff(target, current):
    diff = target - current
    if diff > 180:  diff -= 360
    if diff < -180: diff += 360
    return diff

def trigger_turn(color, current_yaw):
    global smjer_color, first_check, turn_start_yaw, turned_so_far
    global straightening, turning, turn_count
    turn_count += 1
    print(f"Turn {turn_count}/{MAX_TURNS}")
    smjer_color = color
    first_check = 1
    turn_start_yaw = current_yaw
    turned_so_far = 0
    straightening = False
    turning = True
    if color == "blue":
        steer_left(0.7)
    else:
        steer_right(0.7)
    set_speed(TURN_SPEED)
    return True

left_steer.setPosition(0.0)
right_steer.setPosition(0.0)

turning = False
straightening = False
straight_target = None
turn_start_yaw = None
turned_so_far = 0
turn_count = 0

set_speed(CRUISE_SPEED)

while robot.step(timestep) != -1:
    yaw = (_imu_get()[2] * _TO_DEG) % 360
    print("Yaw: ", yaw)
    image = _get_img()
    r = _img_r(image, _CAM_W, 0, 0)
    g = _img_g(image, _CAM_W, 0, 0)
    b = _img_b(image, _CAM_W, 0, 0)

    if   40 < r < 80  and 50 < g < 90  and 100 < b < 150: detected = "blue"
    elif 140 < r < 200 and 70 < g < 120 and 30 < b < 80:  detected = "orange"
    else:                                                 detected = None

    # ── Phase: TURNING ───────────────────────────────────────────────────────
    if turning:
        front_distance = distance_front.getValue()
        speed = front_distance / 7

        
        diff = angle_diff(yaw, turn_start_yaw)
        if smjer_color == "blue":
            turned_so_far = diff
            front_left_distance = distance_front_left.getValue()
            #print("distance: ", front_left_distance)
            if front_left_distance < 25:
                speed += 4
        else:
            turned_so_far = -diff
            front_right_distance = distance_front_right.getValue()
            if front_right_distance < 25:
                speed += 4
            
        #print("speed: ", speed)
        set_speed(speed)
        if turned_so_far >= 87:
            turning = False
            straightening = True
            straight_target = (round(yaw / 90) * 90) % 360
            straight()
            set_speed(CRUISE_SPEED)

    # ── Phase: STRAIGHTENING ─────────────────────────────────────────────────
    elif straightening:
        heading_error = angle_diff(straight_target, yaw)

        if abs(heading_error) <= 1.5:
            straightening = False
            straight()
        else:
            if heading_error > 0:
                steer_left(0.15)
            else:
                steer_right(0.15)

        if detected == "blue" and (smjer_color is None or smjer_color == "blue"):
            if not trigger_turn("blue", yaw):
                break

        elif detected == "orange" and (smjer_color is None or smjer_color == "orange"):
            if not trigger_turn("orange", yaw):
                break

  # ── Phase: CRUISING ──────────────────────────────────────────────────────
    else:
        nearest_90 = (round(yaw / 90) * 90) % 360
        heading_error = angle_diff(nearest_90, yaw)

        if abs(heading_error) > 1.5:
            if heading_error > 0:
                steer_left(0.15)
            else:
                steer_right(0.15)
        else:
            straight()

        if detected == "blue" and (smjer_color is None or smjer_color == "blue"):
            trigger_turn("blue", yaw)
            if turn_count >= MAX_TURNS:
                # finish the turn then drive forward
                while robot.step(timestep) != -1:
                    yaw = (_imu_get()[2] * _TO_DEG) % 360
                    diff = angle_diff(yaw, turn_start_yaw)
                    turned_so_far = diff if smjer_color == "blue" else -diff
                    if turned_so_far >= 76:
                        straight()
                        break
                # drive forward to starting position
                set_speed(CRUISE_SPEED)
                for _ in range(34):  # tune this number — more steps = more distance
                    robot.step(timestep)
                set_speed(0)
                print("3 circles done, stopped at start")
                break

        elif detected == "orange" and (smjer_color is None or smjer_color == "orange"):
            trigger_turn("orange", yaw)
            if turn_count >= MAX_TURNS:
                while robot.step(timestep) != -1:
                    yaw = (_imu_get()[2] * _TO_DEG) % 360
                    diff = angle_diff(yaw, turn_start_yaw)
                    turned_so_far = diff if smjer_color == "blue" else -diff
                    if turned_so_far >= 76:
                        straight()
                        break
                set_speed(CRUISE_SPEED)
                for _ in range(34):  # tune this number
                    robot.step(timestep)
                set_speed(0)
                print("3 circles done, stopped at start")
                break
