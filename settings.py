# GLOBAL VARIABLES
import pygame

# origin (0, 0) is top left corner

class Var():
    def __init__(self):
        global var
        # SCREEN INFORMATION SETUP
        self.height = 846
        self.width = 1436
        self.dimensions = (self.width, self.height)
        self.half_width = 718
        self.half_height = 423
        self.setup = True
        self.time = 0

        self.project = ""

        self.screen = pygame.display.set_mode(self.dimensions)

        # VARIABLE GROUPS SETUP
        self._undo_redo = pygame.sprite.Group()
        self._bar_buttons = pygame.sprite.Group()
        self.active_bar_buttons = []
        self.slider = None
        self.text_box = None
        self.rotate = None
        self.rotate_label = None
        self.reorder = None
        self.reorder_label = None
        self.fold = None
        self.fold_label = None

        self._operations = pygame.sprite.Group()
        self.op = None

        self._steps = pygame.sprite.Group()
        self.step = None

        # tools is a list of sprite groups for 4 tool sprite each
        # tool_screen is the index into the tools list
        self._tools = []
        self.tool = None
        self.tool_screen = -1
        # final tools are the canvases of each step
        self._final_tools = []
        self.final = False

        # canvas tracks any addition/subtraction of materials
        # redo tracks the "undo" of any materials removed from canvas
        # both have key: step num and value: (material, x, y, size/rotation, shape)
        # material can be either a tool or a "remove" circle to erase
        self.canvas = {}
        self.redo = {}
        
        # COLORS
        self.green = (30, 179, 113)
        self.purple = (179, 30, 113)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.light_grey = (240, 240, 240)
        self.less_light_grey = (225, 225, 225)
        self.mid_grey = (216, 216, 216)
        self.more_grey = (190, 190, 190)
        self.mostly_grey = (165, 165, 165)
        self.most_grey = (145,145,145)
        self.transparent = (240, 240, 240, 0)
        self.transparent_grey = (165, 165, 165, 100)

var = Var()