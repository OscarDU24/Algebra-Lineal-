import ctypes


if hasattr(ctypes, "windll"):
    ctypes.windll.gdi32.AddFontResourceExW.argtypes = [
        ctypes.c_void_p,
        ctypes.c_uint,
        ctypes.c_void_p,
    ]

import customtkinter as ctk
