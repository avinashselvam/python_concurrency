from utils import PINCODES, task
import time
import asyncio

def measure(f):
    def timed_f():
        start = time.time()
        f()
        end = time.time()
        print(f'\nTIME TAKEN = {end - start}\n')
    return timed_f

@measure
def sequential():
    for pincode in PINCODES:
        task(pincode)

@measure
def multi_threading():
    from threading import Thread
    threads = [Thread(target=task, kwargs={'pincode': PINCODES})]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

@measure
def multi_processing():
    from multiprocessing import Pool
    with Pool(4) as p:
        p.map(task, PINCODES)

@measure
async def event_driven():
    coroutines = [task(pincode) for pincode in PINCODES]
    await asyncio.gather(*coroutines)
    
sequential()
multi_threading()
multi_processing()
# asyncio.run(event_driven())
