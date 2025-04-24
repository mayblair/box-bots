# LOGIC for main program
import pygame as pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from settings import var
from classes import Step, Operation, Tool, UndoRedo, BarButton, \
    Rotate, Reorder, Fold

undo_label = None
redo_label = None
add_label = None
remove_label = None
tools_label = None

""" Takes a list of image file names as input and displays them as tools on
    the lefthand side of the screen """
def init_toolbar(tools, sizes):
    global tools_label
    print("displaying tools...\n")
    # Label tool list as materials
    tools_label = TextBox(var.screen, 75, 25, 55, 25, \
                        fontSize=18, borderThickness=0, colour=var.more_grey)
    tools_label.setText("Materials")
    tools_label.disable()
    # Begin tool list on top left side of screen
    location = (120, 150)
    var.tool_screen = 0
    for count, image in enumerate(tools):
        if "rubber" in image:
            shapes = []
            for index in range(1, 4):
                shapes.append('images/' + var.project + '/tools/rubber_alt' + str(index) + '.png')
            my_tool = Tool(image, (location[0], location[1] + 200*(count%4)), sizes[count], sizes[count], \
                            shapes = shapes, foldable = True)
        elif "bottlecap" in image:
            my_tool = Tool(image, (location[0], location[1] + 200*(count%4)), sizes[count], sizes[count], \
                           rev_img = 'images/' + var.project + '/tools/bottlecaprev.png')
        elif "cardboard" in image:
            shapes = []
            for index in range(1, 5):
                shapes.append('images/' + var.project + '/tools/cardboard_alt' + str(index) + '.png')
            my_tool = Tool(image, (location[0], location[1] + 200*(count%4)), sizes[count], sizes[count], \
                           shapes = shapes, foldable = True)
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
    location = (120, 150)
    var.tool_screen = 0
    var._final_tools = []
    reset_tool()
    # create final toolbar with contents of every canvas except the final step
    for index, step in enumerate(var._steps):
        if index == len(var._steps) - 1:
            break
        # create transparent surface
        transparent = pygame.Surface(var.dimensions, pygame.SRCALPHA)
        transparent.fill(var.transparent)
        # draw elements from a step's canvas onto the transparent surface
        screen = draw_canvas(step.num, transparent)
        # re-color the light grey "remove" circles to be transparent
        screen.set_colorkey(var.light_grey)
        # draw elements from screen onto the transparent surface
        transparent.blit(screen, (0,0))
        # crop the resulting image
        dimensions = (var.width-590, var.height)
        rect = pygame.Rect(400, 0, dimensions[0], dimensions[1])
        sub = transparent.subsurface(rect).convert_alpha()
        # rotate and scale the resulting image
        r_image = pygame.transform.rotate(sub, 10)
        _image = pygame.transform.smoothscale(r_image, (dimensions[0], dimensions[1] * 0.7))
        # save the image to a file and add to final toolbar
        img_name = 'images/' + var.project + '/tools/final_steps/step' + str(step.num) + '.png'
        pygame.image.save(_image, img_name)
        my_tool = Tool(img_name, (location[0], location[1] + 200*(index%4)), 1000, 1000)
        if index == 0:
            my_tool._state = "selected"
            var.tool = my_tool
        else:
            my_tool._state = "unselected"
        # make a sprite group for every screen of toolbar (4)
        if index % 4 == 0:
            var._final_tools.append(pygame.sprite.Group())
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
    # Calculate space between steps from length of total steps
    spacing = (var.width - 375) / len(image_list)
    # Set Location of steps to be centered above the workspace
    location = (420, 115)
    
    # Begin step display with first step highlighted
    for count, image in enumerate(image_list):
        if count == len(image_list) - 1:
            text = "Final Build"
        else:
            text = "Step " + str(count + 1)
        my_step = Step(image, (location[0] + spacing * count, location[1]), count, text)
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
    global add_label
    global remove_label
    print("displaying operations...\n")
    # Begin operation list on bottom of workspace
    location = ((((var.width + 350) / 2) - (len(operations) * 50)), var.height - 95)
    for count, image in enumerate(operations):
        this_op = Operation(image, (location[0] + 125*count, location[1]), names[count])
        if count == 0:
            this_op._state = "selected"
            var.op = this_op
        else:
            this_op._state = "unselected"
        var._operations.add(this_op)
    # initialize textboxes for add and remove operations
    add_label = TextBox(var.screen, var.width - 660, var.height - 40, 55, 25, \
                                fontSize=15, borderThickness=0, colour=var.light_grey)
    add_label.setText("Add")
    add_label.disable()
    remove_label = TextBox(var.screen, var.width - 540, var.height - 40, 55, 25, \
                                fontSize=15, borderThickness=0, colour=var.light_grey)
    remove_label.setText("Erase")
    remove_label.disable()


""" Displays undo and redo buttons on the bottom right of the screen / workspace"""
def init_undo_redo():
    global undo_label
    global redo_label
    print("displaying undo/redo...\n")
    redo = UndoRedo('images/op_icons/redo.png', "redo")
    undo = UndoRedo('images/op_icons/undo.png', "undo")
    var._undo_redo.add(redo)
    var._undo_redo.add(undo)
    undo_label = TextBox(var.screen, var.width-185, var.height-40, 55, 25, \
                        fontSize=15, borderThickness=0, colour=var.light_grey)
    undo_label.setText("Undo")
    undo_label.disable()
    redo_label = TextBox(var.screen, var.width-110, var.height-40, 55, 25, \
                        fontSize=15, borderThickness=0, colour=var.light_grey)
    redo_label.setText("Redo")
    redo_label.disable()


""" Displays up and down arrow buttons on the top and bottom of the toolbar """
def init_bar_buttons():
    print("displaying bar buttons...\n")
    up = BarButton('images/op_icons/up-arrow.png', "up")
    down = BarButton('images/op_icons/down-arrow.png', "down")
    var._bar_buttons.add(up)
    var._bar_buttons.add(down)


""" Displays slider on the bottom left of screen with a textbox """
def init_slider():
    var.slider = Slider(var.screen, var.width - 1030, var.height - 110, 220, 17, \
                    min=5, max=80, step=1, initial=12, handleColour = var.purple_dark)
    box = TextBox(var.screen, var.width - 940, var.height - 80, 30, 30, fontSize=16)
    box.disable()
    var.text_box = box


""" Displays rotation button and label on the bottom left of screen """
def init_rotate():
    var.rotate = Rotate('images/op_icons/rotate.png')
    var.rotate_label = TextBox(var.screen, var.width - 868, var.height - 50, 55, 25, \
                               fontSize=15, borderThickness=0, colour=var.light_grey)
    var.rotate_label.setText("Rotate")
    var.rotate_label.disable()


""" Displays reorder button and label on the bottom right of screen """
def init_reorder():
    var.reorder = Reorder('images/op_icons/reorder.png')
    var.reorder_label = TextBox(var.screen, var.width - 352, var.height - 50, 55, 25, \
                                fontSize=15, borderThickness=0, colour=var.light_grey)
    var.reorder_label.setText("Reorder")
    var.reorder_label.disable()


""" Displays fold button and label on the bottom left of screen """
def init_fold():
    var.fold = Fold('images/op_icons/fold.png')
    var.fold_label = TextBox(var.screen, var.width - 990, var.height - 50, 55, 25, \
                                fontSize=15, borderThickness=0, colour=var.light_grey)
    var.fold_label.setText("")
    var.fold_label.disable()


""" Adds appropriate up/down bar buttons to display depending on the
    toolscreen """
def toggle_bar_buttons():
    toolbar = var._tools if not var.final else var._final_tools
    var.active_bar_buttons = []
    for button in var._bar_buttons:
        # if on the only toolbar screen, display no buttons
        if len(toolbar) <= 1:
            var.active_bar_buttons = []
        # if on the first toolbar screen, only display down arrow
        elif var.tool_screen == 0:
            if button.name == "down":
                var.active_bar_buttons = [button]
                button.draw(var.screen)
        # if on the last toolbar screen, only display up arrow
        elif var.tool_screen == len(toolbar) - 1:
            if button.name == "up":
                var.active_bar_buttons = [button]
                button.draw(var.screen)
        # if on a toolbar screen neither first or last, display both
        else:
            var.active_bar_buttons += [button]
            button.draw(var.screen)


""" Resets the state of var.tool to be None """
def reset_tool():
    global var
    if var.tool:
        var.tool._state = "unselected"
        var.tool.num_shape = 0
        var.tool.rotation = 0
        var.tool.draw()
        var.tool = None


""" Selects the first tool in the toolbar if add operation is selected
    and unselects any tools if remove is selected """
def check_op():
    toolbar = var._tools if not var.final else var._final_tools
    for index,tool in enumerate(toolbar[var.tool_screen]):
        # if "add" operation is selected, brighten all tools
        if var.op.name == "add" and var.op._state == "selected":
            # select first tool
            if not var.tool and index == 0:
                tool._state = "selected"
                var.tool = tool
            elif tool._state == "darkened":
                tool._state = "unselected"
        # if "remove" operation is selected, darken all tools
        elif var.op.name == "remove" and var.op._state == "selected":    
            # unselect previously selected tool
            if var.tool:
                var.tool.num_shape = 0
                var.tool.rotation = 0
                var.tool = None
            tool._state = "darkened"
        tool.draw()


""" Displays opaque tool where the mouse is located to show tool 
    to add to screen when clicked """
def draw_shadow_tool(p, tool, screen = var.screen):
    image = tool.shapes[tool.num_shape]
    image = tool.rev_img_load if tool.rotation == 4 and tool.rev_img_load else image
    transparent = pygame.Surface(var.dimensions, pygame.SRCALPHA)
    transparent.fill(var.transparent)
    _image = pygame.transform.smoothscale(image, (tool.toolsizex, tool.toolsizey))
    r_image = pygame.transform.rotate(_image, tool.rotation * 45)
    # Re-position the image
    rect = r_image.get_rect()
    rect.center = p[0], p[1]
    transparent.blit(r_image, rect)
    transparent.set_alpha(100)
    screen.blit(transparent, (0,0))


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
    var.slider.draw()
    var.text_box.show()
    var.text_box.draw()


""" Draw rotation button on the bottom left of screen """
def draw_rotate():
    var.rotate.draw()
    var.rotate_label.show()
    var.rotate_label.setText("Rotate")
    var.rotate_label.draw()


""" Draw reorder button on the bottom right of screen """
def draw_reorder():
    var.reorder.draw()
    var.reorder_label.setText("Reorder")
    var.reorder_label.draw()


""" Draw fold button on the bottom left of screen """
def draw_fold():
    var.fold.draw()
    var.fold_label.setText("Fold")
    var.fold_label.show()
    var.fold_label.draw()


""" Draw screen, including background, and undo/redo & toolbar buttons """
def draw_screen():
    # Fill screen in with light grey
    var.screen.fill(var.light_grey)
    # Draw toolbar rectangle
    background = pygame.Rect(0, 0, 305, var.height)
    pygame.draw.rect(var.screen, var.more_grey, background)
    # Draw lines to section canvas from steps and operations
    pygame.draw.line(var.screen, var.more_grey, (335, 230), (var.width - 40, 230), 4)
    pygame.draw.line(var.screen, var.more_grey, (335, var.height - 160), (var.width - 40, var.height - 160), 4)
    # Draw undo/redo and toolbar buttons
    draw_buttons()


""" Draw bar buttons and undo/redo buttons """
def draw_buttons():
    # Draw undo/redo buttons
    for do in var._undo_redo:
        do.draw(var.screen)
    undo_label.draw()
    redo_label.draw()
    tools_label.draw()
    # toggle and draw toolbar buttons
    toggle_bar_buttons()
    for button in var.active_bar_buttons:
        button.draw(var.screen)


""" Draw variables, including steps, tools and operations. """
def draw_variables():
    # set toolbar according to step number
    toolbar = var._tools if not var.final else var._final_tools
    # draw operations, steps, and tools
    for op in var._operations:
        op.draw(var.screen)
    add_label.draw()
    remove_label.draw()
    for step in var._steps:
        step.draw(var.screen)
    for tool in toolbar[var.tool_screen]:
        tool.draw(var.screen)


""" Draw existing materials onto screen, including additions and removals """
def draw_canvas(num, screen = var.screen):
    for addition in var.canvas[num]:
        if addition[0] == "remove":
            remove((addition[1], addition[2]), addition[3], screen)
        else:
            # add selected tool ((x,y), name, rotation, shape, screen) to canvas at selected step
            add_tool((addition[1], addition[2]), addition[0], addition[3], addition[4], screen)
    return screen


""" Takes a point and a tool as input, resizes the image, and places 
    an image of the tool on the screen / workspace """
def add_tool(position, tool, rotation, shape, screen=var.screen):
    print("adding tool...\n")
    image = tool.shapes[shape]
    image = tool.rev_img_load if rotation == 4 and tool.rev_img_load else image
    image = pygame.transform.smoothscale(image, (tool.toolsizex, tool.toolsizey))
    r_image = pygame.transform.rotate(image, rotation * 45)
    # Re-position the image
    rect = r_image.get_rect()
    rect.center = position[0], position[1]
    screen.blit(r_image, rect)


""" Takes a point as input and places a circle on the screen / workspace 
    to "remove" material """
def remove(position, size, screen=var.screen):
    print("removing material...\n")
    transparent = pygame.Surface((var.width, var.height), pygame.SRCALPHA)
    transparent.fill(var.transparent)
    # pygame.draw.circle(screen, var.transparent, position, size)
    pygame.draw.circle(transparent, var.light_grey, position, size)
    screen.blit(transparent, (0,0))


""" Draw one new tool addition onto the canvas """
def draw_new_tool():
    # verify the most recent addition the canvas is an addition
    addition = var.canvas[var.step.num][-1]
    if addition[0] == "remove":
        print("cannot add removal of size " + addition[0] + " to canvas")
    else:
        # add selected tool ((x,y)), name, rotation, shape, screen) to canvas at selected step
        add_tool((addition[1], addition[2]), addition[0], addition[3], addition[4])


""" Draw one new removal onto the canvas """
def remove_new_circle():
    # verify the most recent addition the canvas is a removal
    subtraction = var.canvas[var.step.num][-1]
    if subtraction[0] == "remove":
        # remove at position and size from canvas at selected step
        remove((subtraction[1], subtraction[2]), subtraction[3])
    else:
        print("cannot remove " + subtraction[0] + " from canvas")
