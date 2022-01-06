import IPC
import detection
import camera

if __name__ == "__main__":
    ipc = IPC.Queue()
    producer = camera.Producer(ipc=ipc, src=0)
    consumer = detection.YOLOXDetection(ipc=ipc, dev="CPU")

    producer.start()
    consumer.start()

    producer.join()
    consumer.start()
