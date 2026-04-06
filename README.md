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
   


## THE TEAM
Our team is composed of three members David Beluhan, Gabriel Martinko, Vedran Barunčić and our mentour Rondald Galić. We have a goal of becoming true engineers but more importantly critical thinkers. Team has competed in WRO 2025, category future engineers (WRO Open in Ljubljana, Slovenia) and WRO 2024 Category future inovators (WRO Open in Brescia, Italia).
## CHALLENGE OVERVIEW
    DAVID
## OUR ROBOT
| <img src="https://i.ibb.co/xqgqfV8L/TOP.jpg" width="300">         | <img src="https://i.ibb.co/yn2XmPpn/bottom.jpg" width="300">            |
|----------------------------------|-------------------------------------|
| <p align="center"><b>Top</b></p> | <p align="center"><b>Bottom</b></p> |

| <img src="https://i.ibb.co/qMhD2QHf/LEFT.jpg" width="300">          | <img src="https://i.ibb.co/21rjMJ7L/RIGHT.jpg" width="300">           |
|-----------------------------------|------------------------------------|
| <p align="center"><b>Left</b></p> | <p align="center"><b>Right</b></p> |

| <img src="https://i.ibb.co/zVz5sxQn/FRONT.jpg" width="300">           | <img src="https://i.ibb.co/hRNtB6P6/BACK.jpg" width="300">          |
|------------------------------------|-----------------------------------|
| <p align="center"><b>Front</b></p> | <p align="center"><b>Back</b></p> |


# MOBILITY MANAGEMENT
We have decided to move with RWD ( Rear Wheel Drive - https://en.wikipedia.org/wiki/Rear-wheel_drive) and 4 wheel steering. We considered using a differential, but through some calculations we concluded that the speed difference on wheels would be small enough to consider. However, in this challenge, we need sharp turns, so we decided to use 4 wheel steering to help with that. 
  ## DRIVE
Considering the 4 wheel steering and RWD, we had to have one axle at which there is both steering and drive. We decided to solve that problem with a simple drive shaft (https://en.wikipedia.org/wiki/Drive_shaft). Ours looks like this: <br>
<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/58afc38e-6018-4a47-986e-a928010394e5" /> <br>
It consists of three parts: 
  1)  Wheel Shaft <br>
    <img src="https://i.ibb.co/cK3QTr6L/Wheel-shaft.jpg" alt="Wheel shaft" border="0" width = "400"><img src="https://i.ibb.co/qLV6D14g/dimensions-WHEEL.jpg" alt="dimensions-WHEEL" border="0" width = "400"> <br><br><br>
    
 2) Drive Shaft <br>
   <img src="https://i.ibb.co/yFbj3MLs/ZDRIVE.jpg" alt="ZDRIVE" border="0" width = "350"> <img src="https://i.ibb.co/Kp0vdVQw/ZDRIVE1.jpg" alt="ZDRIVE1" border="0" width = "350"> <br><br><br>
   
 3) Cube <br>
    <img src="https://i.ibb.co/N6RzhjYf/BCUBE.jpg" alt="BCUBE" border="0" width = "150"><img src="https://i.ibb.co/Y7t9SZdD/BCUBE1.jpg" alt="BCUBE1" border="0" width = "350"> <br><br><br>

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

  # WHEELS
  The wheels construction will go like this: on the 3d printed solid part we will mount the also 3d printed but ____ material which will grip with the board like a tire. <br> <br><br>
  **REAR WHEEL**  <br>
  <img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/ed64a284-84f5-49f2-8a0a-aa9606ee626a" />

  **FRONT WHEEL** <br>
  Front wheel is going to be a litlle different beacuse on the rear axle we have a bearing just before the wheel mounting so that the driveshaft and the wheel don+t wobble, but on the front axle, we don't have that so it is going to be on the wheel directly. The bearing is the same as the one on the rear axle.<br>
  <img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/9ff3bb99-2992-48de-bb26-f97a439a5bf0" /> <br>

  

  
# STEERING
4 wheel steering means we needed an inversion so that axles dont rotate in the sam direction. If we want to go left, the front axle has to be rotated to the left, but the rear one to the right. <br> <br><br>
<img width="211" height="239" alt="image" src="https://github.com/user-attachments/assets/704e4da2-3cc6-464a-9c23-45412d262ccc" /> <br><br>
So we divided the steering director in two parts: one is directly rotated by servo and the other is rotated by the first one. Looks like this:   <br><br><br>
<img width="auto" height="400" alt="image" src="https://github.com/user-attachments/assets/52fd59a3-9922-47e7-bf1f-5ceae020cab0" /><br><br>

<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/eb31abc1-52cb-40bd-b318-4898f92b25d3" /><img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/0d65e26b-cdd5-498c-ac57-4efdd1682714" />  <br><br><br>


# SERVO MOTOR
## MOTOR
| <img src="https://i.ibb.co/N2TFqfw3/MOTOR.jpg" alt="MOTOR" border="0" width = "300"> | **FAGM25 - 370** |
|------------------------------|------------------------------|
| **Model:** FARF - 370 - 15 370  | **Voltage:**  12V |
| **No-load Speed:** 5600 RPM | **No-load Current:** 300mA |
| **Stall Torque:** ~1.716 Ncm | **Stall Current:** 900mA |
|  [Specs](https://www.foneacc-motion.com/upload/GM25-370.pdf) | **Function:** Drives the robot |
