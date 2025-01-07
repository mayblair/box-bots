# CLASSES
import pygame
from settings import var

""" Class for an instructional image that can be open or closed 
    in the workspace. Displayed on the top of the workspace. Only 
    one step in the group can be open at any time. """
class Step(pygame.sprite.Sprite):
    def __init__(self, image, point, num, state = "closed"):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.num = num
        # Assign the state to be closed by default
        self._state = state
        # Pass in the image, and resize it
        self.image = pygame.image.load(image).convert_alpha()
        self._x = point[0]
        self._y = point[1]
        
        self.rect = self.image.get_rect()

    def update(self, events):
        updated = False
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()
                        updated = True
        return updated

    def on_click(self):
        global var
        var.step._state = "unselected"
        var.step.draw()
        self._state = "selected"
        self.draw()
        var.step = self
    
    def draw(self, screen = var.screen):
        # Determine if step is open and to be highlighted or closed and to be
        # small and shadowed.
        if self._state == "unselected":
            # Draw a dark grey background rectangle with a small image
            image_surf = pygame.transform.smoothscale(self.image, (60, 60))
            r_width, r_height  = image_surf.get_size()
            background = pygame.Rect(self._x - r_width//2 - 10, self._y - r_height//2 - 10, \
                r_width + 20, r_height + 20)
            pygame.draw.rect(screen, var.more_grey, background, 0, 5)
        elif self._state == "selected":
            image_surf = pygame.transform.smoothscale(self.image, (140, 140))
            r_width, r_height  = image_surf.get_size()
            # Create large light background offset from image
            light_background = pygame.Rect(self._x - r_width//2 - 35, \
                self._y - r_height//2 - 10, r_width + 70, r_height + 20)
            # Create border around the background
            border = pygame.Rect(self._x - r_width//2 - 45, \
                self._y - r_height//2 - 20, r_width + 90, r_height + 40)
            pygame.draw.rect(screen, var.mid_grey, border, 0, 5)
            pygame.draw.rect(screen, var.light_grey, light_background, 0, 5)
        else:
            print("no step state assigned yet")
            pygame.quit()

        # Re-position the image
        self.rect = image_surf.get_rect()
        self.rect.center = self._x, self._y

        # Paste the image on the surface
        screen.blit(image_surf, self.rect)


""" Class for an image of a material that can selected or unselected
    on the left side of the screen. Once selected, the material can 
    be added to the canvas with a click and drag gesture. Only one 
    tool in the group can be selected at any time. """
class Tool(pygame.sprite.Sprite):
    def __init__(self, image, point, toolsizex, toolsizey, state = "unselected", shapes = [], rev_img = None):
        # Call the parent class (Sprite) constructor
        super().__init__()
    
        self._size = 100
        self.toolsizex = toolsizex
        self.toolsizey = toolsizey
        self._x = point[0]
        self._y = point[1]
        self._state = state
        self.rotation = 0

        # Pass in the image, and resize it
        self.image_load = pygame.image.load(image).convert_alpha()
        # add the primary image as first in the shapes list
        self.shapes = [self.image_load]
        self.num_shape = 0
        self.len_shapes = 0
        
        if shapes != []:
            self.len_shapes = len(shapes)
            for img in shapes:
                img_load = pygame.image.load(img).convert_alpha()
                self.shapes.append(img_load)

        # for reverse of images (rotation == 2)
        self.rev_img_load = rev_img
        if rev_img:
            self.rev_img_load = pygame.image.load(rev_img).convert_alpha()

        if var.final:
            self.toolsizey = toolsizey * 0.7
            self.toolsizex = toolsizex * 0.9
            
        self.image = pygame.transform.smoothscale(self.image_load, \
                (self._size, self._size)).convert_alpha()
        
        # Re-position the image
        self.rect = self.image.get_rect()
        self.rect.center = self._x, self._y

    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    def on_click(self):
        global var
        if var.tool:
            var.tool._state = "unselected"
            var.tool.draw()
        var.tool = None
        # if add operation is selected, draw tool
        if var.op.name == "add" and var.op._state == "selected":
            self._state = "selected"
            self.draw()
            var.tool = self
        # if any other operation is selected
        elif var.op.name == "remove" and var.op._state == "selected":
            for op in var._operations:
                if op.name == "add":
                    op._state = "prompted"
                    op.draw()
                    pygame.display.flip()
                    pygame.time.delay(100)
                    op._state = "unselected"
                    op.draw()
        else:
            print("no operation selected")

    def draw(self, screen = var.screen):
        # Determine if step is open and to be highlighted or closed and to be
        # small and shadowed.
        if self._state == "unselected":
            # print("draw unselected")
            # Draw a light grey background circle with dark grey border
            pygame.draw.circle(screen, var.less_light_grey, (self._x, self._y), self._size-15)
        elif self._state == "selected":
            # print("draw selected")
            # Draw a white background circle
            pygame.draw.circle(screen, var.most_grey, (self._x, self._y), self._size-10)
            pygame.draw.circle(screen, var.white, (self._x, self._y), self._size-15)
        else:
            print("no tool state assigned yet")
            pygame.quit()
        # Paste the image on the surface
        var.screen.blit(self.image, self.rect)


""" Class for an operation image that can be open or closed 
    in the workspace. Displayed on the bottom of the workspace.
    Once selected, the operation (add or remove) can 
    be used on the canvas with a click and drag gesture. Only one 
    operation in the group can be selected at any time."""
class Operation(pygame.sprite.Sprite):
    def __init__(self, image, point, name, state = "unselected"):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._size = 80
        self._x = point[0]
        self._y = point[1]
        self.name = name
        self.cursor_size = 12
        self._state = state
        # Pass in the image, and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()
        self.rect.center = self._x, self._y

    def update(self, events):
        updated = False
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()
                        updated = True
        return updated

    def on_click(self):
        if var.op:
            var.op._state = "unselected"
            var.op.draw()
        self._state = "selected"
        self.draw()
        var.op = self
            

    def draw(self, screen = var.screen):
        # Determine if step is open and to be highlighted or closed and to be
        # small and shadowed.
        if self._state == "unselected":
            # Draw a dark grey background rectangle with a small image
            pygame.draw.circle(screen, var.more_grey, (self._x, self._y), self._size-28)
        elif self._state == "selected":
            # Create large light background offset from image
            pygame.draw.circle(screen, var.white, (self._x, self._y), self._size-28)
        elif self.name == "add" and self._state == "prompted":
            print("prompt")
            pygame.draw.circle(screen, var.most_grey, (self._x, self._y), self._size-28)
        else:
            print("no operation state assigned yet")
            pygame.quit()

        # Paste the image on the surface
        screen.blit(self.image, self.rect)


""" Class for an undo / redo button """
class UndoRedo(pygame.sprite.Sprite):
    def __init__(self, image, name, state = "unselected"):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # self.old_time = 0
        self._size = 40
        self.name = name
        self._image = image
        self._state = state
        # Pass in the image, and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()

    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    def on_click(self):
        global var
        step_num = var.step.num
        if self.name == "undo":
            if var.canvas[step_num]:
                var.redo[step_num] += [var.canvas[step_num][-1]]
                var.canvas[step_num] = var.canvas[step_num][:-1]
                
        elif self.name == "redo":
            if var.redo[step_num]:
                var.canvas[step_num] += [var.redo[step_num][-1]]
                var.redo[step_num] = var.redo[step_num][:-1]
        
        # self._state = "selected"
        # self.draw()
    
    def draw(self, screen = var.screen):
        # Draw undo/redo button with appropriate location and image
        if self.name == "redo":
            pygame.draw.circle(var.screen, var.more_grey, (var.width-90, var.height-70), 30)
            self.rect.center = var.width-90, var.height-70
        elif self.name == "undo":
            pygame.draw.circle(var.screen, var.more_grey, (var.width-160, var.height-70), 30)
            self.rect.center = var.width-160, var.height-70
        screen.blit(self.image, self.rect)


""" Class for an arrow button to go to next toolbar screen """
class BarButton(pygame.sprite.Sprite):
    def __init__(self, image, name, state = "unselected"):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._size = 40
        self.name = name
        self._image = image
        self._state = state
        # Pass in the image, and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()

    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    def on_click(self):
        # advance tool screen depending on if up or down arrow is selected
        if self.name == "up" and var.tool_screen > 0:
            var.tool_screen -= 1
                
        elif self.name == "down" and var.tool_screen < len(var._tools) - 1:
            var.tool_screen += 1

        if var.tool:
            var.tool._state = "unselected"
            var.tool = None
        
        self._state = "selected"
        self.draw()
    

    def draw(self, screen = var.screen):
        # Draw undo/redo button with appropriate location and image        
        if self.name == "up":
            pygame.draw.circle(var.screen, var.mid_grey, (280, 70), 30)
            self.rect.center = 280, 68
        elif self.name == "down":
            pygame.draw.circle(var.screen, var.mid_grey, (280, var.height-70), 30)
            self.rect.center = 280, var.height-68
        screen.blit(self.image, self.rect)
        

""" Class for an rotate button to rotate a tool 90 degrees clockwise """
class Rotate(pygame.sprite.Sprite):
    def __init__(self, image, state = "unselected"):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._size = 50
        self._image = image
        self._state = state
        # Pass in the image, and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()

    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    def on_click(self):
        if var.tool:
            var.tool.rotation += 1
            if var.tool.rotation == 8:
                var.tool.rotation = 0
    
    def draw(self, screen = var.screen):
        pygame.draw.circle(var.screen, var.more_grey, \
                           (var.width - 980, var.height - 130), 50)
        self.rect.center = var.width - 980, var.height - 130
        screen.blit(self.image, self.rect)


""" Class for an reorder button to move the most recently drawn
 tool from the top layer to the bottom layer """
class Reorder(pygame.sprite.Sprite):
    def __init__(self, image, state = "unselected"):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._size = 60
        self._image = image
        self._state = state
        # Pass in the image, and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()

    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    def on_click(self):
        current_canv = var.canvas[var.step.num]
        if current_canv:
            recent = current_canv[-1]
            copy_canv = [recent] + current_canv[:len(current_canv) - 1]
            var.canvas[var.step.num] = copy_canv

        # if current_canv:
        #     copy_canv = current_canv
        #     recent = copy_canv[-1]
        #     while recent[0] == "remove":
        #         copy_canv = [recent] + copy_canv[:len(current_canv) - 1]
        #         recent = copy_canv[-1]
        #         # print(copy_canv)
        #     copy_canv = [recent] + copy_canv[:len(current_canv) - 1]
        #     var.canvas[var.step.num] = copy_canv
    

    def draw(self, screen = var.screen):
        pygame.draw.circle(var.screen, var.more_grey, \
                           (var.width - 325, var.height - 130), 50)
        self.rect.center = var.width - 325, var.height - 130
        screen.blit(self.image, self.rect)
        

""" Class for an fold button to cycle through the folded shapes
 of each tool """
class Fold(pygame.sprite.Sprite):
    def __init__(self, image, state = "unselected"):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._size = 50
        self._image = image
        self._state = state
        # Pass in the image, and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()

    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    def on_click(self):
        if var.tool.num_shape == var.tool.len_shapes:
            var.tool.num_shape = 0
        else:
            var.tool.num_shape += 1

    def draw(self, screen = var.screen):
        pygame.draw.circle(var.screen, var.more_grey, \
                           (var.width - 850, var.height - 130), 50)
        self.rect.center = var.width - 850, var.height - 130
        screen.blit(self.image, self.rect)