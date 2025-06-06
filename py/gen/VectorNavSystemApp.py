#!/bin/env python 

# VectorNavSystemApp.py
# A generated example that uses XML Application Creation with 
# Dynamic Data.
#
# This code is automatically generated by RTI System Designer.
# Any change will be overwritten if the file is re-generated.

import argparse
import random
import string
import time
import sys
from dataclasses import dataclass

import rti.connextdds as dds

XML_FILENAME = "VectorNavSystemApp.xml"

# Sets values to the members of GlobalPoseReportType.
# Returns false in case of error (the error message is logged to stderr)
def GlobalPoseReportType_setter(sample, count, max_keys):
    key_count = count % max_keys # Limit the number of keys
    # TODO: set values for member altitude (MSLAltitude)
    # TODO: set values for member altitudeAGL (DistanceAGL)
    # TODO: set values for member altitudeASF (DistanceASF)
    # TODO: set values for member altitudeGeodetic (GeodeticAltitude)
    # TODO: set values for member attitude (Orientation3DNEDType)
    # TODO: set values for member attitudeCovariance (CovarianceOrientationNEDType)
    # TODO: set values for member course (CourseTrueNorth)
    # TODO: set values for member depth (DistanceBSL)
    # TODO: set values for member navigationSolution (NavigationSolutionEnumType)
    # TODO: set values for member position (GeoPosition2D)
    # TODO: set values for member positionCovariance (CovariancePositionNEDType)
    # TODO: set values for member timeStamp (DateTime)
    # TODO: set values for member source (IdentifierType)
# Sets values to the members of SpeedReportType.
# Returns false in case of error (the error message is logged to stderr)
def SpeedReportType_setter(sample, count, max_keys):
    key_count = count % max_keys # Limit the number of keys
    # TODO: set values for member mode (VehicleSpeedModeEnumType)
    # TODO: set values for member speedOverGround (GroundSpeed)
    # TODO: set values for member speedThroughAir (IndicatedAirspeed)
    # TODO: set values for member speedThroughWater (SpeedLocalWaterMass)
    # TODO: set values for member timeStamp (DateTime)
    # TODO: set values for member source (IdentifierType)


# App
# ----------------------------------------------------------------------------
# The main application containing all the DDS Entities. 
class App(dds.NoOpDomainParticipantListener):
    def __init__(self, xml_filename, participant_name):
        super().__init__()
        self._qos_provider = dds.QosProvider(xml_filename)
        self._participant  = self._qos_provider.create_participant_from_config(participant_name)
        self._participant.set_listener(self, dds.StatusMask.ALL & dds.StatusMask.flip(dds.StatusMask.DATA_ON_READERS))

        # DataWriter(s):

        self._global_pose_writer_dw = dds.DynamicData.DataWriter(self._participant.find_datawriter("VectorNavPublisher::GlobalPoseWriter"))
        self._global_pose_writer_dw_data = self._global_pose_writer_dw.create_data()

        self._speed_writer_dw = dds.DynamicData.DataWriter(self._participant.find_datawriter("VectorNavPublisher::SpeedWriter"))
        self._speed_writer_dw_data = self._speed_writer_dw.create_data()


    # Write one sample and return immediately.
    # Depending on the QoS, this method may block (if the write queue is full)
    def write_global_pose_writer_dw(self, count, max_keys):
        print(f"[VectorNavPublisher::GlobalPoseWriter] Writing sample #{count} for topic SpeedStatus...")
        GlobalPoseReportType_setter(self._global_pose_writer_dw_data, count, max_keys)
        self._global_pose_writer_dw.write(self._global_pose_writer_dw_data)
    # Write one sample and return immediately.
    # Depending on the QoS, this method may block (if the write queue is full)
    def write_speed_writer_dw(self, count, max_keys):
        print(f"[VectorNavPublisher::SpeedWriter] Writing sample #{count} for topic GlobalPoseStatus...")
        SpeedReportType_setter(self._speed_writer_dw_data, count, max_keys)
        self._speed_writer_dw.write(self._speed_writer_dw_data)



    # Runs the main application spin loop. Returns the process exit code.
    def run(self, period_microsec, max_iterations, max_keys):
        print("Application is starting. Press CTRL+C to stop")
        count = 0
        speed = 100
        increment = 10
        while ((max_iterations == -1) or (count < max_iterations)):
            print(f"Running iteration #{count}, SpeedThroughAir={speed}")
            # Set SpeedThroughAir in your DynamicData sample
            self._speed_writer_dw_data["speedThroughAir"] = speed
            self.write_global_pose_writer_dw(count, max_keys)
            self.write_speed_writer_dw(count, max_keys)
            count += 1
            speed += increment
            if speed <= 100 or speed >= 400:
                increment = -increment
            time.sleep(period_microsec / 1_000_000)
 
    # Default implementation of DataReaderListener callbacks unless overwritten
    def on_requested_deadline_missed(self, reader, status):
        print(f"on_requested_deadline_missed: topic=#{reader.topic_name}")

    def on_requested_incompatible_qos(self, reader, status):
        print(f"on_requested_incompatible_qos: topic=#{reader.topic_name}")

    def on_sample_rejected(self, reader, status):
        print(f"on_sample_rejected: topic=#{reader.topic_name}")

    def on_liveliness_changed(self, reader, status):
        print(f"on_liveliness_changed: topic=#{reader.topic_name}")

    def on_sample_lost(self, reader, status):
        print(f"on_sample_lost: topic=#{reader.topic_name}")

    def on_subscription_matched(self, reader, status):
        print(f"on_subscription_matched: topic=#{reader.topic_name}")
    # End of Default DataReaderListener callbacks

    # Default DataWriterListener callbacks
    def on_offered_deadline_missed(self, writer, status):
        print(f"on_offered_deadline_missed: topic=#{writer.topic_name}")

    def on_liveliness_lost(self, writer, status):
        print(f"on_liveliness_lost: topic=#{writer.topic_name}")
    
    def on_offered_incompatible_qos(self, writer, status):
        print(f"on_offered_incompatible_qos: topic=#{writer.topic_name}")

    def on_publication_matched(self, writer, status):
        print(f"on_publication_matched: topic=#{writer.topic_name}, match count=#{status.current_count}")


# A data class to store the parsed command line arguments
# -----------------------------------------------------------------------------
@dataclass
class ApplicationArguments:
    loop_period_msec = 1000
    max_iterations = -1
    max_key_count = 10

# parse_arguments
# -----------------------------------------------------------------------------
# parses the command line arguments and returns an ApplicationArguments object
def parse_arguments():
    parser = argparse.ArgumentParser(description='VectorNavSystemApp Connext DDS Application')
    parser.add_argument(
        '-l',
        '--loop_period_msec',
        type=int,
        help='Number of milliseconds to wait in main spin loop')
    parser.add_argument(
        '-i',
        '--max_iterations',
        type=int,
        help='Number iterations to perform before terminating (-1=unlimited)')
    parser.add_argument(
        '-k',
        '--max_key_count',
        type=int,
        help='Number keys to use when publishing data')
    return parser.parse_args(namespace=ApplicationArguments)


# Main entry point
# -----------------------------------------------------------------------------
def main():
    args: ApplicationArguments = parse_arguments()
    try:
        app = App(XML_FILENAME, "UMAA_DomainParticipantLibrary::UMAA_DomainParticipantLibrary::VectorNavParticipant")
        app.run(args.loop_period_msec*1000, args.max_iterations, args.max_key_count)

    except KeyboardInterrupt:
        print("Shutting down...")

# Main
if __name__ == '__main__':
    main()



