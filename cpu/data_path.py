from ALU import ALU

class DataPath:

    def __init__(self, rom, ram):
        self.ALU = ALU()
        self.acc = 0
        self.cr = 0 #command register
        self.ar = 0 #address register
        self.ip = 0 #instruction pointer
        self.dr = 0 #data register
        self.sr = self.ALU.flags() #status register
        self.output = []
        self.input = list(input())
        self.rom = rom
        self.ram = ram
    
    def fetch_instruction(self):
        self.ar = self.ip

        self.cr = self.rom.read(self.ar)

        self.ip += 1

    def alu_flags(self):
        self.ALU.value = self.acc
        self.ALU.refresh_flags()

    def info(self):
        self.sr = self.ALU.flags()
        return(f"AR: {self.ar} | IP: {self.ip} | DR: {self.dr} | ACC: {self.acc} | NZC: {self.sr}")
