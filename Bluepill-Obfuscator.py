import base64, random, zlib, string, sys, py_compile, os
if len(sys.argv) <= 1:
    filename = input("Please drag a file into this terminal\n")
else:
    filename = sys.argv[1]
with open(filename, 'rb') as data:
    data = data.read()
splitlines = data.split(b"\n")

modules = b""
for imports in splitlines:
    if (imports.startswith(b"import") or imports.startswith(b"from")):
        modules += imports

bluepill= """
import base64;import zlib
x = {{
    "__dev__":"HamzLDN",
    "__git__": "https://github.com/HamzLDN",
    "__tiktok__": "@youarepwned"
}}
class BluePill:
    def __init__(self, code:bytes) -> None:self.code=code
    def tunnel(self, text, key) -> bytes: return bytes([byte ^ key[i % len(key)] for i, byte in enumerate(text)])
    def run(self) -> bytes: return compile(self.tunnel(zlib.decompress(base64.b85decode(self.code)), {}), 'string', 'exec')
"""
       # return exec(self.tunnel(dm(b6.b85decode(self.code)), {}))

key = ''.join(random.choice(string.ascii_letters) for _ in range(10)).encode('utf-8')
class BlueObf:
    def __init__(self,data):
        self.data = data
        self.b16 = b'b16decode'
        self.b32 = b'b32decode'
        self.b64 = b'b64decode'
        self.b85 = b'b85decode'
        self.anti_skid = b'if (x.get("__dev__") != "HamzLDN") or (x.get("__git__") != "https://github.com/HamzLDN") or (x.get("__tiktok__") != "@youarepwned") else '
        self.anti_skid_message = b"print('Keep trying... Made by youarepwned. AKA Bluepill')"
        self.sections = []
        self.vars = []
        self.headers = {
            "__dev__":"HamzLDN",
            "__git__": "https://github.com/HamzLDN",
            "__tiktok__": "@youarepwned"
        }

    def xor(self, text, key) -> bytes: return bytes([byte ^ key[i % len(key)] for i, byte in enumerate(text)])
    def var_gen(self, length):
        characters = string.ascii_letters
        while True:
            combo = ''.join(random.choice(characters) for _ in range(length))
            if combo not in self.vars: return combo
    def obf_rand(self, text, encode_type) -> bytes:
        if encode_type == 1:return base64.b64encode(text)
        if encode_type == 2:return base64.b32encode(text)
        if encode_type == 3:return base64.b16encode(text)
        if encode_type == 4:return base64.b85encode(text)

    def enc_layer1(self) -> bytes:
        for i in range(5):
            num = random.randint(1,4)
            encoder = b''
            if num==3:encoder = self.b16
            if num==2:encoder = self.b32
            if num==1:encoder = self.b64
            if num==4:encoder = self.b85
            if i!=0: self.data = b'exec(compile(base64.' + encoder + b'("' + self.obf_rand(self.data, num) + b'"), "string", "exec"))';continue
            self.data = self.anti_skid_message + self.anti_skid + b'exec(compile(base64.' + encoder + b'("' + self.obf_rand(self.data, num) + b'"), "string", "exec"))'
        self.data = base64.b85encode(zlib.compress(self.xor(self.data, key))); return self.data
    
    def randomizer(self):
        # Randomize the variables
        chunk_size = random.randint(2, 10)
        chunks = [self.data[i:i+chunk_size] for i in range(0, len(self.data), chunk_size)]
        new_val = []
        for i, values in enumerate(chunks, start=1):
            var_len = self.var_gen(10)
            self.vars.append(var_len)
            new_val.append("{} = '{}'".format(var_len ,values))

        random.shuffle(new_val)
        code = ";".join(new_val) + "\n" + 'exec(' + '+'.join(self.vars) + ')'
        return base64.a85encode(code.encode('utf-8'))

code = BlueObf(data).enc_layer1()
payload = modules + b"\n" +bluepill.format(key).encode('utf-8') + b"exec(BluePill('''"+code+b"''').run())"

with open(filename[:-3] + '-blueobf.py','wb') as f:
    f.write(payload)



py_compile.compile(filename[:-3] + '-blueobf.py', cfile=filename[:-3] + '-blueobf.pyc')

os.remove(filename[:-3] + '-blueobf.py')

try:
    input("File created at " + filename[:-3]+'-blueobf.pyc')
except Exception as e:
    input(e)
