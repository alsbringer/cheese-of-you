from utils import flip_x

class Skill():
    def __init__(self,type,name , frames, delay):
        self.name = name
        self.type = type
        self.active = False
        self.frames = frames
        self.active_index = 0
        self.counter = -1
        self.target = None
        self.margin = 10
        self.delay = delay
                
    def update_skill(self):
        for frame in self.frames:
            if self.target:
                if frame.face_direction != self.target.face_direction:
                    frame.surface = flip_x(frame.surface)
                    frame.face_direction = self.target.face_direction
            
                if self.target.face_direction == "right":
                    frame.rect.left = self.target.rect.right -self.margin 
                    frame.rect.centery = self.target.rect.centery
                elif self.target.face_direction == "left":
                    frame.rect.right = self.target.rect.left + self.margin
                    frame.rect.centery = self.target.rect.centery
        if self.active:
            self.counter += 1
            if self.counter >= self.delay:
                self.counter = 0 # reset frame counter
                self.active_index = (self.active_index) % len(self.frames)
                self.current_frame = self.frames[self.active_index]
                print("current frame: ", self.active_index)
                self.active_index += 1
                if self.active_index >= len(self.frames):
                    self.active_index = 0
                    self.close_skill()
            
    def cast_skill(self, target):
        self.active = True
        self.target = target
        for frame in self.frames:
            frame.face_direction = target.face_direction
        
    def close_skill(self):
        print("deactive dipanggil")
        self.active = False