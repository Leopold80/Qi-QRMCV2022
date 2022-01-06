from camera import CamPara


class SolverBase:
    def __init__(self, cam_para=CamPara()):
        self.cam_para = cam_para

    def get_angle(self) -> tuple:
        raise NotImplementedError()
