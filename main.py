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

# Activate back sensor
mux.enable_channels(4)

# Initial address check before 1st change
avail_addresses = qwiic.scan()
print("Possible VL53L1X addresses")
print("Hex: ", [hex(x) for x in avail_addresses])
print("Dec: ", [int(x) for x in avail_addresses])

# Check if dec slot 85 has been taken yet, if not, run replacement
if 0x55 not in avail_addresses:
    ToF_rear = qwiic.QwiicVL53L1X(41)
    ToF_rear.SetI2CAddress(85)
else:
    ToF_rear = qwiic.QwiicVL53L1X(85)
ToF_rear.SensorInit()

# Activate front sensor
mux.enable_channels(3)
ToF_front = qwiic.QwiicVL53L1X(41)
ToF_front.SensorInit()

# Final check before looping
avail_addresses = qwiic.scan()
print("Possible VL53L1X addresses")
print("Hex: ", [hex(x) for x in avail_addresses])
print("Dec: ", [int(x) for x in avail_addresses])
os.system('i2cdetect -y 1')

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
