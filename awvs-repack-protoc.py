#!/usr/bin/env python3
import struct, zlib, os, datetime, sys, script_pb2

mask, pos = 2 ** 32 - 16, 32
input_directory = os.path.abspath(
    sys.argv[1] if len(sys.argv) > 1 else "awvs_script_blob_decode_" + datetime.date.today().isoformat())
with open('wvsc_blob-repack.bin', 'wb') as fp:
    fp.write(b'\x00' * pos)
    for dir_path, _, names in os.walk(input_directory):
        for name in names:
            script = script_pb2.wvs_script()
            script.name = '/' + os.path.relpath(os.path.join(dir_path, name), start=input_directory).replace("\\", "/")
            script.content = open(os.path.join(dir_path, name), 'rb').read()
            compressed = zlib.compress(script.SerializeToString(), level=9)
            fp.write(struct.pack('<I', len(compressed)) + compressed)
            fp.write(b'\x00' * (((len(compressed) + 4) & mask) + 12 - len(compressed)))
print('ok! output: wvsc_blob-repack.bin\n')
