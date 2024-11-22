from machine import Pin, PWM, ADC
import time

# Initialize IR sensors on pins 26 and 27
ir_sensor_1 = ADC(Pin(26))
ir_sensor_2 = ADC(Pin(27))

# Define threshold values for black and white detection
threshold_black = 30000  # Threshold for detecting black
threshold_white = 30000  # Threshold for detecting white

# Define GPIO pins for H-bridge control
IN1 = Pin(10, Pin.OUT)
IN2 = Pin(11, Pin.OUT)
IN3 = Pin(12, Pin.OUT)
IN4 = Pin(13, Pin.OUT)
ENA = PWM(Pin(6))  # PWM for Motor 1
ENB = PWM(Pin(7))  # PWM for Motor 2

# Set PWM frequency for speed control
ENA.freq(1000)  # 1kHz PWM frequency
ENB.freq(1000)  # 1kHz PWM frequency

# Function to move the car forward with full power
def move_forward():
    ENA.duty_u16(65535)  # Full power
    ENB.duty_u16(65535)  # Full power
    
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.high()

# Function to turn the car left aggressively
def turn_left():
    ENA.duty_u16(65535)  # Full power on motor 1
    ENB.duty_u16(32768)  # Reduced power on motor 2
    
    IN1.low()
    IN2.high()
    IN3.high()
    IN4.low()

# Function to turn the car right aggressively
def turn_right():
    ENA.duty_u16(32768)  # Reduced power on motor 1
    ENB.duty_u16(65535)  # Full power on motor 2
    
    IN1.high()
    IN2.low()
    IN3.low()
    IN4.high()

# Function to stop the car
def stop_car():
    ENA.duty_u16(0)  # Stop motor 1
    ENB.duty_u16(0)  # Stop motor 2
    
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.low()
    print("Car stopped.")

# Main loop for line following
try:
    while True:
        # Read the sensor values
        value_1 = ir_sensor_1.read_u16() 
        value_2 = ir_sensor_2.read_u16() 
        print("Sensor 1 Value:", value_1)
        print("Sensor 2 Value:", value_2)
        
        # Determine if the sensors are on black or white
        sensor_1_black = value_1 >= threshold_black
        sensor_2_black = value_2 >= threshold_black
        
        # Line following logic
        if sensor_1_black and sensor_2_black:
            # Both sensors on black - stop the car
            stop_car()
            break
        elif sensor_1_black and not sensor_2_black:
            # Left sensor on black, right sensor on white - turn right to adjust
            turn_right()
            print("Turning right...")
        elif sensor_2_black and not sensor_1_black:
            # Right sensor on black, left sensor on white - turn left to adjust
            turn_left()
            print("Turning left...")
        else:
            # Both sensors on white - move forward
            move_forward()
            print("Moving forward...")

        # Very short delay before the next iteration for faster response
        time.sleep(0.01)  # 10ms delay

except KeyboardInterrupt:
    # Stop the car if the script is interrupted
    stop_car()
