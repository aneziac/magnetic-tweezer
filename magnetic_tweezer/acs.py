"""
ACS Motion Control Interface
for Z axis motor

2022.07.06 Phantomlsh
"""

# import ctypes


# MIN_Z = 0
# MAX_Z = 39

# # look into using https://github.com/petebachant/ACSpy instead
# io = ctypes.windll.LoadLibrary("ACSCL_x64.dll")
# double = ctypes.c_double

# # connect to ACS Motion Control
# # Note the encoding of string
# hc = io.acsc_OpenCommEthernetTCP(b"10.0.0.100", 701)

# if hc == -1:
#     print("Failed to connect ACS Motion Control")
# else:
#     io.acsc_Enable(hc, 0, 0)
#     print("Connected to ACS Motion Control")


# def magnet_height_to(pos: float) -> None:
#     """Change the height of the magnet via the ACS Motion Control"""
#     if pos < MIN_Z or pos > MAX_Z:
#         raise RuntimeError('Motor position out of bounds')
#     io.acsc_ToPoint(hc, 0, 0, double(pos), 0)
