from utils import flip_x

class Skill():
    def __init__(self,type,name , frames, delay):
        self.name = name
        self.type = type
        self.active = False
        self.frames = frames
        self.active_index = 0
        self.counter = -1
        self.user = None
        self.margin = 10
        self.delay = delay
        self.damage = 100
        self.hit = set()
    
    def set_hit(self, entity):
        self.hit.add(entity)
    
                
    def update_skill(self):
        
        for frame in self.frames:
            if self.user:
                
                
                if frame.face_direction != self.user.face_direction:
                    frame.surface = flip_x(frame.surface)
                    frame.face_direction = self.user.face_direction
            
                if self.user.face_direction == "right":
                    frame.rect.left = self.user.rect.right -self.margin 
                    frame.rect.centery = self.user.rect.centery
                elif self.user.face_direction == "left":
                    frame.rect.right = self.user.rect.left + self.margin
                    frame.rect.centery = self.user.rect.centery
                    
        if self.active:
            self.counter += 1
            if self.counter >= self.delay:
                self.counter = 0 # reset frame counter
                self.active_index = (self.active_index) % len(self.frames)
                self.current_frame = self.frames[self.active_index]
                self.active_index += 1
                if self.active_index >= len(self.frames):
                    self.active_index = 0
                    self.close_skill()
            
    def cast_skill(self, target):
        self.user = target
        self.active = True
        
    def close_skill(self):
        self.active = False
        self.hit.clear()
