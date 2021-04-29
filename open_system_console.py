# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
import ctypes
from ctypes import wintypes


bl_info = {
    "name": "Open/Close System Console",
    "author": "todashuta",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "Menu Bar > Open System Console, F3 Search > Open System Console/Close System Console",
    "description": "",
    "warning": "",
    "wiki_url": "https://github.com/todashuta/blender-addon-console-open-close/wiki",
    "tracker_url": "https://github.com/todashuta/blender-addon-console-open-close/issues",
    "category": "3D View"
}


def num_windows() -> int:
    import os
    blender_exe_pid = os.getpid()
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    EnumWindows = ctypes.windll.user32.EnumWindows
    tids = []
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    def callback(hwnd, lparam):
        pid = wintypes.DWORD()
        tid = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            if pid.value == blender_exe_pid:
                tids.append(tid)
            return True
    EnumWindows(EnumWindowsProc(callback), 0)
    return len(tids)


def console_opened() -> bool:
    n1 = num_windows()
    bpy.ops.wm.console_toggle()
    n2 = num_windows()
    bpy.ops.wm.console_toggle()
    return n1 > n2


def console_open():
    if not console_opened():
        return bpy.ops.wm.console_toggle()
    else:
        return {"CANCELLED"}


def console_close():
    if console_opened():
        return bpy.ops.wm.console_toggle()
    else:
        return {"CANCELLED"}


class WINDOW_OT_open_system_console(bpy.types.Operator):
    bl_idname = "wm.console_open"
    bl_label  = "Open System Console"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return console_open()


class WINDOW_OT_close_system_console(bpy.types.Operator):
    bl_idname = "wm.console_close"
    bl_label  = "Close System Console"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return console_close()


classes = [
        WINDOW_OT_open_system_console,
        WINDOW_OT_close_system_console,
]


def menu_func(self, context):
    layout = self.layout
    layout.operator(WINDOW_OT_open_system_console.bl_idname, icon="CONSOLE")
    layout.separator()


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_window.prepend(menu_func)


def unregister():
    bpy.types.TOPBAR_MT_window.remove(menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
