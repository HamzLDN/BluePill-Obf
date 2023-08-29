import base64, random, zlib, string, sys, py_compile, os,time,site

def get_file_data():
    if len(sys.argv) <= 1:
        filename = input("Please drag a file into this terminal\n")
    else:
        filename = sys.argv[1]
    with open(filename, 'rb') as data:
        data = data.read()
    return data.split(b"\n"), data, filename

key = ''.join(random.choice(string.ascii_letters) for _ in range(10000)).encode('utf-8')
def get_imports(splitlines: list):
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

    def enc_layer1(self, layers) -> bytes:
        start = time.time()
        for i in range(layers):
            num = random.randint(1,4)
            encoder = b''
            if num==3:encoder = self.b16
            if num==2:encoder = self.b32
            if num==1:encoder = self.b64
            if num==4:encoder = self.b85
            percent = (i/layers)
            if i!=0: self.data = b'exec(compile(base64.' + encoder + b'("' + self.obf_rand(self.data, num) + b'"), "string", "exec"))'
            else: self.data = self.anti_skid_message + self.anti_skid + b'exec(compile(base64.' + encoder + b'("' + self.obf_rand(self.data, num) + b'"), "string", "exec"))'
            print(f"{print_loading_bar(int(percent * 100))}  Percent: ({int(percent*100)}%)", end='\r')
        self.data = base64.b85encode(zlib.compress(self.xor(self.data, key)))
        print(f"{print_loading_bar(int(100))}  Percent: ({int(100)}%)\n", end='\r')
        print("This can take around", int(time.time()-start), "seconds for the code to run")
        return self.data



def compile_2_exe(filename, icon, exename):
    PyInstaller.__main__.run([
        '--name='+exename,
        '--onefile',
        '--icon='+icon,
        '--distpath='+os.getcwd(),
        filename + '-blueobf.py'
    ])
    os.remove(filename + '-blueobf.py')
if __name__ == '__main__':
    compile2pyc = False
    compile2exe = False
    icon = None
    exename = ""
    try:
        import PyInstaller.__main__
    except:
        pyinst = input("pyinstaller is not installed... would you like to install it? [y/N]").lower()
        if pyinst == "y":
            print("Installing pyinstaller")
            if os.name == "nt": os.popen("pip install pyinstaller > NUL 2>&1")
            else: os.popen("pip install pyinstaller > /dev/null 2>&1")
            print("Installed")
    exe = input("Would you like to convert it to an exe [y/N]").lower()
    if exe == "y":
        compile2exe = True
    if not compile2exe:
        pyc = input("Would you like to convert it to a pyc [Y/n]").lower()
        if pyc == "y":
            compile2pyc = True
    else:
        exename = input("Please give your exe a name: ")
    layersofenc = input("How many layers would you want to encrypt? Default random 3-10. Anything above 10 is not recommended").lower()
    try:
        layers = int(layersofenc)
    except:
        layers = random.randint(3,10)
        print("Invalid integer. Using {} layers".format(layers))
    addicon = input("Please add an icon file path. Type N for NONE").lower()
    if addicon != "y":
        icon = "NONE"
    else:
        icon = addicon

    modules, data, filename = get_file_data()
    code = BlueObf(data).enc_layer1(layers)
    payload = get_imports(modules) + b"\n" +bluepill.encode('utf-8') + b"exec(BluePill('''"+code.replace(b'\0', b'')+b"''', b'" + key + b"').run())"
    filename = filename[:-3]
    with open(filename+ '-blueobf.py','wb') as f:
        f.write(payload)
    if compile2pyc:
        print("INTERESTING")
        py_compile.compile(filename + '-blueobf.py', cfile=filename + '-blueobf.pyc')
        os.remove(filename + '-blueobf.py')
    if compile2exe:
        print("FILENAME:",filename)
        compile_2_exe(filename, icon, exename)
    input("File created at " + filename + '-blueobf.py')