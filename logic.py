# LOGIC for main program
import pygame as pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from settings import var
from classes import Step, Operation, Tool, UndoRedo, BarButton, Rotate

undo_label = None
redo_label = None

""" Takes a list of image file names as input and displays them as tools on
    the lefthand side of the screen """
def init_toolbar(tools, sizes):
    print("displaying tools...\n")
    # Begin tool list on top left side of screen
    location = (130, 150)
    var.tool_screen = 0
    for count, image in enumerate(tools):
        if "rubber" in image:
            my_tool = Tool(image, (location[0], location[1] + 200*(count%4)), sizes[count], sizes[count], alt_img='images/tools/rubber_alt.png')
        elif "bottlecap" in image:
            my_tool = Tool(image, (location[0], location[1] + 200*(count%4)), sizes[count], sizes[count], rev_img='images/tools/bottlecaprev.png')
        else:
            my_tool = Tool(image, (location[0], location[1] + 200*(count%4)), sizes[count], sizes[count])
        if count == 0:
            my_tool._state = "selected"
            var.tool = my_tool
        else:
            my_tool._state = "unselected"
        # make a sprite group for every screen of toolbar (4)
        if count % 4 == 0:
            var._tools += [pygame.sprite.Group()]
        # add tools to the appropriate tool screen list
        if count < 4:
            var._tools[0].add(my_tool)
        elif count < 8:
            var._tools[1].add(my_tool)
        elif count < 12:
            var._tools[2].add(my_tool)

""" Populates the toolbar list with a final toolbar containing
    the contents of each step's canvas """
def final_toolbar():
    global var
    location = (130, 150)
    var.tool_screen = 0
    reset_tool()
    # create final toolbar with contents of every canvas except the last one
    for index, step in enumerate(var._steps):
        if index == len(var._steps) - 1:
            break
        transparent = pygame.Surface(var.dimensions, pygame.SRCALPHA)
        transparent.fill(var.transparent)
        screen = draw_canvas(step.num, transparent)
        transparent.blit(screen, (0,0))
        dimensions = (var.width-590, var.height)
        rect = pygame.Rect(400, 0, dimensions[0], dimensions[1])
        sub = screen.subsurface(rect).convert_alpha()
        r_image = pygame.transform.rotate(sub, 10).convert_alpha()
        _image = pygame.transform.smoothscale(r_image, (dimensions[0], dimensions[1] * 0.7)).convert_alpha()       
        img_name = "images/tools/steps/step" + str(step.num) + ".png"
        pygame.image.save(_image, img_name)
        my_tool = Tool(img_name, (location[0], location[1] + 200*(index%4)), 1000, 1000)
        my_tool._state = "unselected"
        # make a sprite group for every screen of toolbar (4)
        if index % 4 == 0:
            var._final_tools += [pygame.sprite.Group()]
        # add tools to the appropriate tool screen list
        if index < 4:
            var._final_tools[0].add(my_tool)
        elif index < 8:
            var._final_tools[1].add(my_tool)
        elif index < 12:
            var._final_tools[2].add(my_tool)


""" Takes a list of image file names as input and displays them as steps
    on the top of the screen / workspace. One of the steps is highlighted to 
    signify it is the current build goal. """
def init_steps(image_list):
    print("displaying steps...\n")
    # Calculate space between steps from length of instruction
    spacing = (var.width - 470) / len(image_list)
    # Set Location of steps to be centered above the workspace
    location = (500, 100)
    
    # Begin step display with first step highlighted
    for count, image in enumerate(image_list):
        my_step = Step(image, (location[0] + spacing * count, location[1]), count)
        if count == 0:
            my_step._state = "selected"
            var.step = my_step
        else:
            my_step._state = "unselected"
        var._steps.add(my_step)
        var.canvas[my_step.num] = []
        var.redo[my_step.num] = []


""" Takes a list of image file names as input and displays them as operations
    on the bottom of the screen / workspace """
def init_operations(operations, names):
    print("displaying operations...\n")
    # Begin operation list on bottom of workspace
    location = ((((var.width + 350) / 2) - (len(operations) * 50)), var.height - 100)
    for count, image in enumerate(operations):
        this_op = Operation(image, (location[0] + 150*count, location[1]), names[count])
        if count == 0:
            this_op._state = "selected"
            var.op = this_op
        else:
            this_op._state = "unselected"
        var._operations.add(this_op)


""" Displays undo and redo buttons on the bottom right of the screen / workspace"""
def init_undo_redo():
    global undo_label
    global redo_label
    print("displaying undo/redo...\n")
    redo = UndoRedo('images/redo.png', "redo")
    undo = UndoRedo('images/undo.png', "undo")
    var._undo_redo.add(redo)
    var._undo_redo.add(undo)
    undo_label = TextBox(var.screen, var.width-185, var.height-40, 55, 25, fontSize=15, borderThickness=0, colour=var.light_grey)
    undo_label.setText("Undo")
    undo_label.disable()
    redo_label = TextBox(var.screen, var.width-110, var.height-40, 55, 25, fontSize=15, borderThickness=0, colour=var.light_grey)
    redo_label.setText("Redo")
    redo_label.disable()


""" Displays up and down arrow buttons on the top and bottom of the toolbar """
def init_bar_buttons():
    print("displaying bar buttons...\n")
    up = BarButton('images/up-arrow.png', "up")
    down = BarButton('images/down-arrow.png', "down")
    var._bar_buttons.add(up)
    var._bar_buttons.add(down)


""" Displays slider on the bottom left of screen with a textbox """
def init_slider():
    var.slider = Slider(var.screen, var.width-250, var.height-160, 150, 15, \
                    min=5, max=80, step=1, initial=12)
    box = TextBox(var.screen, var.width-75, var.height-160, 35, 25, fontSize=15)
    box.disable()
    var.text_box = box


""" Displays rotation button and label on the bottom left of screen """
def init_rotate():
    var.rotate = Rotate('images/rotate.png')
    var.rotate_label = TextBox(var.screen, var.width - 296, var.height - 80, 55, 25, fontSize=15, borderThickness=0, colour=var.light_grey)
    var.rotate_label.setText("Rotate")
    var.rotate_label.disable()


""" Adds appropriate up/down bar buttons to display depending on the
    toolscreen """
def toggle_bar_buttons():
    var.active_bar_buttons = []
    for button in var._bar_buttons:
        # if on the last toolbar screen, only display up arrow
        if var.tool_screen == len(var._tools) - 1:
            if button.name == "up":
                var.active_bar_buttons = [button]
                button.draw(var.screen)
        # if on the first toolbar screen, only display down arrow
        elif var.tool_screen == 0:
            if button.name == "down":
                var.active_bar_buttons = [button]
                button.draw(var.screen)
        else:
            var.active_bar_buttons += button
            button.draw(var.screen)


""" Resets the state of var.tool to be None """
def reset_tool():
    global var
    if var.tool:
        print("reset")
        var.tool._state = "unselected"
        var.tool.draw()
        var.tool = None

""" Selects the first tool in the toolbar if add operation is selected
    and unselects any tools if remove is selected """
def check_op():
    toolbar = var._tools if not var.final else var._final_tools
    for index,tool in enumerate(toolbar[var.tool_screen]):
        # if "add" operation is selected, select first tool
        if var.op.name == "add" and not var.tool and index == 0:
            tool._state = "selected"
            tool.draw()
            var.tool = tool
        # if "remove" operation is selected, unselect tool
        elif var.op.name == "remove" and var.tool and index == 0:
            var.tool._state = "unselected"
            var.tool.draw()
            var.tool = None
        break


""" Displays opaque tool where the mouse is located to show tool 
    to add to screen when clicked """
def draw_shadow_tool(p, tool, screen = var.screen):
    image = tool.rev_img_load if tool.rotation == 2 and tool.rev_img_load else tool.image_load
    image = tool.alt_image_load if tool.alt_image_load else image
    # transparent = pygame.Surface(var.dimensions, pygame.SRCALPHA)
    # transparent.fill(var.transparent)
    r_image = pygame.transform.rotate(image, tool.rotation * 90).convert_alpha()
    r_image.set_alpha(100)
    _image = pygame.transform.smoothscale(r_image, \
        (tool.toolsizex, tool.toolsizey)).convert_alpha()
    # Re-position the image
    rect = _image.get_rect()
    rect.center = p[0], p[1]
    # crop image
    # portion_dim = (var.width-590, var.height)
    # portion = pygame.Rect(400, 0, portion_dim[0], portion_dim[1])
    # transparent.blit(_image, rect)
    # sub = transparent.subsurface(portion).convert_alpha()
    screen.blit(_image, rect)


""" Displays opaque circle where the mouse is located to show area 
    to remove from screen when clicked """
def draw_shadow(p, screen = var.screen):
    transparent = pygame.Surface((var.width, var.height), pygame.SRCALPHA)
    transparent.fill(var.transparent)
    pygame.draw.circle(transparent, var.transparent_grey, p, var.slider.getValue())
    screen.blit(transparent, (0,0))


""" Draw slider and textbox on the bottom left of screen """
def draw_slider():
    var.text_box.setText(var.slider.getValue())
    var.slider.show()
    var.text_box.show()
    var.slider.draw()
    var.text_box.draw()


""" Draw rotation button on the bottom left of screen """
def draw_rotate():
    var.rotate.draw()
    var.rotate_label.setText("Rotate")
    var.rotate_label.draw()


""" Draw screen, including background and buttons """
def draw_screen():
    # Fill it in with light grey
    var.screen.fill(var.light_grey)
    # Draw toolbar rectangle
    background = pygame.Rect(0, 0, 345, var.height)
    pygame.draw.rect(var.screen, var.more_grey, background)
    # Draw lines to section canvas from steps and operations
    pygame.draw.line(var.screen, var.more_grey, (365, 210), (var.width - 50, 210), 4)
    pygame.draw.line(var.screen, var.more_grey, (365, var.height - 190), (var.width - 50, var.height - 190), 4)
    # Draw undo/redo and toolbar buttons
    draw_buttons()


""" Draw buttons, including bar buttons and undo/redo buttons """
def draw_buttons():
    # Draw undo/redo buttons
    for do in var._undo_redo:
        do.draw(var.screen)
    undo_label.draw()
    redo_label.draw()
    # toggle and draw toolbar buttons
    toggle_bar_buttons()
    for button in var.active_bar_buttons:
        button.draw(var.screen)



""" Draw buttons, including steps, tools and operations. """
def draw_variables():
    toolbar = var._tools if not var.final else var._final_tools
    for op in var._operations:
        op.draw(var.screen)
    for step in var._steps:
        step.draw(var.screen)
    for tool in toolbar[var.tool_screen]:
        # print(tool._state)
        tool.draw(var.screen)


""" Draw existing materials onto screen, including additions and removals """
def draw_canvas(num, screen = var.screen):
    for addition in var.canvas[num]:
        if addition[0] == "remove":
            remove((addition[1], addition[2]), addition[3], screen)
        else:
            add_tool((addition[1], addition[2]), addition[0], addition[3], screen)
    return screen


""" Draw one new tool addition onto the canvas """
def draw_new_tool():
    # verify the most receent addition the canvas is an addition
    addition = var.canvas[var.step.num][-1]
    if addition[0] == "remove":
        print("cannot add removal of size " + addition[0] + " to canvas")
    else:
        # add selected tool (position, name, and rotation) to canvas at selected step
        add_tool((addition[1], addition[2]), addition[0], addition[3])


""" Draw one new removal onto the canvas """
def remove_new_circle():
    # verify the most receent addition the canvas is a removal
    subtraction = var.canvas[var.step.num][-1]
    if subtraction[0] == "remove":
        # remove at position and size from canvas at selected step
        remove((subtraction[1], subtraction[2]), subtraction[3])
    else:
        print("cannot remove " + subtraction[0] + " from canvas")


""" Takes a point and a tool as input, resizes the image, and places 
    an image of the tool on the screen / workspace """
def add_tool(position, tool, rotation, screen=var.screen):
    print("adding tool...\n")
    image = tool.alt_image_load if tool.alt_image_load else tool.image_load
    image = tool.rev_img_load if rotation == 2 and tool.rev_img_load else image
    r_image = pygame.transform.rotate(image, rotation * 90)
    _image = pygame.transform.smoothscale(r_image, \
            (tool.toolsizex, tool.toolsizey))
    # Re-position the image
    rect = _image.get_rect()
    rect.center = position[0], position[1]
    screen.blit(_image, rect)


""" Takes a point as input and places a circle on the screen / workspace 
    to "remove" material """
def remove(position, size, screen=var.screen):
    print("removing material...\n")
    transparent = pygame.Surface((100, 100), pygame.SRCALPHA)
    transparent.fill(var.transparent)
    # pygame.draw.circle(transparent, var.light_grey, position, size)
    pygame.draw.circle(screen, var.transparent, position, size)
    screen.blit(transparent, (position[0], position[1]))
    # screen.blit(transparent, (position[0], position[1]))