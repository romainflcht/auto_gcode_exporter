from functions import *
import time


export_queue = []


while 1:
    fill_export_queue(export_queue)

    start_timer = time.time()
    if export_files(export_queue) == 0:
        export_queue.clear()
        send_toast_export_finished(time.time() - start_timer)