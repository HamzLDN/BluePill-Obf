import base64, random, zlib

data = b'''
print("Hello World")
'''


b16 = b'b16decode'
b32 = b'b32decode'
b64 = b'b64decode'
b85 = b'b85decode'

headers = {
    "__dev__":"HamzLDN",
    "__git__": "https://github.com/HamzLDN",
    "__tiktok__": "@youarepwned"
}

def obf(text, encode_type):
    if encode_type == 1:return base64.b64encode(text)
    if encode_type == 2:return base64.b32encode(text)
    if encode_type == 3:return base64.b16encode(text)
    if encode_type == 4:return base64.b85encode(text)
anti_skid = b'print("haha skid detected. Keep trying...") if (x.get("__dev__") != "HamzLDN") or (x.get("__git__") != "https://github.com/HamzLDN") or (x.get("__tiktok__") != "@youarepwned") else '
sections = []
bluepill=b"""
import base64 as b6;from zlib import decompress as dm
x = {
    "__dev__":"HamzLDN",
    "__git__": "https://github.com/HamzLDN",
    "__tiktok__": "@youarepwned"
}
class BluePill:
    def __init__(self, code:bytes) -> None:self.code=code
    def run(self) -> bytes:return exec(dm(b6.b85decode(self.code)))
"""
for i in range(12):
    num = random.randint(1,4)

    encoder = b''
    if num==3:encoder = b16
    if num==2:encoder = b32
    if num==1:encoder = b64
    if num==4:encoder = b85
    if i!=0:
        data = b'exec(b6.' + encoder + b'("' + obf(data, num) + b'"))'
        continue
    data = b'exec(b6.' + encoder + b'("' + obf(data, num) + b'"))'
    data = anti_skid + data
data = base64.b85encode(zlib.compress(data))
payload = b"__import__(chr(98)+chr(97)+chr(115)+chr(101)+chr(54)+chr(52));BluePill('"+data+b"').run()"
sections.append(bluepill);sections.append(payload)

print(b"\n".join(sections).decode())