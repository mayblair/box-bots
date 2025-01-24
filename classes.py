# CLASSES
import pygame
from settings import var
from pygame_widgets.textbox import TextBox

""" Class for an instructional image that can be open or closed 
    in the workspace. Displayed on the top of the workspace. Only 
    one step in the group can be open at any time. """
class Step(pygame.sprite.Sprite):

    """ Initialize a Step with a path to an image, an (x,y) coordinate location, 
        a number associated with order, a text label, and an optional state. """
    def __init__(self, image, point, num, text, state = "closed"):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.num = num
        # Assign the state to be closed by default
        self._state = state
        # Pass in the image and store its location
        self.image = pygame.image.load(image).convert_alpha()
        self._x = point[0]
        self._y = point[1]
        self.rect = self.image.get_rect()
        # create a label for the step according to its text 
        if text == "Final Build":
            self.text = TextBox(var.screen, self._x - 40, self._y - 55, 55, 0, \
                            fontSize=15, borderThickness=0, colour=var.light_grey)
        else:
            self.text = TextBox(var.screen, self._x - 25, self._y - 55, 55, 0, \
                            fontSize=15, borderThickness=0, colour=var.light_grey)
        self.text.setText(text)
        self.text.disable()

    """ Method thats decides from mouse events if Sprite was clicked on """
    def update(self, events):
        updated = False
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()
                        updated = True
        return updated

    """ Operate on Sprite and perform action associated with click """
    def on_click(self):
        global var
        # unselect the previously selected step
        var.step._state = "unselected"
        var.step.draw()
        # select the sprite that is clicked on
        self._state = "selected"
        var.step = self
    
    """ Draw the Step according to its state and the state of the program """
    def draw(self, screen = var.screen):
        # Determine if step is open and to be highlighted or closed
        # and to be small and shadowed with a label.
        if self._state == "unselected":
            # if final step, color background yellow instead of purple
            if self.text.getText() == "Final Build":
                back_color = var.yellow_grey
            else:
                back_color = var.purple_grey
            # Draw a darker background with a small image
            image_surf = pygame.transform.smoothscale(self.image, (70, 70))
            r_width, r_height = image_surf.get_size()
            background = pygame.Rect(self._x - r_width//2 - 10, self._y - r_height//2 - 10, \
                r_width + 20, r_height + 20)
            pygame.draw.rect(screen, back_color, background, 0, 5)
            # Label the step
            self.text.draw()
        elif self._state == "selected":
            # if final step, color background yellow instead of purple
            if self.text.getText() == "Final Build":
                back_color = var.yellow_light
            else:
                back_color = var.purple_light
            image_surf = pygame.transform.smoothscale(self.image, (170, 170))
            r_width, r_height = image_surf.get_size()
            # Create large light background offset from image
            light_background = pygame.Rect(self._x - r_width//2 - 10, \
                self._y - r_height//2 - 10, r_width + 20, r_height + 20)
            # Create border around the light background
            border = pygame.Rect(self._x - r_width//2 - 15, \
                self._y - r_height//2 - 15, r_width + 30, r_height + 30)
            pygame.draw.rect(screen, var.purple_dark, border, 0, 5)
            pygame.draw.rect(screen, back_color, light_background, 0, 5)
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

    """ Initialize a Tool with a path to an image, an (x,y) coordinate location, 
        a number representing width, a number representing height, and optional 
        inputs. The optional inputs are a state of selection, a list of alternate
        paths to shapes for folding operation, a path to a reverse image for 
        upside-down rotations, and a flag to track if the tool is foldable or not. """
    def __init__(self, image, point, toolsizex, toolsizey, state = "unselected", \
                 shapes = [], rev_img = None, foldable = False):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Set final toolbar images to a larger size
        self._size = 100 if not var.final else 150
        self.toolsizex = toolsizex
        self.toolsizey = toolsizey
        self._x = point[0]
        self._y = point[1]
        self._state = state
        self.foldable = foldable
        self.rotation = 0

        # Pass in the image, and resize it
        self.image_load = pygame.image.load(image).convert_alpha()
        # Add the primary image as first in the shapes list
        self.shapes = [self.image_load]
        # Index into shapes to choose the right image
        self.num_shape = 0
        # Total length of shape options
        self.len_shapes = 0
        
        # If there are shapes, load the images
        if shapes != []:
            self.len_shapes = len(shapes)
            for img in shapes:
                img_load = pygame.image.load(img).convert_alpha()
                self.shapes.append(img_load)

        # Load reverse image if there one provided (rotation == 4)
        self.rev_img_load = rev_img
        if rev_img:
            self.rev_img_load = pygame.image.load(rev_img).convert_alpha()
        # Skew the width and height if tool is part of final toolbar
        if var.final:
            self.toolsizey = toolsizey * 0.75
            self.toolsizex = toolsizex * 0.95
        # Load the tool image, resize it, and reposition it 
        self.image = pygame.transform.smoothscale(self.image_load, \
                (self._size, self._size)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self._x, self._y

    """ Method thats decides from mouse events if Sprite was clicked on """
    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    """ Operate on Sprite and perform action associated with click """
    def on_click(self):
        global var
        # unselect the previous tool
        if var.tool:
            var.tool._state = "unselected"
            var.tool.num_shape = 0
            var.tool.rotation = 0
        var.tool = None
        # if user is in the add operation, select this tool
        if var.op.name == "add" and var.op._state == "selected":
            self._state = "selected"
            var.tool = self

    """ Draw the Tool according to its state """
    def draw(self, screen = var.screen):
        # Determine if step is open and to be highlighted or closed and to be
        # small and shadowed.
        if self._state == "unselected":
            # Draw a light grey background circle with dark grey border
            pygame.draw.circle(screen, var.yellow_grey, (self._x, self._y), 85)
        elif self._state == "selected":
            # Draw a white background circle
            pygame.draw.circle(screen, var.yellow_dark, (self._x, self._y), 90)
            pygame.draw.circle(screen, var.yellow_light, (self._x, self._y), 85)
        elif self._state == "darkened":
            # Draw a darkened circle
            pygame.draw.circle(screen, var.mostly_grey, (self._x, self._y), 85)
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

    """ Initialize an Operation with a path to an image, an (x,y) coordinate location, 
        a name (either add or remove), and an optional state of selection. """
    def __init__(self, image, point, name, state = "unselected"):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._size = 75
        self._x = point[0]
        self._y = point[1]
        self.name = name
        self.cursor_size = 12
        self._state = state
        # Pass in the image and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()
        self.rect.center = self._x, self._y

    """ Method thats decides from mouse events if Sprite was clicked on """
    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    """ Operate on Sprite and perform action associated with click """
    def on_click(self):
        # unselect previous operation
        if var.op:
            var.op._state = "unselected"
        # select operation that is clicked on
        self._state = "selected"
        var.op = self
            

    """ Draw the Operation according to its state """
    def draw(self, screen = var.screen):
        # Determine if step is open and to be highlighted or closed and to be
        # small and shadowed.
        if self._state == "unselected":
            # Draw a dark grey background rectangle with a small image
            pygame.draw.circle(screen, var.purple_mid, (self._x, self._y), self._size-25)
        elif self._state == "selected":
            # Create large light background offset from image
            pygame.draw.circle(screen, var.purple_dark, (self._x, self._y), self._size-25)
            pygame.draw.circle(screen, var.purple_light, (self._x, self._y), self._size-30)
        else:
            print("no operation state assigned yet")
            pygame.quit()

        # Paste the image on the surface
        screen.blit(self.image, self.rect)


""" Class for an undo / redo button """
class UndoRedo(pygame.sprite.Sprite):

    """ Initialize an UndoRedo with a path to an image and a name 
        (either undo or redo). """
    def __init__(self, image, name):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        self._size = 35
        self.name = name
        self._image = image
        # Pass in the image and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()

    """ Method thats decides from mouse events if Sprite was clicked on """
    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    """ Operate on Sprite and perform action associated with click """
    def on_click(self):
        global var
        step_num = var.step.num
        if self.name == "undo":
            # if there is a material to undo on the current step canvas
            if var.canvas[step_num]:
                # add the last material used to the redo dictionary
                var.redo[step_num] += [var.canvas[step_num][-1]]
                # remove the last material added to the canvas at the step
                var.canvas[step_num] = var.canvas[step_num][:-1]
                
        elif self.name == "redo":
            # if there is a material to redo on the current step canvas
            if var.redo[step_num]:
                # add the last material added to the redo dictionary to the canvas
                var.canvas[step_num] += [var.redo[step_num][-1]]
                # remove the last material added to the redo dictionary
                var.redo[step_num] = var.redo[step_num][:-1]
    
    """ Draw the button according to its name """
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

    """ Initialize a BarButton with a path to an image and a name 
        (either up or down). """
    def __init__(self, image, name):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._size = 40
        self.name = name
        self._image = image
        # Pass in the image and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()

    """ Method thats decides from mouse events if Sprite was clicked on """
    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    """ Operate on Sprite and perform action associated with click """
    def on_click(self):
        # choose the correct toolbar to show
        toolbar = var._tools if not var.final else var._final_tools
        # operate click only if the add operation is selected
        if var.op.name == "add":
            # advance tool screen depending on if up or down arrow is selected
            if self.name == "up" and var.tool_screen > 0:
                var.tool_screen -= 1
            # if down is clicked and it is the last screen
            elif self.name == "down" and var.tool_screen < len(toolbar) - 1:
                var.tool_screen += 1
            # if there is a tool selected, unselect it
            if var.tool:
                var.tool._state = "unselected"
                var.tool = None
    
    """ Draw the button according to its name """
    def draw(self, screen = var.screen):
        # Draw undo/redo button with appropriate location and image        
        if self.name == "up":
            pygame.draw.circle(var.screen, var.yellow_dark, (250, 70), 30)
            self.rect.center = 250, 68
        elif self.name == "down":
            pygame.draw.circle(var.screen, var.yellow_dark, (250, var.height-70), 30)
            self.rect.center = 250, var.height-68
        screen.blit(self.image, self.rect)
        

""" Class for an rotate button to rotate a tool 90 degrees clockwise """
class Rotate(pygame.sprite.Sprite):

    """ Initialize a Rotate with a path to an image. """
    def __init__(self, image):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._size = 40
        self._image = image
        # Pass in the image and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()

    """ Method thats decides from mouse events if Sprite was clicked on """
    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    """ Operate on Sprite and perform action associated with click """
    def on_click(self):
        # if there is a tool selected, rotate it by 45 degrees
        if var.tool:
            var.tool.rotation += 1
            # if the tool reaches 360 degrees, change back to 0 degrees
            if var.tool.rotation == 8:
                var.tool.rotation = 0
    
    """ Draw the button with a grey background and a rotate image """
    def draw(self, screen = var.screen):
        pygame.draw.circle(var.screen, var.more_grey, \
                           (var.width - 840, var.height - 100), self._size)
        self.rect.center = var.width - 840, var.height - 100
        screen.blit(self.image, self.rect)


""" Class for an reorder button to move the most recently drawn
 tool from the top layer to the bottom layer """
class Reorder(pygame.sprite.Sprite):

    """ Initialize a Reorder with a path to an image. """
    def __init__(self, image):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._size = 40
        self._image = image
        # Pass in the image and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()

    """ Method thats decides from mouse events if Sprite was clicked on """
    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    """ Operate on Sprite and perform action associated with click """
    def on_click(self):
        current_canv = var.canvas[var.step.num]
        if current_canv:
            # capture the last material added to the canvas at the step
            recent = current_canv[-1]
            # move the recent material to the first postion
            copy_canv = [recent] + current_canv[:len(current_canv) - 1]
            var.canvas[var.step.num] = copy_canv

    """ Draw the button with a grey background and a reorder image """
    def draw(self, screen = var.screen):
        pygame.draw.circle(var.screen, var.more_grey, \
                           (var.width - 320, var.height - 100), self._size)
        self.rect.center = var.width - 320, var.height - 100
        screen.blit(self.image, self.rect)
        

""" Class for an fold button to cycle through the folded shapes
 of each tool """
class Fold(pygame.sprite.Sprite):

    """ Initialize a Fold with a path to an image. """
    def __init__(self, image):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self._size = 40
        self._image = image
        # Pass in the image, and resize it
        image_load = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(image_load, \
            (self._size, self._size))
        # Re-position the image
        self.rect = self.image.get_rect()

    """ Method thats decides from mouse events if Sprite was clicked on """
    def update(self, events):
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.on_click()

    """ Operate on Sprite and perform action associated with click """
    def on_click(self):
        # if there is a tool selected to fold, change tool shape
        if var.tool:
            # if this is the final shape, change to first shape
            if var.tool.num_shape == var.tool.len_shapes:
                var.tool.num_shape = 0
            else:
                var.tool.num_shape += 1

    """ Draw the button with a grey background and a fold image """
    def draw(self, screen = var.screen):
        pygame.draw.circle(var.screen, var.more_grey, \
                           (var.width - 970, var.height - 100), self._size)
        self.rect.center = var.width - 970, var.height - 98
        screen.blit(self.image, self.rect)