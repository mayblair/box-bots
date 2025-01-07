# PYGAME INTERFACE for modular building instructions with images
import pygame
import pygame_widgets
import os
import sys
from settings import var
from logic import init_operations, init_toolbar, init_steps, \
    init_undo_redo, init_bar_buttons, final_toolbar, reset_tool, \
    draw_screen, draw_canvas, draw_new_tool, init_rotate, draw_rotate, \
    draw_variables, remove_new_circle, check_op, init_slider, draw_slider, \
    draw_shadow, draw_shadow_tool, init_reorder, draw_reorder, \
    init_fold, draw_fold


# GAME LOGIC
def process_events(events):
    global var
    global slider
    global running
    for event in events: 
        if event.type == pygame.QUIT:
            running = False
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # pygame_widgets.update(events)
            # var._undo_redo.update(events)
            # var._bar_buttons.update(events)
            x, y = pygame.mouse.get_pos()
            toolbar = var._tools if not var.final else var._final_tools

            # click on canvas
            if (var.width-100 > x > 350 and 630 > y > 230):
                # store tool info in dictionary under selected step
                if var.op.name == "add" and var.tool:
                    var.canvas[var.step.num] += [(var.tool, x, y, var.tool.rotation, var.tool.num_shape)]
                    draw_new_tool()
                    return True
                # store removed circle in dictionary under selected step
                elif var.op.name == "remove":
                    # only remove material if there is material on canvas
                    if var.canvas[var.step.num]:
                        var.canvas[var.step.num] += [("remove", x, y, var.slider.getValue())]
                        remove_new_circle()
                        return True
            # click on operations
            elif (var.width - 20 > x > 350 and var.height > y > 690):
                toolbar[var.tool_screen].update(events)
                var.rotate.update(events)
                var.reorder.update(events)
                var.fold.update(events)
                var._undo_redo.update(events)
                # check add and remove ops for a change
                for op in var._operations:
                    updated = op.update(events)
                    if updated:
                        check_op()
                        break
                # if remove op is selected for first time, init slider
                if var.op.name == "remove":
                    if not var.slider:
                        init_slider()
            # click on tool bar
            elif (350 > x > 0):
                var._bar_buttons.update(events)
                toolbar[var.tool_screen].update(events)
            # click on steps
            elif (var.width > x > 305 and y < 230):
                old_step = var.step.num
                for step in var._steps:
                    updated = step.update(events)
                    if updated:
                        # if the final step is chosen, change to step-based toobar
                        if var.step.num == len(var._steps) - 1:
                            var.final = True
                            final_toolbar()
                            check_op()
                        # if the previous step chosen was final step
                        elif old_step == len(var._steps) - 1:
                            reset_tool()
                            var.final = False
                            check_op()
                        else:
                            var.final = False
                        break
            else:
                print("unknown update at " + str(x) + " " + str(y))
    draw_screen()
    draw_variables()
    draw_canvas(var.step.num)
    return True


# START FUNCTION
def start():
    # global slider
    pygame.init()
    set_up_vars()
    init_undo_redo()
    init_bar_buttons()
    init_slider()
    init_rotate()
    init_reorder()
    init_fold()
    draw_screen()
    draw_variables()
    pygame.display.flip()
    
    while running:
        var.time = clock.tick(60)
        x, y = pygame.mouse.get_pos()
        events = pygame.event.get()
        pygame_widgets.update(events)
        process_events(events)
        # if remove is selected and slider is initiated, draw slider and shadow circle
        if var.op.name == "remove" and var.slider:
            # set text labels of rotate, reorder, and fold to be blank
            var.rotate_label.setText("")
            var.fold_label.setText("")
            draw_reorder()
            draw_slider()
            draw_shadow((x,y), var.screen)
        # otherwise add is selected, show a shadow of image on mouse
        elif var.op.name == "add" and var.tool and var.op._state != "prompted":
            var.slider.hide()
            var.text_box.hide()
            draw_rotate()
            draw_reorder()
            draw_fold()
            draw_shadow_tool((x,y), var.tool, var.screen)
        pygame.display.flip()
    pygame.quit()


# READ IN VARIABLES FROM LOCAL DIRECTORIES
def set_up_vars():
    # Get the list of all files and directories
    path = "/Users/mcblair/thesis/box-bots/images/"
    # make sure is png or jpg
    step_list = os.listdir(path + var.project + '/steps/')
    steps = sorted(['images/' + var.project + '/steps/' + s for s in step_list \
                    if "png" in s])
    init_steps(steps)

    # bottlecap, cardboard, rubber, skewer, straw, glue
    sizes = [160, 350, 185, 370, 380, 85]
    tool_list = os.listdir(path + var.project + '/tools/')
    tools = sorted(['images/' + var.project + '/tools/' + t for t in tool_list \
                    if ("alt" not in t and "rev" not in t) and \
                        ("png" in t or "jpg" in t)])
    init_toolbar(tools, sizes)

    op_list = os.listdir(path + 'operations/')
    op_names = ['add', 'remove']
    ops = ['images/operations/' + o for o in op_list if "png" in o]
    init_operations(ops, op_names)

if __name__ == '__main__':
    # MAIN PROGRAM VARIABLES
    project_name = sys.argv[1:]
    if project_name:
        var.project = project_name[0]
        running = True
        slider = False
        # START GAME
        clock = pygame.time.Clock()
        print('\nstarting interface...\n')
        start()
    else:
        print("\nEnter a project name (i.e., 'car')\n")
        running = False
        pygame.quit()
