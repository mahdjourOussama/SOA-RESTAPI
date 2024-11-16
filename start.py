import subprocess
import signal
import sys

services = [
    "WatchdogService.py",
    "DecisionApprovalService.py",
    "ProperityEvaluationService.py",
    "ServiceComposer.py",
    "SolvapilityVerificationService.py",
    "TextMiningService.py",
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
