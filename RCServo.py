import sys
import time 
from Phidget22.Devices.RCServo import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

try:
    from PhidgetHelperFunctions import *
except ImportError:
    sys.stderr.write("\nCould not find PhidgetHelperFunctions. Either add PhdiegtHelperFunctions.py to your project folder "
                      "or remove the import from your project.")
    sys.stderr.write("\nPress ENTER to end program.")
    readin = sys.stdin.readline()
    sys.exit()

'''
* Sets the RCServo Target Position and Engages the motor
* Displays info about the attached Phidget channel.  
* Fired when a Phidget channel with onAttachHandler registered attaches
*
* @param self The Phidget channel that fired the attach event
'''
def onAttachHandler(self):
    
    ph = self

    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
        print("\nAttach Event:")
        
        """
        * Get device information and display it.
        """
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel:  " + str(channel) + "\n")
    
        """
        * Set a TargetPosition inside of the attach handler to initialize the servo's starting position.
        * TargetPosition defines position the RC Servo will move to.
        * TargetPosition can be set to any value from MinPosition to MaxPosition.
        """
        print("\tSetting Target Position to 90")
        try:
            ph.setTargetPosition(90)
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Setting TargetPosition: \n\t")
            DisplayError(e)
            return
            
        """
        * Engage the RCServo inside of the attach handler to allow the servo to move to its target position
        * The servo will only track a target position if it is engaged.
        * Engaged can be set to True to enable the servo, or False to disable it.
        """
        print("\tSetting Engaged")
        try:
            ph.setEngaged(True)
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Setting Engaged: \n\t")
            DisplayError(e)
            return
        
    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Displays info about the detached Phidget channel.
* Fired when a Phidget channel with onDetachHandler registered detaches
*
* @param self The Phidget channel that fired the attach event
"""
def onDetachHandler(self):

    ph = self

    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
        print("\nDetach Event:")
        
        """
        * Get device information and display it.
        """
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel:  " + str(channel) + "\n")
        
    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Writes Phidget error info to stderr.
* Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
*
* @param self The Phidget channel that fired the attach event
* @param errorCode the code associated with the error of enum type ph.ErrorEventCode
* @param errorString string containing the description of the error fired
"""
def onErrorHandler(self, errorCode, errorString):

    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

"""
* Indicated the RCServo has reached its target position
* Fired when an RCServo channel with onTargetPositionReachedHandler registered has reached its target position
*
* @param self The RCServo channel that fired the TargetPositionReached event
* @param position The reported position from the RCServo channel
"""
def onTargetPositionReachedHandler(self, position):

    #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
    #www.phidgets.com/docs/Using_Multiple_Phidgets for information

    print("[Target Pos Reached Event] -> Position: " + str(position))
    
"""
* Prints descriptions of how events related to this class work
"""
def PrintEventDescriptions():

    print("\n--------------------\n"
        "\n  | Target Position Reached events will call their associated function every time the RCServo controller has reached its target position.\n"
        "  | Press ENTER once you have read this message.")
    readin = sys.stdin.readline(1)
    
    print("\n--------------------")
            
"""
* Creates, configures, and opens a RCServo channel.
* Provides interface for controlling TargetPosition of the RCServo.
* Closes out RCServo channel
*
* @return 0 if the program exits successfully, 1 if it exits with errors.
"""
def main():

                chY = RCServo()
                chX = RCServo()
                chY.setDeviceSerialNumber(492965)
                chX.setDeviceSerialNumber(492965)
                chY.setChannel(1)
                chX.setChannel(0)
                print("\n--------------------------------------")
                print("\nSetting OnAttachHandler...")
                chY.setOnAttachHandler(onAttachHandler)
                chX.setOnAttachHandler(onAttachHandler)
        
                print("Setting OnDetachHandler...")
                chY.setOnDetachHandler(onDetachHandler)
                chX.setOnDetachHandler(onDetachHandler)

                print("Setting OnErrorHandler...")
                chY.setOnErrorHandler(onErrorHandler)
                chX.setOnErrorHandler(onErrorHandler)

                print("\nSetting OnTargetPositionReachedHandler...")
                chY.setOnTargetPositionReachedHandler(onTargetPositionReachedHandler)
                chX.setOnTargetPositionReachedHandler(onTargetPositionReachedHandler)

                print("\nOpening and Waiting for Attachment...")

                try:
                        chY.openWaitForAttachment(5000)
                        chX.openWaitForAttachment(5000)
                except PhidgetException as e:
                        PrintOpenErrorMessage(e, chX)
                        PrintOpenErrorMessage(e, chY)
                        raise EndProgramSignal("Program Terminated: Open Failed")

                print("--------------------\n"
                "\n  | RC Servo position can be controlled by setting its Target Position.\n"
                "  | By default, the target  can be a number from 0.0 to 180.0, though this can be changed by setting MinPosition and MaxPosition.\n"
                "  | For this example, acceleration has been fixed to 1.0Hz, but can be changed in custom code.\n"
    
                "\nInput a desired position between 0.0 and 180.0 and press ENTER"
                "\nIf your servo doesn't move, but also doesn't cause errors, ensure your RCServo has been enabled.\n"
                "Input Q and press ENTER to quit\n")

                end = False


                while (end != True):
                        bufY = sys.stdin.readline(100)
                        if not bufY:
                            continue
                        bufX = sys.stdin.readline(100)
                        if not bufX:
                            continue
                        if (bufY[0] == 'Q' or bufY[0] ==  'q' or bufX[0] == 'Q' or bufX[0] ==  'q'):
                            end = True
                            continue

                        try:
                            targetPositionY = float(bufY)
                            targetPositionX = float(bufX)

                        except ValueError as e:
                            print("Input must be a number, or Q to quit.")
                            continue
                        if (targetPositionY > chY.getMaxPosition() or targetPositionY < chY.getMinPosition()):
                            print("TargetPosition must be between %.2f and %.2f\n" % (chY.getMinPosition(), chY.getMaxPosition()))
                            continue

                        if (targetPositionX > chX.getMaxPosition() or targetPositionX < chX.getMinPosition()):
                            print("TargetPosition must be between %.2f and %.2f\n" % (chX.getMinPosition(), chX.getMaxPosition()))
                            continue

                        print("Setting RCServo TargetPosition to " + str(targetPositionY))
                        chY.setTargetPosition(targetPositionY)
                        print("Setting RCServo TargetPosition to " + str(targetPositionX))
                        chX.setTargetPosition(targetPositionX)

                print("Cleaning up...")
                chY.close()
                chX.close()
                print("\nExiting...")
                return 0


main()
