import pygame
from entities import Entity

class FlexContainer:
    def __init__(self, width = 0, height = 0, column = False, gap = 0, gap_x = None, gap_y = None, padding = 0,padding_x =None, padding_y = None, allign = None):
        self.gap = gap
        self.gap_x = gap_x
        self.gap_y = gap_y
        self.padding = padding
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.column = column
        self.width = width
        self.height = height
        self.allign = None
        self.container = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        self.children: list[Entity] = []
        self.set_size()
        self.set_childern()
        
    def set_size(self):
        if not self.padding: self.padding = 0
        if not self.padding_x: self.padding_x = self.padding
        if not self.padding_y: self.padding_y = self.padding
        
        if not self.gap: self.gap = 0
        if not self.gap_x: self.gap_x = self.gap
        if not self.gap_y: self.gap_y = self.gap
        
        if self.column:
            for child in self.children:
                self.height += child.rect.height
                if child.rect.width > self.width: self.width = child.rect.width
            self.height += self.padding_y*2 + self.gap_y* (len(self.children)-1)
                
        else: 
            for child in self.children:
                self.width += child.rect.width
                if child.rect.height > self.height: self.height = child.rect.height
            self.width += self.padding_x*2 + self.gap_x* (len(self.children)-1)
        self.update_container()
            
    def update_container(self):
        self.container = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
                
    def add_child(self, child: Entity):
        if self.column: 
            if not self.children: self.height += child.rect.height
            else: self.height += child.rect.height + self.gap_y
        else:
            if not self.children: self.width += child.rect.width
            else: self.width += child.rect.width + self.gap_x
            
        self.children.append(child)
        self.set_childern()
        self.update_container()
        
    def set_childern(self):
        first = True
        prev_size = 0
        if not self.column:
            for child in self.children:
                if first:
                    child.rect.left = self.padding_x
                else:
                    child.rect.left = self.gap_x + prev_size
                prev_size = child.rect.width
                first = False
                
        elif self.column:
            for child in self.children:
                if first:
                    child.rect.top = self.padding_y
                else:
                    child.rect.top = self.gap_y + prev_size
                prev_size = child.rect.height
                first = False
        