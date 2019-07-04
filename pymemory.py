import ctypes
from ctypes.wintypes import *
import win32gui
import win32process
import win32api
import psutil
import getpass

PROCESS_ALL_ACCESS = 0x1F0FFF
TH32CS_INHERIT = 0x80000000
TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPTHREAD = 0x00000004

def open_process(dwDesiredAccess, bInheritHandle, pid):
    OpenProcess = ctypes.windll.kernel32.OpenProcess
    OpenProcess.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD]
    OpenProcess.restype = ctypes.wintypes.HANDLE

    return OpenProcess(dwDesiredAccess, bInheritHandle, pid)
    
def close_handle(handle):
    CloseHandle = ctypes.windll.kernel32.CloseHandle
    CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
    CloseHandle.restype = ctypes.wintypes.BOOL
    
    return CloseHandle(handle)

class MODULEENTRY32(ctypes.Structure):
    _fields_ = [("dwSize", ctypes.c_long),
                ("th32ModuleID", ctypes.c_long),
                ("th32ProcessID", ctypes.c_long),
                ("GlblcntUsage", ctypes.c_long),
                ("ProccntUsage", ctypes.c_long),
                ("modBaseAddr", ctypes.c_long),
                ("modBaseSize", ctypes.c_long),
                ("hModule", ctypes.c_void_p),
                ("szModule", ctypes.c_char*256),
                ("szExePath", ctypes.c_char*260)]

def create_tool_help32_snapshot(flags, pid):
    CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    CreateToolhelp32Snapshot.argtypes = [ctypes.c_int, ctypes.c_int]
    return CreateToolhelp32Snapshot(flags, pid)

def module32_first(hModuleSnap, me32Ptr):
    Module32First = ctypes.windll.kernel32.Module32First
    Module32First.argtypes = [ctypes.c_void_p, ctypes.POINTER(MODULEENTRY32)]
    Module32First.reltype = ctypes.c_int

    return Module32First(hModuleSnap, me32Ptr)

def module32_next(hModuleSnap, me32Ptr):
    Module32Next = ctypes.windll.kernel32.Module32Next
    Module32Next.argtypes = [ctypes.c_void_p, ctypes.POINTER(MODULEENTRY32)]
    Module32Next.reltype = ctypes.c_int

    return Module32Next(hModuleSnap, me32Ptr)

def get_module_base_address(pid, moduleName):
    hModuleSnap = ctypes.c_void_p(0)
    me32 = MODULEENTRY32()
    me32.dwSize = ctypes.sizeof(MODULEENTRY32)
    hModuleSnap = create_tool_help32_snapshot(TH32CS_SNAPMODULE, pid)

    mod = module32_first(hModuleSnap, ctypes.pointer(me32))

    if not mod:
        print("Error getting client_panorama.dll base address", getLastError())
        mem.close_handle(hModuleSnap)
        return False
    while mod:
        if me32.szModule.decode() == moduleName:
            close_handle(hModuleSnap)
            return me32.modBaseAddr
        else: 
            mod = module32_next(hModuleSnap, ctypes.pointer(me32))

def getPIDbyName(procName):
    for process in psutil.process_iter(attrs=["pid", "name", "username"]):
    	if process.name() == procName:
    		return process.pid

def write_bool(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_bool(value)),  ctypes.sizeof(ctypes.c_bool(value)), ctypes.c_ulong(0))

def write_char(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_char(value)), ctypes.sizeof(ctypes.c_char(value)), ctypes.c_ulong(0))

def write_wchar(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_wchar(value)), ctypes.sizeof(ctypes.c_wchar(value)), ctypes.c_ulong(0))

def write_byte(hProcess, address, value): 
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.c_byte(ctypes.c_wchar(value)), ctypes.sizeof(ctypes.c_byte(value)), ctypes.c_ulong(0))

def write_ubyte(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.c_ubyte(ctypes.c_wchar(value)), ctypes.sizeof(ctypes.c_ubyte(value)), ctypes.c_ulong(0))

def write_short(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.c_short(ctypes.c_wchar(value)), ctypes.sizeof(ctypes.c_short(value)), ctypes.c_ulong(0))

def write_u_short(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.c_ushort(ctypes.c_wchar(value)), ctypes.sizeof(ctypes.c_ushort(value)), ctypes.c_ulong(0))

def write_int(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_int(value)),  ctypes.sizeof(ctypes.c_int(value)), ctypes.c_ulong(0))

def write_int32(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_int32(value)),  ctypes.sizeof(ctypes.c_int32(value)), ctypes.c_ulong(0))

def write_int64(hProcess, address, value):   
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_int64(value)),  ctypes.sizeof(ctypes.c_int64(value)), ctypes.c_ulong(0))

def write_uint(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_uint(value)),  ctypes.sizeof(ctypes.c_uint(value)), ctypes.c_ulong(0))

def write_uint32(hProcess, address, value):    
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_uint32(value)),  ctypes.sizeof(ctypes.c_uint32(value)), ctypes.c_ulong(0))

def write_uint64(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_uint64(value)),  ctypes.sizeof(ctypes.c_uint64(value)), ctypes.c_ulong(0))

def write_long(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_long(value)),  ctypes.sizeof(ctypes.c_long(value)), ctypes.c_ulong(0))

def write_ulong(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_ulong(value)),  ctypes.sizeof(ctypes.c_ulong(value)), ctypes.c_ulong(0))

def write_longlong(hProcess, address, value):   
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_longlong(value)),  ctypes.sizeof(ctypes.c_longlong(value)), ctypes.c_ulong(0))

def write_ulongLong(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_ulonglong(value)),  ctypes.sizeof(ctypes.c_ulonglong(value)), ctypes.c_ulong(0))

def write_c_size_t(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_size_t(value)),  ctypes.sizeof(ctypes.c_size_t(value)), ctypes.c_ulong(0))



def write_c_ssize_t(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_ssize_t(value)),  ctypes.sizeof(ctypes.c_ssize_t(value)), ctypes.c_ulong(0))



def write_float(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_float(value)),  ctypes.sizeof(ctypes.c_float(value)), ctypes.c_ulong(0))

def write_double(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_double(value)),  ctypes.sizeof(ctypes.c_double(value)), ctypes.c_ulong(0))

def write_longdouble(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_longdouble(value)),  ctypes.sizeof(ctypes.c_longdouble(value)), ctypes.c_ulong(0))

def write_c_char_p(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_char_p(value)),  ctypes.sizeof(ctypes.c_char_p(value)), ctypes.c_ulong(0))

def write_wc_char_p(hProcess, address, value):
    ctypes.windll.kernel32.WriteProcessMemory(hProcess, address, ctypes.byref(ctypes.c_wchar_p(value)),  ctypes.sizeof(ctypes.c_wchar_p(value)), ctypes.c_ulong(0))

def read_bool(hProcess, address):
    ReadBuffer = ctypes.c_bool()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_char(hProcess, address):
    ReadBuffer = ctypes.c_char()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_wchar(hProcess, address, ):
    ReadBuffer = ctypes.c_wchar()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_byte(hProcess, address):
    ReadBuffer = ctypes.c_byte()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_ubyte(hProcess, address):
    ReadBuffer = ctypes.c_ubyte()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_short(hProcess, address):
    ReadBuffer = ctypes.c_short()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)

    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_u_short(hProcess, address):
    ReadBuffer = ctypes.c_ushort()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)   
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_int(hProcess, address):
    ReadBuffer = ctypes.c_int()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_int32(hProcess, address):
    ReadBuffer = ctypes.c_int32()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_int64(hProcess, address):
    ReadBuffer = ctypes.c_int64()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_uint(hProcess, address):
    ReadBuffer = ctypes.c_uint()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_uint32(hProcess, address):
    ReadBuffer = ctypes.c_uint32()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_uint64(hProcess, address):
    ReadBuffer = ctypes.c_uint64()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_long(hProcess, address):
    ReadBuffer = ctypes.c_long()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_ulong(hProcess, address):
    ReadBuffer = ctypes.c_ulong()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_longlong(hProcess, address):
    ReadBuffer = ctypes.c_longlong()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_ulongLong(hProcess, address):
    ReadBuffer = ctypes.c_ulonglong()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_c_size_t(hProcess, address, ):
    ReadBuffer = ctypes.c_size_t()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value


def read_c_ssize_t(hProcess, address):
    ReadBuffer = ctypes.c_ssize_t()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value


def read_float(hProcess, address):
    ReadBuffer = ctypes.c_float()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_double(hProcess, address):
    ReadBuffer = ctypes.c_double()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_longdouble(hProcess, address):
    ReadBuffer = ctypes.c_longdouble()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_c_char_p(hProcess, address):
    ReadBuffer = ctypes.c_char_p()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value

def read_wc_char_p(hProcess, address):
    ReadBuffer = ctypes.c_wchar_p()
    lpBuffer = ctypes.byref(ReadBuffer)
    nSize = ctypes.sizeof(ReadBuffer)
    bytesRead = ctypes.c_ulong(0)
    
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, address, lpBuffer, nSize, bytesRead)
    return ReadBuffer.value
