import sys

from cpu_runner import CpuRunner


def run():
    CpuRunner().run(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    run()
