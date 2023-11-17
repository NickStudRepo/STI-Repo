import deflate, io

# # Decompress a bytes/bytearray value.
# compressed_data = get_data_z()
# with deflate.DeflateIO(io.BytesIO(compressed_data), deflate.ZLIB) as d:
#     decompressed_data = d.read()

# Compress a bytes/bytearray value.

f = open("./Huffman/demofile.txt","r")
data = f.read()
stream = io.BytesIO()
with deflate.DeflateIO(stream, deflate.ZLIB) as d:
    d.write(data)
compressed_data = stream.getvalue()

print(compressed_data)