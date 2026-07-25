import json
import struct
import os

DEFAULT_PORT = 45000
CHUNK_SIZE = 65536

def create_message(message_dict):
    """Pack dict to [4 bytes length][JSON UTF-8]"""
    json_bytes = json.dumps(message_dict, ensure_ascii=False).encode('utf-8')
    length_prefix = struct.pack('>I', len(json_bytes))
    return length_prefix + json_bytes

async def read_message(reader):
    """Read message from asyncio StreamReader"""
    length_bytes = await reader.readexactly(4)
    message_length = struct.unpack('>I', length_bytes)[0]
    json_bytes = await reader.readexactly(message_length)
    return json.loads(json_bytes.decode('utf-8'))

def get_free_space(path):
    """Free space in bytes"""
    if os.name == 'nt':
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(path), None, None, ctypes.pointer(free_bytes)
        )
        return free_bytes.value
    else:
        stat = os.statvfs(path)
        return stat.f_frsize * stat.f_bavail