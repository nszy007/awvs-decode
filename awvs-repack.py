#!/usr/bin/env python3
import struct, zlib, os, datetime, sys


def tailor_protobuf_encode(path, content):
    '''
    protobuf format:
    message {
        required string name = 1;
        required bytes content = 2;
    }
    name:    tag=(1<<3)|2 = 10 = 0x0a = '\x0a'
    content: tag=(2<<3)|2 = 18 = 0x12 = '\x12'
    '''

    def encode_int(n):
        parts = []
        while n > 0:
            parts.append((n & 0x7f) | 0x80)
            n >>= 7
        if len(parts) > 0: parts[-1] &= 0x7f
        return bytes(parts) if len(parts) else b'\x00'

    encode_bytes = lambda s: encode_int(len(s)) + s
    return b'\x0a' + encode_bytes(b'/' + path) + b'\x12' + encode_bytes(content)


mask, pos = 2 ** 32 - 16, 32
input_directory = os.path.abspath(
    sys.argv[1] if len(sys.argv) > 1 else "awvs_script_blob_decode_" + datetime.date.today().isoformat())
with open('wvsc_blob-repack.bin', 'wb') as fp:
    fp.write(b'\x00' * pos)
    for dir_path, _, names in os.walk(input_directory):
        for name in names:
            content = tailor_protobuf_encode(
                os.path.relpath(os.path.join(dir_path, name), start=input_directory).replace("\\", "/").encode('utf-8'),
                open(os.path.join(dir_path, name), 'rb').read())
            compressed = zlib.compress(content, level=9)
            fp.write(struct.pack('<I', len(compressed)) + compressed)
            file_len = len(compressed)
            fp.write(b'\x00' * (((len(compressed) + 4) & mask) + 12 - len(compressed)))
print('ok! output: wvsc_blob-repack.bin\n')
