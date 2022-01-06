import yaml
import numpy as np


class CamPara:
    def __init__(self, para_path="camera/uvc_camera.yml"):
        with open(para_path, mode='r') as para_f:
            para = yaml.load(para_f)

        _cam_mat = para['camera_matrix']['data']
        rows = para['camera_matrix']['rows']
        cols = para['camera_matrix']['cols']
        self._cam_mat = np.array(_cam_mat).reshape(rows, cols)

        _dist_mat = para['distortion_coefficients']['data']
        rows = para['distortion_coefficients']['rows']
        cols = para['distortion_coefficients']['cols']
        self._dist_mat = np.array(_dist_mat).reshape(rows, cols)

    @property
    def cam_mat(self):
        return self._cam_mat

    @property
    def dist_mat(self):
        return self._dist_mat

    @property
    def fx(self):
        return self._cam_mat[0, 0]

    @property
    def fy(self):
        return self._cam_mat[1, 1]

    @property
    def cx(self):
        return self._cam_mat[0, 2]

    @property
    def cy(self):
        return self._cam_mat[1, 2]

