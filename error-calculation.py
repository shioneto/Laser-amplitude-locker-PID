import numpy as np
import matplotlib.pyplot as plt

kp = 0.6
threshold = 0.0015

errors = np.linspace(0, 0.004, 500)
scale = np.tanh(errors / threshold)
deltas = kp * errors * scale
linear = kp * errors

plt.figure(figsize=(8, 5))
plt.plot(errors, deltas, label='With tanh smoothing', color='blue', linewidth=2)
plt.plot(errors, linear, label='Linear (kp * error)', color='red', linestyle='--')
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
plt.title('PID Delta vs Error (0 to 0.003 V)')
plt.xlabel('Error (V)')
plt.ylabel('Delta (Control Update)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
import pandas as pd

# Load the data from the Excel file
file_path = r"C:\Users\user\OneDrive\デスクトップ\vscode\ECE122\code\research\PID-control-project\Input voltage vs Output voltage(1).xlsx"
data = pd.read_excel(file_path, sheet_name='voltage_data')

# Extract relevant columns (Input and Output)
input_voltage = data['Input']
output_voltage = data['Output']

# Create a DataFrame for easier manipulation
df = pd.DataFrame({
    'Input': input_voltage,
    'Output': output_voltage
})

# Drop rows with NaN values (if any)
df = df.dropna()

# Sort by Input voltage to ensure consecutive changes are correctly calculated
df = df.sort_values(by='Input')

# Calculate the differences in Input and Output voltages
df['Delta_Input'] = df['Input'].diff().abs()
df['Delta_Output'] = df['Output'].diff().abs()

# Filter data around the output voltage of interest (1.4V ± tolerance)
target_output = 3.5
tolerance = 0.01  # Adjust tolerance as needed
filtered_df = df[(df['Output'] >= target_output - tolerance) & 
                 (df['Output'] <= target_output + tolerance)]

# Calculate the average ratio of Delta_Output to Delta_Input in the filtered region
if not filtered_df.empty:
    avg_ratio = filtered_df['Delta_Output'].mean() / filtered_df['Delta_Input'].mean()
else:
    # Fallback: use the entire dataset if no data points are found around 1.4V
    avg_ratio = df['Delta_Output'].mean() / df['Delta_Input'].mean()

# Predict the number of input changes needed for 0.02V output differentiation
target_delta_output = 0.01
if avg_ratio != 0:
    required_delta_input = target_delta_output / avg_ratio
    # Since each input change is a step (assuming smallest delta_input is one step)
    avg_delta_input = df['Delta_Input'].mean()
    num_input_changes = required_delta_input / avg_delta_input
else:
    num_input_changes = float('inf')  # Avoid division by zero

print(f"Average ratio (Delta_Output/Delta_Input) around 1.4V: {avg_ratio:.6f}")
print(f"Required input voltage change for 0.02V output differentiation: {required_delta_input:.6f} volts")
print(f"Number of input voltage changes needed: {num_input_changes:.2f}")
