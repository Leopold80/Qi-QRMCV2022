import cv2

from camera import CamPara
from .solver_base import SolverBase


class SinglePointSolver(SolverBase):
    def __init__(self, cam_para=CamPara()):
        super().__init__(cam_para)

    def get_angle(self, points):
        undistorted_points = cv2.undistortPoints(
            points, self.cam_para.cam_mat, self.cam_para.dist_mat,
            None, self.cam_para.cam_mat
        )

    def undistort_image(self, fr):
        undistort_fr = cv2.undistort(fr, self.cam_para.cam_mat, self.cam_para.dist_mat)
        return undistort_fr