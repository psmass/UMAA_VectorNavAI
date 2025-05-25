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


    if global_pose_reader is None:
        raise RuntimeError("GlobalPoseReader not found. Check your XML config and DataReader name.")
    if speed_reader is None:
        raise RuntimeError("SpeedReader not found. Check your XML config and DataReader name.")

    # Use DynamicData.DataReader wrapper
    global_pose_dyn_reader = dds.DynamicData.DataReader(global_pose_reader)
    speed_dyn_reader = dds.DynamicData.DataReader(speed_reader)

    # Set up WaitSets for each reader
    def make_handler(reader_name, dyn_reader):
        def handler(_):
            for sample, info in dyn_reader.take():
                if info.valid:
                    print(f"[{reader_name}] Data received: {sample}")
        return handler

    global_pose_condition = dds.StatusCondition(global_pose_dyn_reader)
    global_pose_condition.enabled_statuses = dds.StatusMask.DATA_AVAILABLE
    global_pose_condition.set_handler(make_handler("GlobalPoseReader", global_pose_dyn_reader))

    speed_condition = dds.StatusCondition(speed_dyn_reader)
    speed_condition.enabled_statuses = dds.StatusMask.DATA_AVAILABLE
    speed_condition.set_handler(make_handler("SpeedReader", speed_dyn_reader))

    waitset = dds.WaitSet()
    waitset += global_pose_condition
    waitset += speed_condition

    print("Waiting for data on GlobalPoseReader and SpeedReader...")
    try:
        while True:
            waitset.dispatch(dds.Duration(4))  # Wait up to 4 seconds
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()