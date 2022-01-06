import cv2

import angle_solver
import detection

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = detection.YOLOXDetection()
    solver = angle_solver.SinglePointSolver()

    while True:
        _, fr = cap.read()


