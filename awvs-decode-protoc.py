#!/usr/bin/env python3
import struct, zlib, os, datetime, script_pb2

# protobuf referer: https://developers.google.com/protocol-buffers/docs/encoding
mask, pos = 2 ** 32 - 16, 32
base_path = os.path.abspath("awvs_script_blob_decode_" + datetime.date.today().isoformat())
with open('wvsc_blob.bin', 'rb') as fp:
    raw = fp.read()
    while pos < len(raw):
        file_len = struct.unpack('<I', raw[pos:pos + 4])[0]
        d = zlib.decompress(raw[pos + 4: pos + 4 + file_len])
        script = script_pb2.wvs_script()
        script.ParseFromString(d)
        path = os.path.join(base_path, script.name[1:])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'wb').write(script.content)
        pos += ((file_len + 4) & mask) + 16
print('ok! output: %s' % base_path)