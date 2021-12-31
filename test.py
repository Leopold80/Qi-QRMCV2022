import IPC
import detection
import videostream

if __name__ == "__main__":
    ipc = IPC.Queue()
    producer = videostream.Producer(ipc=ipc, src=0)
    consumer = detection.YOLOXDetection(ipc=ipc, dev="CPU")

    producer.start()
    consumer.start()

    producer.join()
    consumer.start()
