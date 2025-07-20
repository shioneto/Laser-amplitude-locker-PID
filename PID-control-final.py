import time
import matplotlib.pyplot as plt 
import csv
import numpy as np
from moku.instruments import Oscilloscope

i = Oscilloscope('192.168.73.1', force_connect=True)
# initial setup 
goal = 3.17500
kp = 0.00085 #proportional gain
control = 2.08701#intial voltage
threshold = 0.0015
dt = 0.4 # second per cycle
time_data = []
voltage_data = []
control_data = []
setpoint_data = []
error_data = []

try:
    def compute_pid(current_value):
        global control
        
        error = current_value - goal
        scale = np.tanh(abs(error)/ threshold)
        delta = kp*error*scale
        # delta =  kp * error 
        if (abs(error)<0.0008): delta = 0
        
        control += delta
        control = max(0, min(5, control)) # Max 5 volts 
        

        #Debug code##
        #print(f"Voltage: {current_voltage:.3f}V, Error: {error:.3f}V, Control: {control:.3f}V")
        error_data.append(abs(error))
        
        return control
    start_loop_time = time.time()
    loop_count = 0
    max_runtime = 3830 # (seconds)
    
    while (time.time() - start_loop_time) < max_runtime:
        start_time = time.time()
        
        try:
            data = i.get_data()  
            
            # Check if data is valid
            if data and 'ch1' in data and len(data['ch1']) > 0:
                current_voltage = float(data['ch1'][-1])             
                control_signal = compute_pid(current_voltage)
                i.generate_waveform(channel=1, type='Sine', amplitude=0.002,offset = control_signal, frequency=5e3)
            
                # 4. Store data for plotting
                current_time = time.time() - start_loop_time
                time_data.append(current_time); voltage_data.append(current_voltage); control_data.append(control_signal); setpoint_data.append(goal)

                # Debug 
                #print(f"Time: {current_time:.1f}s, Voltage: {current_voltage:.3f}V, Error: {(goal - current_voltage):.3f}V, Control: {control_signal:.3f}V")
            else:
                print("Warning: Invalid data received from oscilloscope")
                
        except (KeyError, IndexError, ValueError) as e:
            print(f"Warning: Data parsing error - {e}")
            
        except Exception as e:
            print(f"Warning: Unexpected error in loop - {e}")
        
        # 6. Maintain loop timing
        elapsed = time.time() - start_time
        if elapsed < dt:
            time.sleep(dt - elapsed)
        else:
            print("Warning: PID loop too slow!")
            
        loop_count += 1
    
    print(f"\nData collection complete after {time.time() - start_loop_time:.1f} seconds")

except KeyboardInterrupt:   
    print("\nLoop interrupted by user")
    
except Exception as e:
    print(f"Critical error: {e}")
    i.relinquish_ownership()
    raise e
    
finally:
    i.relinquish_ownership()

    with open('PID-data', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Control Voltage (V)', 'Output Voltage (V)', 'Setpoint (V)', 'Error (V)'])
        for t, u, y, sp, e in zip(time_data, control_data, voltage_data, setpoint_data, error_data):
            writer.writerow([t, u, y, sp, e])


    # Create matplotlib plot if we have data
    if time_data:
        plt.figure(figsize=(12, 8))
        # Plot voltage response
        plt.subplot(3, 1, 1)
        plt.plot(time_data, voltage_data, 'b-', linewidth=2, label='Actual Voltage')
        plt.plot(time_data, setpoint_data, 'r--', linewidth=2, label='Setpoint ')
        plt.ylim(0, 5)
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.title('PID Voltage Control Response')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(3, 1, 3)
        plt.plot(time_data, error_data, 'm-', linewidth=2, label='|Error|')
        plt.xlabel('Time (s)')
        plt.ylabel('Error (V)')
        plt.title('PID Error Magnitude Over Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save the plot as PNG
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"pid_voltage_control_{timestamp}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved as: {filename}")

        plt.plot(time_data, voltage_data, 'b-', linewidth=2, label='Actual Voltage')
        
        plt.show()
    else:
        print("No data collected for plotting")