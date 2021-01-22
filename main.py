import os, sys, time
import qwiic

# Calibration Sequence for VL53L1X Sensors

# Connect to mux
mux = qwiic.QwiicTCA9548A()
# Disable all connections for recalibration
mux.disable_all()

print("Changing address of back motor from (dec) default 41 to 85")

# Detect for I2C connection
print("Running: i2cdetect -y i")
os.system('i2cdetect -y 1')

# Scan for I2C addresses
avail_addresses = qwiic.scan()

# Disable General Call Adress
pca = qwiic.QwiicPCA9685()
pca.set_addr_bit(0,0)

# Scan for I2C addresses again
avail_addresses = qwiic.scan()

# Remove Pi Servo pHat from avail_address list
avail_addresses.remove(0x40)

# Activate back sensor and change address
mux.enable_channels(4)
ToF_rear = qwiic.QwiicVL53L1X(41)
ToF_rear.SensorInit()
ToF_rear.setI2CAddress(85)

# Activate front sensor
mux.enable_channels(3)
ToF_front = qwiic.QwiicVL53L1X(41)
TOF_front.SensorInit()

while True:
    try:
        # Start Measurements
        ToF_front.StartRanging()
        time.sleep(0.005)
        ToF_rear.StartRanging()
        time.sleep(0.005)

        # Take Measurements
        fwd_distance = ToF_front.GetDistance()
        time.sleep(0.005)
        rear_distance = ToF_rear.GetDistance()
        time.sleep(0.005)

        # Stop Measurements
        ToF_front.StopRanging()
        time.sleep(0.005)
        ToF_rear.StopRanging()

        print("Forward distance(mm) = %s    Rear Distance(mm): %s" % (fwd_distance, rear_distance))
    except Exception as e:
        print(e)
