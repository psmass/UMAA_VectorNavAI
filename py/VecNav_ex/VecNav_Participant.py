import rti.connextdds as dds
import rti.idl as idl
from enum import IntEnum
from time import sleep
import datetime

@idl.enum
class umaa_NavigationSolutionEnum(IntEnum):
    ESTIMATED = 0
    GROUND_TRUTH = 1
    MEASURED = 2
    
@idl.enum
class VehicleSpeedModeEnumType(IntEnum):
    LRC = 0                # Low Range Cruise
    MEC = 1                # Medium Efficiency Cruise
    MRC = 2                # Maximum Range Cruise
    SLOW = 3               # Slow Speed Mode
    VEHICLE_SPECIFIC = 4   # Vehicle-Specific Mode

def main():
    # Load the XML configuration
    qos_provider = dds.QosProvider("../../data_model/VectorNavSystem.xml")

    # Create the DomainParticipant from the XML configuration
    participant = qos_provider.create_participant_from_config(
        "UMAA_DomainParticipantLibrary::VectorNavParticipant"
    )
    #while True:
    #     pass

    # Access DataWriters
    global_pose_writer = dds.DynamicData.DataWriter.find_by_name(participant, "VectorNavPublisher::GlobalPoseWriter")
    if global_pose_writer is None:
        raise RuntimeError("GlobalPoseWriter not found. Check the XML configuration.")

    speed_writer =  dds.DynamicData.DataWriter.find_by_name(participant, "VectorNavPublisher::SpeedWriter")
    if speed_writer is None:
        raise RuntimeError("GlobalPoseWriter not found. Check the XML configuration.")

    gp_altitude = 100.0
    speed = 100.0  # Start SpeedThroughAir at 100
    increment = 10  # Increment/Decrement value for SpeedThroughAir
    # Create DynamicData for GlobalPoseReportType
    topic_type = qos_provider.type(qos_provider.type_libraries[0], "GlobalPoseReportType")
    global_pose_data = dds.DynamicData(topic_type)
    global_pose_data["course"] = 1.57
    global_pose_data["navigationSolution"] = umaa_NavigationSolutionEnum.ESTIMATED

    # Set source::id and source::parentID
    global_pose_data["source.id"] = bytes([100] + [0] * 15)  # Set id to 100 (UUID is 16 bytes)
    global_pose_data["source.parentID"] = bytes([10] + [0] * 15)  # Set parentID to 10 (UUID is 16 bytes)

    # Create DynamicData for SpeedReportType
    topic_type = qos_provider.type(qos_provider.type_libraries[0], "SpeedReportType")
    speed_data = dds.DynamicData(topic_type)
    speed_data["speedOverGround"] = speed

    # Set source::id and source::parentID
    speed_data["source.id"] = bytes([100] + [0] * 15)  # Set id to 100 (UUID is 16 bytes)
    speed_data["source.parentID"] = bytes([10] + [0] * 15)  # Set parentID to 10 (UUID is 16 bytes)

    while True:
        # Get the current system time
        now = datetime.datetime.now()
        seconds = int(now.timestamp())  # Seconds since epoch
        nanoseconds = now.microsecond * 1000  # Convert microseconds to nanoseconds

        # Update the timestamp for GlobalPoseReportType
        global_pose_data["timeStamp"] = {"seconds": seconds, "nanoseconds": nanoseconds}
        global_pose_data["altitude"] = gp_altitude
        global_pose_writer.write(global_pose_data)

        # Update the timestamp for SpeedReportType
        speed_data["timeStamp"] = {"seconds": seconds, "nanoseconds": nanoseconds}
        speed_data["speedThroughAir"] = speed
        speed_writer.write(speed_data)

        # Print the updated values
        print(f"\nWriting GlobalPose & Speed Reports: Altitude={gp_altitude}, SpeedThroughAir={speed}, Timestamp={seconds}.{nanoseconds}", flush=True)

        # Increment altitude for the next iteration
        gp_altitude += 10

        # Update SpeedThroughAir: Increment or Decrement
        speed += increment
        if speed >= 400 or speed <= 100:
            increment = -increment  # Reverse direction when limits are reached

        # Sleep for 1 second before the next iteration
        sleep(1)

    print("VectorNavParticipant is set up and data has been written.")

if __name__ == "__main__":
    try:
        main()

    except RuntimeError as e:
           print(f"Runtime error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
