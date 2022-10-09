from Phidget22.Devices.RCServo import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from PhidgetHelperFunctions import *
from tkinter import *
import time
import cv2
import globs

def onAttachHandler(self):
    ph = self

    try:
        # If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        # www.phidgets.com/docs/Using_Multiple_Phidgets for information

        print("\nAttach Event:")

        """
		* Get device information and display it.
		"""
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT:
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


def onDetachHandler(self):
    ph = self

    try:
        # If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        # www.phidgets.com/docs/Using_Multiple_Phidgets for information

        print("\nDetach Event:")

        """
		* Get device information and display it.
		"""
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT:
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


def onErrorHandler(self, errorCode, errorString):
    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")


def PrintEventDescriptions():
    print("\n--------------------\n"
          "\n  | Target Position Reached events will call their associated function every time the RCServo controller has reached its target position.\n"
          "  | Press ENTER once you have read this message.")
    readin = sys.stdin.readline(1)

    print("\n--------------------")





globs.chY = RCServo()
globs.chX = RCServo()
globs.chY.setDeviceSerialNumber(492965)
globs.chX.setDeviceSerialNumber(492965)
globs.chY.setChannel(1)
globs.chX.setChannel(0)
globs.chY.setOnAttachHandler(onAttachHandler)
globs.chX.setOnAttachHandler(onAttachHandler)
globs.chY.setOnDetachHandler(onDetachHandler)
globs.chX.setOnDetachHandler(onDetachHandler)
globs.chY.setOnErrorHandler(onErrorHandler)
globs.chX.setOnErrorHandler(onErrorHandler)

try:
    globs.chY.openWaitForAttachment(5000)
    globs.chX.openWaitForAttachment(5000)
except PhidgetException as e:
    PrintOpenErrorMessage(e, globs.chX)
    PrintOpenErrorMessage(e, globs.chY)
    raise EndProgramSignal("Program Terminated: Open Failed")


def fnc_play():
    globs.window.destroy()
    time.sleep(1)
    play = 0
    targetPositionY = float(50)
    targetPositionX = float(100)
    globs.chY.setTargetPosition(targetPositionY)
    globs.chX.setTargetPosition(targetPositionX)
    globs.chY.close()
    globs.chX.close()



globs.index_picture = 0

def take_picture():
    picName = "pictures/pic" + str(globs.index_picture) + ".jpg"
    globs.index_picture += 1
    cv2.imwrite(picName, globs.frame_zoom)


#init GUI
globs.window = Tk()
globs.window.title("")
globs.window.attributes('-fullscreen', True)  
# window.iconbitmap("images_gui/drone_logo_yPm_icon.ico")
globs.window.config(background='#034B5E')

#title project
frame_top = Frame(globs.window, bg='#034B5E', bd=0, relief=SUNKEN)
label_title = Label(frame_top, text="Drone Surveillance System", font=("Calibri", 40, "bold"), bg='#034B5E', fg='white')
label_title.pack(pady=10)
frame_top.pack(side=TOP, fill=BOTH)

# bottom text
frame_bottom = Frame(globs.window, bg='#034B5E', bd=2, relief=SUNKEN)
label_bottom1 = Label(frame_bottom, text="Drone Detection Project 2 - Amir Sarig & Michael Aboulhair\nSupervised by Johanan Erez, Eli Appleboim, Israel Berger, Yossi Bar Erez and Zhitnikov Andrey\nTechnion - Israel Institute of Technology, Department of Electrical Engineering\nVision and Image Sciences Laboratory (VISL)\n2019/2020",
	              font=("Calibri", 15), bg='#034B5E', fg='#6B777F')

image_technion = PhotoImage(file="images_gui/logo_technion.png")
#image_technion = image_technion.zoom(60)
#image_technion = image_technion.subsample(32)
label_logo_technion = Label(frame_bottom, image=image_technion, bg='#034B5E')
label_logo_technion.pack(side=LEFT, padx=20)

image_fac = PhotoImage(file="images_gui/logo_fac.png")
#image_fac = image_fac.zoom(60)
#image_fac = image_fac.subsample(32)
label_fac = Label(frame_bottom, image=image_fac, bg='#034B5E')
label_fac.pack(side=LEFT, padx=20)

image_VISL = PhotoImage(file="images_gui/logo_visl.png")
#image_VISL = image_VISL.zoom(60)
#image_VISL = image_VISL.subsample(32)
label_logo_VISL = Label(frame_bottom, image=image_VISL, bg='#034B5E')
label_logo_VISL.pack(side=LEFT, padx=10)

label_bottom1.pack(side=LEFT, padx=45)
frame_bottom.pack(side=BOTTOM, fill=BOTH)


# zoom cam text
frame_sc = Frame(globs.window, bg='#034B5E', bd=2, relief= GROOVE)
label_sc = Label(frame_sc, text="Zoom Camera", font=("Calibri", 30, "bold"), bg='#034B5E', fg='white')
label_sc.pack(pady=5)
label_moving = Label(frame_sc, text="Moving", font=("Calibri", 20), bg='#034B5E', fg='white')
label_moving.pack()
frame_sc.pack(side=RIGHT, expand=True, fill=BOTH)
frame_sc.bind('<Escape>', lambda e: frame_sc.quit())
globs.main_sc = Label(frame_sc)
globs.main_sc.pack(pady=20)
globs.label_sc2 = Label(frame_sc, text="Looking for drones...", font=("Calibri", 30, "bold"), bg='#034B5E', fg='red')
globs.label_sc2.pack(pady=5)
globs.label_sc3 = Label(frame_sc, text="", font=("Calibri", 20), bg='#034B5E', fg='red')
globs.label_sc3.pack()
globs.label_sc4 = Label(frame_sc, text="", font=("Calibri", 20), bg='#034B5E', fg='red')
globs.label_sc4.pack()

# wide cam text
frame_lc = Frame(globs.window, bg='#034B5E', bd=2, relief=GROOVE)
label_lc = Label(frame_lc, text="RealSense Camera", font=("Calibri", 30, "bold"), bg='#034B5E', fg='white')
label_fixed = Label(frame_lc, text="Fixed", font=("Calibri", 20), bg='#034B5E', fg='white')
label_lc.pack(pady=5)
label_fixed.pack()
frame_lc.pack(side=LEFT, expand=True, fill=BOTH)
frame_lc.bind('<Escape>', lambda e: frame_lc.quit())
globs.main_lc = Label(frame_lc)
globs.main_lc.pack(pady=20)
label_lc3 = Label(frame_lc, text="Motion detection", font=("Calibri", 30, "bold"), bg='#034B5E', fg='white')
label_lc3.pack(pady=5)
label_lc2 = Label(frame_lc, text="", font=("Calibri", 20), bg='#034B5E', fg='red')
label_lc2.pack(pady=5)


# button quit
frame_button = Frame(globs.window, bg='#034B5E', bd=0, relief=GROOVE)
quit_button = Button(frame_button, bg='#034B5E', fg='#034B5E', highlightthickness=0, bd=0, relief=GROOVE, command=fnc_play)
close_icon = PhotoImage(file="images_gui/close_icon.png")
close_icon = close_icon.zoom(25)
close_icon = close_icon.subsample(32)
quit_button.config(image=close_icon, bg='#034B5E', fg='#034B5E', highlightthickness=0, bd=0, relief=GROOVE)
quit_button.pack(pady=10)


# button save picture
take_picture_button = Button(frame_button, bg='#034B5E', highlightthickness=0, bd=0, relief=GROOVE, command=take_picture)
camera_icon = PhotoImage(file="images_gui/camera_icon.png")
camera_icon = camera_icon.zoom(25)
camera_icon = camera_icon.subsample(32)
take_picture_button.config(image=camera_icon, bg='#034B5E', highlightthickness=0, bd=0, relief=GROOVE)
take_picture_button.pack(pady=20)
frame_button.pack(side=TOP, expand=True, fill=BOTH)

# system image 
image_system = PhotoImage(file="images_gui/system.png")
image_system = image_system.zoom(25)
image_system = image_system.subsample(32)
label_system = Label(frame_button, image=image_system, bg='#034B5E')
label_system.pack(pady=70)

# Servos angles
globs.label_angles_text = Label(frame_button, text="""Motor's Position:""", font=("Calibri", 20), bg='#034B5E', fg='white')
globs.label_angles_text.pack()

globs.label_angles = Label(frame_button, text='\u03B8x = '+str("{0:.1f}".format(globs.posX))+'\n\u03B8y = '+ str("{0:.1f}".format(globs.posY)), font=("Calibri", 20), bg='#034B5E', fg='white')
globs.label_angles.pack()




