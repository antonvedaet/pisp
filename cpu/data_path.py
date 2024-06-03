class DataPath:

    def __init__(self, rom, ram):
        self.acc = 0
        self.cr = 0 #command register
        self.ar = 0 #address register
        self.ip = 0 #instruction pointer
        self.dr = 0 #data register
        self.rom = rom
        self.ram = ram
    

    # ЭТО ДЕЛАЕТСЯ В CONTROL UNIT'E
    def fetch_instruction(self):
        self.ar = self.ip

        self.cr = self.rom.read(self.ar)

        self.ip += 1

    def info(self):
        return(f"AR: {self.ar} | IP: {self.ip} | DR: {self.dr} | ACC: {self.acc}")
