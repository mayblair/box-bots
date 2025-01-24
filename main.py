# PYGAME INTERFACE for modular building instructions with images
import pygame
import pygame_widgets
from pygame.font import *
import os
import sys
from settings import var
from logic import init_operations, init_toolbar, init_steps, \
    init_undo_redo, init_bar_buttons, final_toolbar, reset_tool, \
    draw_screen, draw_canvas, draw_new_tool, init_rotate, draw_rotate, \
    draw_variables, remove_new_circle, check_op, init_slider, draw_slider, \
    draw_shadow, draw_shadow_tool, init_reorder, draw_reorder, \
    init_fold, draw_fold


""" Process mouse events to implement interface logic """
def process_events(events):
    global var
    global slider
    global running
    for event in events: 
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get mouse position and select normal or final toolbar
            x, y = pygame.mouse.get_pos()
            toolbar = var._tools if not var.final else var._final_tools
            # CLICK ON CANVAS
            if (var.width-100 > x > 350 and 630 > y > 230):
                # store tool info in canvas dictionary under selected step
                if var.op.name == "add" and var.tool:
                    var.canvas[var.step.num] += [(var.tool, x, y, var.tool.rotation, var.tool.num_shape)]
                    draw_new_tool()
                # store removed circle in dictionary under selected step
                elif var.op.name == "remove":
                    # only remove material if there is material on canvas
                    if var.canvas[var.step.num]:
                        var.canvas[var.step.num] += [("remove", x, y, var.slider.getValue())]
                        remove_new_circle()
            # CLICK ON OPERATIONS
            elif (var.width - 20 > x > 350 and var.height > y > 690):
                # update all the operations, tools, and operative buttons
                toolbar[var.tool_screen].update(events)
                var.rotate.update(events)
                var.reorder.update(events)
                var.fold.update(events)
                var._undo_redo.update(events)
                for op in var._operations:
                    op.update(events)
                check_op()
                # if remove op is selected for the first time, init slider
                if var.op.name == "remove" and not var.slider:
                    init_slider()
            # CLICK ON TOOLBAR
            elif (350 > x > 0):
                # update tools and tool bar buttons
                var._bar_buttons.update(events)
                toolbar[var.tool_screen].update(events)
                # if remove is selected, change to add operation
                if var.op.name == "remove" and var.op._state == "selected":
                    # find add operation sprite and select it
                    add_op = [op for op in var._operations if op.name == "add"][0]
                    add_op._state = "selected"
                    var.op._state = "unselected"
                    var.op = add_op
                    check_op()
            # CLICK ON STEPS
            elif (var.width > x > 305 and y < 230):
                old_step = var.step
                for step in var._steps:
                    # search for updated step
                    updated = step.update(events)
                    if updated:
                        # if the final step is chosen, change to step-based toolbar
                        if var.step.num == len(var._steps) - 1:
                            var.final = True
                            final_toolbar()
                        # if the previous step chosen was final step
                        elif old_step.num == len(var._steps) - 1:
                            var.final = False
                            reset_tool()
                            # check operations to properly draw tools
                            check_op()
                        # if any other step is chosen, ensure final toolbar is not selected
                        else:
                            var.final = False
                        old_step.text.show()
                        var.step.text.hide()
                        break
            else:
                print("unknown update at " + str(x) + " " + str(y))
    # redraw screen
    draw_screen()
    draw_variables()
    draw_canvas(var.step.num)


""" Start the program by initializing the variables and beginning a
    while loop which processes events """
def start():
    # initialize the game and all the relevant sprites
    pygame.init()
    set_up_vars()
    init_undo_redo()
    init_bar_buttons()
    init_slider()
    init_rotate()
    init_reorder()
    init_fold()
    # draw the screen and variables
    draw_screen()
    draw_variables()
    # hide the first step's label
    var.step.text.hide()
    pygame.display.flip()
    
    while running:
        # tick clock, get mouse position, and process events
        var.time = clock.tick(60)
        x, y = pygame.mouse.get_pos()
        events = pygame.event.get()
        pygame_widgets.update(events)
        process_events(events)
        # if remove operation is selected
        if var.op.name == "remove" and var.slider:
            # hide text labels of rotate and fold
            var.rotate_label.hide()
            var.fold_label.hide()
            # draw reorder and slider
            draw_reorder()
            draw_slider()
            # draw shadow circle to show erase area on mouse
            draw_shadow((x,y), var.screen)
        # if add operation is selected
        elif var.op.name == "add" and var.op._state == "selected":
            # hide slider, slider text, and fold
            var.slider.hide()
            var.text_box.hide()
            var.fold_label.hide()
            # draw reorder and rotate
            draw_rotate()
            draw_reorder()
            if var.tool:
                # draw fold if foldable tool is selected
                if var.tool.foldable:
                    draw_fold()
                # show a shadow of image on mouse
                draw_shadow_tool((x,y), var.tool, var.screen)
        pygame.display.flip()
    pygame.quit()


""" Read in variable images for tools and steps from local directory """
def set_up_vars():
    # find local directory
    path = "/Users/mcblair/thesis/box-bots/images/"
    # make sure file is png or jpg
    # initialize steps
    step_list = os.listdir(path + var.project + '/steps/')
    steps = sorted(['images/' + var.project + '/steps/' + s for s in step_list \
                    if "png" in s])
    init_steps(steps)
    
    # initialize tools
    # tools order: bottlecap, cardboard, rubber, skewer, straw, glue
    sizes = [160, 350, 175, 370, 380, 85]
    tool_list = os.listdir(path + var.project + '/tools/')
    # filter out alternate or reverse images
    tools = sorted(['images/' + var.project + '/tools/' + t for t in tool_list \
                    if ("alt" not in t and "rev" not in t) and \
                        ("png" in t or "jpg" in t)])
    init_toolbar(tools, sizes)

    # initialize operations
    op_list = os.listdir(path + 'operations/')
    op_names = ['add', 'remove']
    ops = ['images/operations/' + o for o in op_list if "png" in o]
    init_operations(ops, op_names)
    
    
""" Start main function """
if __name__ == '__main__':
    # read in project name
    project_name = sys.argv[1:]
    if project_name:
        var.project = project_name[0]
        # set starting variables
        running = True
        slider = False
        # start clock and interface
        clock = pygame.time.Clock()
        print('\nstarting interface...\n')
        start()
    # ask for a project name if none is provided
    else:
        print("\nEnter a project name (i.e., 'tutorial')\n")
        running = False
        pygame.quit()
