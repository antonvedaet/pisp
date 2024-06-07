from cpu_runner import CpuRunner
from translate import translate


def run():
    translate()
    CpuRunner().run()

if __name__ == "__main__":
    run()
