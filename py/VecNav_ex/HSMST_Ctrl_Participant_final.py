import rti.connextdds as dds

def main():
    # Load the XML configuration
    qos_provider = dds.QosProvider("../../data_model/VectorNavSystem.xml")

    # Create the DomainParticipant from the XML configuration
    participant = qos_provider.create_participant_from_config(
        "UMAA_DomainParticipantLibrary::HSMSTControlParticipant"
    )

    # Access DataReaders
    global_pose_reader = dds.DynamicData.DataReader.find_by_name(participant,"HSMSTControlSubscriber::GlobalPoseReader")
    if global_pose_reader is None:
        raise RuntimeError("GlobalPoseReader not found. Check the XML configuration.")

    speed_reader = dds.DynamicData.DataReader.find_by_name(participant,"HSMSTControlSubscriber::SpeedReader")
    if speed_reader is None:
        raise RuntimeError("SpeedReader not found. Check the XML configuration.")

    # Create a WaitSet and attach conditions
    waitset = dds.WaitSet()

    # Create a ReadCondition for global_pose_reader
    global_pose_condition = dds.ReadCondition(
        global_pose_reader, dds.DataState.any_data
    )
    waitset += global_pose_condition

    # Create a ReadCondition for speed_reader
    speed_condition = dds.ReadCondition(
        speed_reader, dds.DataState.any_data
    )
    waitset += speed_condition

    print("Waiting for data...")
    while True:
        # Wait for data to become available
        active_conditions = waitset.wait(dds.Duration(10))  # Wait up to 10 seconds

        # Process data for global_pose_reader
        if global_pose_condition in active_conditions:
            for data, info in filter(lambda s: s.info.valid, global_pose_reader.take()):
                print(f"Received GlobalPose data: {data}")

        # Process data for speed_reader
        if speed_condition in active_conditions:
            for data, info in filter(lambda s: s.info.valid, speed_reader.take()):
                print(f"Received Speed data: {data}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
