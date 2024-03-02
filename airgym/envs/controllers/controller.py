import torch

from airgym.envs.controllers.attitude_control import LeeAttitudeContoller
from airgym.envs.controllers.position_control import LeePositionController
from airgym.envs.controllers.velocity_control import LeeVelocityController


control_class_dict = {
    "lee_position_control": LeePositionController,
    "lee_velocity_control": LeeVelocityController,
    "lee_attitude_control": LeeAttitudeContoller
}

class Controller:
    def __init__(self, control_config, device):
        self.control_config = control_config
        self.device = device
        self.controller_name = control_config.controller
        self.kP = torch.tensor(control_config.kP, dtype=torch.float32, device=self.device)
        self.kV = torch.tensor(control_config.kV, dtype=torch.float32, device=self.device)
        self.kOmega = torch.tensor(control_config.kOmega, dtype=torch.float32, device=self.device)
        self.kR = torch.tensor(control_config.kR, dtype=torch.float32, device=self.device)

        self.scale_input = torch.tensor(control_config.scale_input, dtype=torch.float32, device=self.device)

        if self.control_config.controller not in control_class_dict:
            raise ValueError("Invalid controller name: {}".format(self.control_config.controller))
        else:
            if control_class_dict[self.controller_name] is LeeAttitudeContoller:
                self.controller = LeeAttitudeContoller(self.kR, self.kOmega)
            elif control_class_dict[self.controller_name] is LeePositionController:
                self.controller = LeePositionController(self.kP, self.kV, self.kR, self.kOmega)
            elif control_class_dict[self.controller_name] is LeeVelocityController:
                self.controller = LeeVelocityController(self.kV, self.kR, self.kOmega)
            else:
                raise ValueError("Invalid controller name: {}".format(self.control_config.controller))
            
    
    def __call__(self, robot_state, command_actions):
        # check if controller name matches class in dict
        scaled_input = command_actions * self.scale_input
        return self.controller(robot_state, scaled_input)
