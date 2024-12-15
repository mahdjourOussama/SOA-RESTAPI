import subprocess
import signal
import sys

services = [
    "services/watchdog/main.py",
    "services/decisionApproval/main.py",
    "services/properityEvaluation/main.py",
    "services/serviceComposer/main.py",
    "services/solvapilityVerification/main.py",
    "services/textMining/main.py",
    # "app.py",
]

processes = []


def signal_handler(sig, frame):
    for process in processes:
        process.terminate()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    for service in services:
        process = subprocess.Popen(["python", service])
        processes.append(process)

    for process in processes:
        process.wait()
