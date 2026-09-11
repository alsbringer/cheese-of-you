from entities import Player, Frame
from utils import flip_x

class Effect():
    def __init__(self,type, frames, delay):
        self.type = "slash"
        self.active = False
        self.frames: list[Frame] = frames
        self.active_index = 0
        self.target: Player = None
        self.margin = 10
        self.timer = 0
        self.delay = delay
        
    def update_effect(self):
        for frame in self.frames:
            if self.target:
                if frame.face_direction != self.target.face_direction:
                    frame.surface = flip_x(frame.surface)
                    frame.face_direction = self.target.face_direction
            
                if self.target.face_direction == "right":
                    frame.rect.left = self.target.rect.right -self.margin # atur posisi frame sesuai target
                    frame.rect.centery = self.target.rect.centery
                elif self.target.face_direction == "left":
                    frame.rect.right = self.target.rect.left + self.margin
                    frame.rect.centery = self.target.rect.centery
        
        if self.active:            
            self.timer += 1
            if self.timer >= self.delay:
                self.active_index+=1
                self.timer = 0
                if self.active_index >= len(self.frames):
                    self.active_index = 0
                    self.end_effect()
            
    def start_effect(self, target : Player):
        self.active = True
        self.target = target
        for frame in self.frames:
            frame.face_direction = target.face_direction
        
    def end_effect(self):
        self.active = False