# Laser-amplitude-locker-PID
Developed a PID controller using Moku:Go and an Electro-Optic Modulator (EOM) to stabilize the laser output (setup shown in the picture below). The PID-control-final.py file contains the final version of the PID controller code.

In the algorithm, the proportional gain of the PID controller is designed to decrease when the error is small. I used a decay function to prevent fluctuations around the maximum value (i.e., when the error — setpoint minus actual — is zero), as implemented in error-calculation.py.

<img width="1376" height="714" alt="Screenshot 2025-07-19 193428" src="https://github.com/user-attachments/assets/c8a8b9a7-8905-46d5-99b1-aea032f1a19e" />
Result: both with 9mW Output reading
<img width="1179" height="585" alt="PID-controller" src="https://github.com/user-attachments/assets/06ca6256-d079-4daf-a1eb-6b2246157e27" />
