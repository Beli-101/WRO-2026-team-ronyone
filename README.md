# WRO 2026 Future Engineers -  RONYONE


## 📁 Table of Contents

- [👤👤👤 About the team](#the-team)
- [⚔️ Challenge Overview](#challenge-overview)
- [🚗 Our Robot](#our-robot)
- [ 🤸 Mobility Management](#mobility-management)
    - [ Drive](#drive)
      - [ Motor](#motor)
      - [ Wheels](#wheels)
  - [Steering](#steering)
    - [ Steering Servo Motor](#servo-motor)
  - [Assembly](#assembly)
  - [Assembled](#assembled)
   


## THE TEAM
Our team is composed of three members David Beluhan, Gabriel Martinko, Vedran Barunčić and our mentor Rondald Galić. We have a goal of becoming true engineers but more importantly critical thinkers. The team has competed in WRO 2025, in the Future Engineers category (WRO Open in Ljubljana, Slovenia) and WRO 2024 in Future Innovators (WRO Open in Brescia, Italy).

        Vedran, age 16: programming
        Gabriel, age 16: 3d design
        David, age 15: 3d design

## CHALLENGE OVERVIEW

This is the game mat which we are gonna do all the challenges on:
<img width="1316" height="764" alt="image" src="https://github.com/user-attachments/assets/6487d5d0-3245-413a-9d87-16ab59b773b3" />
OPEN CHALLENGE
For the open challenge, the robot just needs to do 3 laps around the map, and finish in the finishing zone.

OBSTACLE CHALLENGE
The obstacle challenge is a little bit more complicated. Esentially it has the same form as the open challenge, meaning that the robot still needs to do 3 laps around the map but now there are red and green pillars placed randomly on the map, if it is a red pillar the robot should go right around it, and if it is a green pillar it should go left around it. At the end of the 3 laps, the robot has a designated parking spot that you can see is colored pink, in the space the robot needs to parallel park.

## Software Development Environment

For efficiency, the software development was separated from the mechanical build. While the mechanical team worked on the physical robot, the software was developed and tested in Webots by Cyberbotics — an open source robot simulation application that provides a complete environment to model, program and simulate robots.

The first step was creating a new world in Webots, importing the WRO Future Engineers map scaled to real dimensions, and adding all track elements: pillars, parking space walls, outer walls and inner walls. This allowed full simulation testing without needing the physical robot.

The robot itself was initially built with standard differential drive, but we quickly realized there was no clean way to implement steering - only by creating speed differences between left and right wheels. This led us to rebuild the entire robot using the AckermannVehicle node, which is a dedicated module for Ackermann steering geometry. After inputting the correct physical dimensions and adding all sensors, we began testing.

### Sensors Used
| Sensor                      | Implementation                        | Purpose                            |
| --------------------------- | ------------------------------------- | ---------------------------------- |
| Camera “color sensor”       | 1×1 camera, RGB read                  | Detects blue/orange lines on track |
| Camera                      | Standard detection camera             | Detects red/green pillars on track |
| Front distance sensor       | Standard distance sensor              | Wall proximity during turns        |
| Front-left distance sensor  | Standard distance sensor              | Inner wall clearance (left turns)  |
| Front-right distance sensor | Standard distance sensor              | Inner wall clearance (right turns) |
| IMU                         | Inertial measurement unit             | Yaw tracking for turn control      |
| Front camera                | Camera (obstacle challenge)           | Pillar detection and avoidance     |
| Side sensors                | Distance sensors (obstacle challenge) | Lateral positioning                |
| Rear sensor                 | Distance sensor (obstacle challenge)  | Parking and reversing              |


Since no dedicated color sensor node exists in Webots, a camera was used with resolution set to 1×1 pixels. Each frame, the red, green and blue channel values are read directly and classified by threshold ranges.

### Open Challenge - Control Logic
The open challenge controller runs a state machine with three mutually exclusive phases: turning, straightening, and cruising.
Color Detection
The 1×1 camera captures one pixel per timestep. The RGB values are compared against tuned threshold ranges to classify the floor color:
```python
if   40 < r < 80  and 50 < g < 90  and 100 < b < 150: detected = "blue"
elif 140 < r < 200 and 70 < g < 120 and 30 < b < 80:  detected = "orange"
else:                                                   detected = None
```
Blue indicates a left turn, orange a right turn. The first detected color also sets the direction for all subsequent turns in that run.

### State Machine
Cruising is the default state. While cruising, the robot continuously compares its current IMU yaw against the nearest 90° increment and applies a small fixed steering correction if the heading error exceeds 1.5°. This prevents small angular errors from accumulating over multiple laps.
Turning is triggered when a color line is detected. The turn direction is locked to the first color seen at the start of the run. Rather than targeting an absolute yaw angle which breaks at the 270°→360° boundary, the controller measures how many degrees have been rotated since the turn started:
```python
diff = angle_diff(yaw, turn_start_yaw)
turned_so_far = diff      # blue (left)
turned_so_far = -diff     # orange (right)
```
The turn completes after 87° of rotation, leaving a small margin to account for mechanical overshoot. During the turn, speed is dynamically adjusted based on front distance sensor readings to maintain safe wall clearance.
Straightening activates immediately after a turn finishes. The controller snaps to the nearest 90° heading as a target and applies a fixed ±0.15 radian steering correction until the heading error falls within 1.5°, at which point the wheels return to center.

Each time a color line triggers a turn, a counter increments. On a square track with one line per corner, three full laps equal 12 turns. On the 12th detection, the robot completes its final turn, drives forward a fixed number of steps to return to the starting position, then stops.

The controller runs at a 2ms timestep, giving approximately 500 control loop iterations per second. This is critical for reliable color detection at speed — at higher timesteps the robot can drive past the color strip between two consecutive camera reads.

Occasional missed detection at start: At simulation startup the color sensor sometimes fails to detect the first line, causing the robot to drive straight through it. We believe this is a simulation artifact related to sensor initialization timing and expect it to be less of an issue on the physical robot cycle times. If it persists, the controller loop will be further optimized.

A demonstration video of the Open Challenge simulation in Webots can be viewed here:

[Open Challenge Simulation Video](LINK_HERE)

## OUR ROBOT
| <img src="https://i.ibb.co/DH3zMkSx/TOP.jpg" width = "300" alt="TOP" border="0">        | <img src="https://i.ibb.co/TDrsGHbn/BOTTOM.jpg" width = "300" alt="BOTTOM" border="0">            |
|----------------------------------|-------------------------------------|
| <p align="center"><b>Top</b></p> | <p align="center"><b>Bottom</b></p> |

| <img src="https://i.ibb.co/7J2pV2mQ/LEFT.jpg" width = "300" alt="LEFT" border="0">          | <img src="https://i.ibb.co/JwDLg6Xy/RIGHT.jpg" width = "300" alt="RIGHT" border="0">           |
|-----------------------------------|------------------------------------|
| <p align="center"><b>Left</b></p> | <p align="center"><b>Right</b></p> |

| <img src="https://i.ibb.co/40hCvp8/FORNT.jpg" width = "300" alt="FORNT" border="0">           | <img src="https://i.ibb.co/gLHNhjn7/BACK.jpg" width = "300" alt="BACK" border="0">         |
|------------------------------------|-----------------------------------|
| <p align="center"><b>Front</b></p> | <p align="center"><b>Back</b></p> |


# MOBILITY MANAGEMENT
We have decided to move with RWD ( Rear Wheel Drive - https://en.wikipedia.org/wiki/Rear-wheel_drive) and 4 wheel steering. We considered using a differential, but through some calculations we concluded that the speed difference on wheels would be small enough to consider. However, in this challenge, we need sharp turns, so we decided to use 4 wheel steering to help with that. 
  ## DRIVE
Considering the 4 wheel steering and RWD, we had to have one axle at which there is both steering and drive. We decided to solve that problem with a simple drive shaft (https://en.wikipedia.org/wiki/Drive_shaft). Ours looks like this: <br>
<img src="https://i.ibb.co/LXT3N4Wj/RWD.jpg" width ="500" alt="RWD" border="0"> 
<img src="https://i.ibb.co/v42KSBTy/RWD1.jpg"  width ="500" alt="RWD1" border="0"> <br>
<img src="https://i.ibb.co/kVDDbpmZ/SHAFT.jpg"  width ="500" alt="SHAFT" border="0"><br>
It consists of MULTIPLE parts: 
  1)  Wheel Shaft <br>
    <img src="https://i.ibb.co/cK3QTr6L/Wheel-shaft.jpg" alt="Wheel shaft" border="0" width = "400"><img src="https://i.ibb.co/qLV6D14g/dimensions-WHEEL.jpg" alt="dimensions-WHEEL" border="0" width = "400"> <br><br><br>
    
 2) Drive Shaft <br>
   <img src="https://i.ibb.co/yFbj3MLs/ZDRIVE.jpg" alt="ZDRIVE" border="0" width = "350"> <img src="https://i.ibb.co/Kp0vdVQw/ZDRIVE1.jpg" alt="ZDRIVE1" border="0" width = "350"> <br><br><br>
   
 3) Cube <br>
    <img src="https://i.ibb.co/N6RzhjYf/BCUBE.jpg" alt="BCUBE" border="0" width = "150"><img src="https://i.ibb.co/Y7t9SZdD/BCUBE1.jpg" alt="BCUBE1" border="0" width = "350"> <br><br><br>

Also, important is that we have two bewel gears in ratio 2:1 (wheel:motor), from which we get more speed. Considering that we have 256RPM on our motor, we will have 512RPM on the output, which results in the speed of around 9km/h after some calculations. 
Here are the gears:
<br>
<img src="https://i.ibb.co/vxqK6ckR/GEARS.jpg" alt="GEARS" border="0">
<br>
Small gear: <br>
<img src="https://i.ibb.co/FbHXYSww/MALI-GEAR.jpg" alt="MALI-GEAR" border="0">
<br><br><br>
Big gear: <br>
<img src="https://i.ibb.co/qMP9MzGg/GEAR-BIG.jpg"  alt="GEAR-BIG" border="0">

After finishing the drive shaft we added steer bearings, as we call them. WE designed them so that we can place a bought ball bearing ( THIS ONE: https://www.zjhoto.com/product-706ac-6x17x6mm-miniature-angular-contact-ball-bearing ) so that the drive shaft doesn't wobble in it's hole. They also have a little hook added on them which are used to steer. The steer bearing  looks like this: <br>
<img src="https://i.ibb.co/6Kx5W10/SB.jpg" alt="SB" border="0" width = "350"><img src="https://i.ibb.co/9HXzdT7Q/SA.jpg" alt="SA" border="0" width = "350"> <br> <br><br>

All the joints that are meant to be rotatible are 3mm in diamter, so that the M2 screw leaves enough space for rotating, but the top part od the screw and nut don't allow movement up and down. 


## MOTOR
| <img src="https://i.ibb.co/N2TFqfw3/MOTOR.jpg" alt="MOTOR" border="0" width = "300"> | **FAGM25 - 370** |
|------------------------------|------------------------------|
| **Model:** FARF - 370 - 15 370  | **Voltage:**  12V |
| **No-load Speed:** 5600 RPM | **No-load Current:** 300mA |
| **Stall Torque:** ~1.716 Ncm | **Stall Current:** 900mA |
|  [Specs](https://www.foneacc-motion.com/upload/GM25-370.pdf) | **Function:** Drives the robot |

**Why we chose it?**
- previously available to us
- sufficient torque


To hold the motor in the place, we designed this holder: <br>
<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/49feaaf2-56ce-40dc-835a-b876552e5222" />
<img src="https://i.ibb.co/JFwGzB99/Motor-HOLDER.jpg" width="500" alt="Motor-HOLDER" border="0">

  # WHEELS
  The wheels construction will go like this: on the 3d printed solid part we will mount the also 3d printed but ____ material which will grip with the board like a tire. <br> <br><br>
  **INNER SOLID REAR WHEEL**  <br>
  <img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/ed64a284-84f5-49f2-8a0a-aa9606ee626a" />

  **INNER SOLID FRONT WHEEL** <br>
  Front wheel is going to be a litlle different beacuse on the rear axle we have a bearing just before the wheel mounting so that the driveshaft and the wheel don+t wobble, but on the front axle, we don't have that so it is going to be on the wheel directly. The bearing is the same as the one on the rear axle.<br>
  <img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/9ff3bb99-2992-48de-bb26-f97a439a5bf0" /> <br>

  **OUTER RUBER PART OF THE WHEEL**
The first two parts shown are going to be solid, but that wouldn't be that great to go against the map, so we designed a outer part that is going to  be printed from the TPU material, and assembled to the inner parts. We aproximated that the friction coefficient would be around 0,8, and with that and the mass of the robot which we got from adding all the masses of components and calculating the volume of the 3d parts, multiplying by the material density, we got how much the frictin force would be, and it would be around 7,1N. That was also a comfirming factor of 2:1 ratio. <br>
<img width="300" height="auto" alt="image" src="https://github.com/user-attachments/assets/44bb38aa-01d4-48dd-abfc-861428a9cb38" />
<img src="https://i.ibb.co/kVG36SLB/OUTER-WHEEL.jpg" height = "500" alt="OUTER-WHEEL" border="0">



  

  
# STEERING
4 wheel steering means we needed an inversion so that axles dont rotate in the sam direction. If we want to go left, the front axle has to be rotated to the left, but the rear one to the right. The steering looks like this: It is located on the bottom side of our platform. <br> <br><br>
<img width="600" height="auto" alt="image" src="https://github.com/user-attachments/assets/276e3e46-2402-4e85-a217-cde5082950bf" /><br><br>
The steering consists of 4 parts: Steering gear, inverted steering gear, pivot arms and wheel holders.
So we divided the steering director in two parts: one is directly rotated by servo and the other is rotated by the first one. Looks like this:   <br><br><br>

1) Directly rotated from the servo:
<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/cd29f1ac-2637-4d43-b23f-21d6900ce462" />
<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/85b0024d-7c4f-401b-8c9d-5838327bea27" />



<BR><BR>2) Inverted steering gear - rotated by the other gear: <br><br>
<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/9e225be0-8779-4444-a28e-d81e07784279" />
<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/14c98177-caf1-4695-bd81-7167c03be7dd" /> <br>


<BR><BR>3) Pivot arm: <br><br>
<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/ffd7d335-a67a-48a8-b632-42cbbdbc6e3b" />
<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/b6f3975d-c45a-45a1-8927-2fdde67cae5b" />

<BR><BR>4) Wheel Holders: <br><br>
<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/06c7255b-267a-461f-8961-04fc03054cb5" />
<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/ea1b5dd9-99b8-42d0-ab26-b73b7d1888d5" />






# SERVO MOTOR
## MOTOR
|<img width="300" height="auto" alt="image" src="https://github.com/user-attachments/assets/a81f5302-c946-4d12-b62a-5a5955a231b1" />| **80KG servo** |
|------------------------------|------------------------------|
| **Model:** SCX61  | **Voltage:**  6V|
| **Idle current:** 3mA | **Signal type:** PWM |
| **Stall current:** ~2.4A | **Torque:** 12.1kg-cm |
|  [Specs](https://www.aliexpress.com/item/1005008753027913.html?spm=a2g0o.productlist.main.5.67492a2fYgEdzw&algo_pvid=1e3a1e3d-7f7b-4d29-bfff-c69b5cfc5ad3&pdp_ext_f=%7B%22order%22%3A%2226%22%2C%22spu_best_type%22%3A%22price%22%2C%22eval%22%3A%221%22%2C%22fromPage%22%3A%22search%22%7D&utparam-url=scene%3Asearch%7Cquery_from%3A%7Cx_object_id%3A1005008753027913%7C_p_origin_prod%3A) | **Function:** Steers |

**Why we chose it?**
- previously available to us
- reliable
- more than strong enough

CABLE MANAGMENT

At WRO 2025, our cable management system was a disaster, so this year we decided to take the situation seriously. We built custom component holders in which we built holes and tunnels specifically for the wires. Some of our holders have multiple holes so we can chose in what direction will wires go after the robot is put together.

TOF SENSOR HOLDERS

slika i shema bočnog redo redo

FRONT SENSOR HOLDER

slika

REAR SENSOR HOLDER

slika

## Assembly

Both the drive and steering system, are pinned up up to the chasis using holders using M2 screws and bolts. 
The chasis looks like this: <br>

<img width="889" height="513" alt="image" src="https://github.com/user-attachments/assets/fb6e236f-05c9-4d1f-bc84-179bdb9aa9e7" /><br><br><br>

The connectors look like this: <br>
THE FRONT ONE: <br>

<img width="400" height="auto" alt="image" src="https://github.com/user-attachments/assets/7a2fa6f4-469e-48a5-b245-9096b4d34808" /><img width="400" height="auto" alt="image" src="https://github.com/user-attachments/assets/390a6180-dac5-4d56-bafe-66d271f32d36" /> <br><br>

THE REAR ONE: <br>

This one had to be different because of the big gear which would get in the way. <br> 

<img width="450" height="350" alt="image" src="https://github.com/user-attachments/assets/b3d4533c-e1ed-4fa5-b4d4-a8b27e9cd697" />
<img src="https://i.ibb.co/WN5BjLx1/HOLDER-REAR.jpg" width="400" alt="HOLDER-REAR" border="0">


And here is everything:
<img width="1024" height="685" alt="image" src="https://github.com/user-attachments/assets/390c21df-760b-4726-8e19-6f2d212bcc62" />




## Assembled
        pictures of robot really connected




 

