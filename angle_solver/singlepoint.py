import numpy as np

import cv2

from camera import CamPara
from .solver_base import SolverBase


class SinglePointSolver(SolverBase):
    def __init__(self, cam_para=CamPara()):
        super().__init__(cam_para)

    def get_angle(self, points):
        # shape of points [n, 2]
        # 去除畸变后的点
        undis_points = cv2.undistortPoints(
            points, self.cam_para.cam_mat, self.cam_para.dist_mat,
            None, self.cam_para.cam_mat
        )
        undis_points = np.squeeze(undis_points, axis=1)

        rx = (undis_points[:, 0] - self.cam_para.cx) / self.cam_para.fx
        ry = (undis_points[:, 1] - self.cam_para.cy) / self.cam_para.fy

        return (np.arctan(rx) / np.pi * 180.) + 180., (np.arctan(ry) / np.pi * 180.) + 180., undis_points

    def undistort_image(self, fr):
        undistort_fr = cv2.undistort(fr, self.cam_para.cam_mat, self.cam_para.dist_mat)
        return undistort_fr
