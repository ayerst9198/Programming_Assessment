import ctypes
import time

# Constants for key codes and window actions
VK_LWIN = 0x5B
VK_M = 0x4D
SW_MINIMIZE = 6

# Define the keybd_event() function from the Win32 API
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]
def keybd_event(key, flags):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(key, key, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Define a function to minimize the active window
def minimize_window():
    keybd_event(VK_LWIN, 0)  # Press the left Windows key
    keybd_event(VK_M, 0)     # Press the "M" key
    time.sleep(0.1)          # Wait for the window to minimize
    keybd_event(VK_M, 2)     # Release the "M" key
    keybd_event(VK_LWIN, 2)  # Release the left Windows key

# Loop until the "p" key is pressed
while True:
    if ctypes.windll.user32.GetAsyncKeyState(ord('P')):
        break

    minimize_window()
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_MINIMIZE) # Minimize console window
