class DataPath:

    def __init__(self, rom, ram):
        self.acc = 0
        self.cr = 0 #command register
        self.ar = 0 #address register
        self.ip = 0 #instruction pointer
        self.dr = 0 #data register
        self.rom = rom
        self.ram = ram
    
    def fetch_instruction(self):
        self.cr = self.rom.read(self.ip)
        self.ip += 1

