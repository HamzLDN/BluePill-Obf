import base64, random, zlib, string, sys, py_compile, os,time
if len(sys.argv) <= 1:
    filename = input("Please drag a file into this terminal\n")
else:
    filename = sys.argv[1]
with open(filename, 'rb') as data:
    data = data.read()
splitlines = data.split(b"\n")

def get_imports():
    modules = b""
    for imports in splitlines:
        if (imports.startswith(b"import") or imports.startswith(b"from")):
            modules += imports + b"\n"
    return modules
def print_loading_bar(number):
    bar_length = 25
    percent = number / 100
    fill_length = int(percent * bar_length)
    empty_length = bar_length - fill_length
    new_bar = '=' * fill_length
    bar = f"[{new_bar[:-1]}>{' ' * empty_length}]"
    return bar
bluepill= """
import base64;import zlib
x = {
    "__dev__":"HamzLDN",
    "__git__": "https://github.com/HamzLDN",
    "__tiktok__": "@youarepwned"
}
class BluePill:
    def __init__(self, code:bytes,passcode:bytes) -> None:self.code=code;self.passcode=passcode;self.c=compile
    def tunnel(self, text, key) -> bytes: return bytes([byte ^ key[i % len(key)] for i, byte in enumerate(text)])
    def run(self) -> bytes: return self.c(self.tunnel(zlib.decompress(base64.b85decode(self.code)), self.passcode), 'string', 'exec')
"""
       # return exec(self.tunnel(dm(b6.b85decode(self.code)), {}))

key = ''.join(random.choice(string.ascii_letters) for _ in range(10000)).encode('utf-8')


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
        loop = random.randint(3,10)
        start = time.time()
        for i in range(loop):
            num = random.randint(1,4)
            encoder = b''
            if num==3:encoder = self.b16
            if num==2:encoder = self.b32
            if num==1:encoder = self.b64
            if num==4:encoder = self.b85
            percent = (i/loop)
            if i!=0: self.data = b'exec(compile(base64.' + encoder + b'("' + self.obf_rand(self.data, num) + b'"), "string", "exec"))'
            else: self.data = self.anti_skid_message + self.anti_skid + b'exec(compile(base64.' + encoder + b'("' + self.obf_rand(self.data, num) + b'"), "string", "exec"))'
            print(f"{print_loading_bar(int(percent * 100))}  Percent: ({int(percent*100)}%)", end='\r')
        self.data = base64.b85encode(zlib.compress(self.xor(self.data, key)))
        print(f"{print_loading_bar(int(100))}  Percent: ({int(100)}%)\n", end='\r')
        print("This can take around", int(time.time()-start), "seconds for the code to run")
        return self.data





print("Obfuscating")
code = BlueObf(data).enc_layer1()
payload = get_imports() + b"\n" +bluepill.encode('utf-8') + b"exec(BluePill('''"+code.replace(b'\0', b'')+b"''', b'" + key + b"').run())"

with open(filename[:-3] + '-blueobf.py','wb') as f:
    f.write(payload)
compiler = False
if compiler:
    py_compile.compile(filename[:-3] + '-blueobf.py', cfile=filename[:-3] + '-blueobf.pyc')

    os.remove(filename[:-3] + '-blueobf.py')

try:
    input("File created at " + filename[:-3]+'-blueobf.py')
except Exception as e:
    input(e)
