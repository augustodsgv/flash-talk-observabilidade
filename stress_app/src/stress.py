import multiprocessing
import time
import math

class Stress:
    def __init__(self):
        pass

    def _cpu_stress_fn(self, stress_time : int) -> None:
        start_time = time.time()
        while time.time() - start_time < stress_time:
            math.sqrt(1 * 2 * 4 * 8 * 16 * 32 * 64 * 128)

    def cpu_stress(self, stress_time : int, cores_n : int) -> None:
        if cores_n > multiprocessing.cpu_count():
            raise ValueError('Trying to use more cpus than are available')
        processes = []
        for _ in range(cores_n):
            p = multiprocessing.Process(target=self._cpu_stress_fn, args=(stress_time,))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
           
    def memory_stress(self, stress_time : int, bytes_n : int) -> None:
        start_time = time.time()
        memory_allocated = bytearray(bytes_n)
        while time.time() - start_time < stress_time:
            pass