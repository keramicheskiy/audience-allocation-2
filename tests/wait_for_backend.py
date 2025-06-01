import os
import time
import requests

from settings import BACKEND_URL


def wait_for_backend(timeout=30):
    start_time = time.time()
    while True:
        try:
            response = requests.get(f"{BACKEND_URL}/health")
            if response.status_code == 200:
                print("Backend is ready")
                break
        except requests.exceptions.ConnectionError:
            pass

        if time.time() - start_time > timeout:
            raise TimeoutError("Backend did not start in time")
        print("Waiting for backend...")
        time.sleep(1)

if __name__ == "__main__":
    wait_for_backend()
