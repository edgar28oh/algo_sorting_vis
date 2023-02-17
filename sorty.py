from curses import window
import random
import math
import pygame
pygame.init()
WIDTH = 900
HEIGHT = 750
win = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.Font('freesansbold.ttf', 18)
pygame.display.set_caption('Visualition for Sorting Algos')


# some colors
LIGHT_GRAY = 239, 239, 239
MED_GRAY = 122, 122, 122
DARK_GRAY = 61, 61, 61
BG = LIGHT_GRAY
YELLOW = 243, 255, 60
BLUE = 60, 92, 255
WHITE = 255, 255, 255
BLACK = 0, 0, 0


class Button:
    def __init__(self, width, height, x_cord, y_cord, text, enabled):
        self.width = width
        self.height = height
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.text = text
        self.enabled = enabled
        self.draw()

    def draw(self):
        button_txt = font.render(self.text, True, 'black')
        button_rect = pygame.rect.Rect(
            (self.x_cord, self.y_cord), (self.height, self.width))
        if self.enabled:
            if self.clicky():
                pygame.draw.rect(win, 'green', button_rect, 0, 5)
            else:
                pygame.draw.rect(win, 'red', button_rect, 0, 5)
        else:
            pygame.draw.rect(win, 'grey', button_rect, 0, 5)
        pygame.draw.rect(win, 'white', button_rect, 2, 5)
        win.blit(button_txt, (self.x_cord + 2, self.y_cord + 2))

    def clicky(self):
        mouse_pos = pygame.mouse.get_pos()
        left_clck = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect(
            (self.x_cord, self.y_cord), (self.height, self.width))
        if left_clck and button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        else:
            return False

    def isOver(self, pos):
        if pos[0] > self.x_cord and pos[0] < self.x_cord + self.height:
            if pos[1] > self.y_cord and pos[1] < self.y_cord + self.width:
                return True

        return False


class DrawStuff:

    GRADIENTS = [
        (245, 236, 66),
        (66, 245, 120),
        (245, 66, 158)
    ]

    LR_PADDING = 60
    TOP_PADDING = 120
    BG_COLOR = BLACK
    FONT = pygame.font.SysFont('arial', 30)
    PINK = 242, 66, 245
    LIGHT_BLUE = 66, 212, 245

    def __init__(self, width, height, lst):
        self.width = WIDTH
        self.height = HEIGHT
        self.window = pygame.display.set_mode((width, height))
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.bar_width = round((self.width - self.LR_PADDING) / len(lst))
        self.bar_height = math.floor(
            (self.height - self.TOP_PADDING) / (self.max_val - self.min_val))
        self.start_x = self.LR_PADDING // 2


def draw(draw_stuff, sorting_algo_name, ascending):
    # this is the error for reset
    draw_stuff.window.fill('black')

    title = draw_stuff.FONT.render(f"{sorting_algo_name} - {' Ascending' if ascending else ' Descending'}", 1, draw_stuff.PINK)
    draw_stuff.window.blit(title,(draw_stuff.width/2 - title.get_width()/2,55))

    reset_bttn = Button(22, 55, 25, 25, 'Reset', True)
    strt_bttn = Button(22, 50, 95, 25, 'Start', True)
    ascend_bttn = Button(22, 100, 165, 25, 'Ascending', True)
    descen_bttn = Button(22, 110, 280, 25, 'Descending', True)
    insert_sort_bttn = Button(22, 125, 410, 25, 'Insertion Sort', True)
    bubble_sort_bttn = Button(22, 110, 565, 25, 'Bubble Sort', True)
    quick_sort_bttn = Button(22, 110, 695, 25, 'Quick Sort', True)

    draw_list(draw_stuff)
    pygame.display.update()


def start_list(n, min_val, max_val):

    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def draw_list(draw_stuff, color_pos = {}, clear_bg = False):
    lst = draw_stuff.lst

    if clear_bg:
        clear_rect = (draw_stuff.LR_PADDING//2, draw_stuff.TOP_PADDING, draw_stuff.width - draw_stuff.LR_PADDING, draw_stuff.height - draw_stuff.TOP_PADDING)
        pygame.draw.rect(draw_stuff.window, draw_stuff.BG_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_stuff.start_x + i * draw_stuff.bar_width

        y = draw_stuff.height - \
            (val - draw_stuff.min_val) * draw_stuff.bar_height

        color = draw_stuff.GRADIENTS[i % 3]
        if i in color_pos:
            color = color_pos[i]

        pygame.draw.rect(win, color,
                         (x, y, draw_stuff.bar_width, draw_stuff.height))
    if clear_bg:
        pygame.display.update()

def insertion_sort(draw_stuff, ascending = True):
    lst = draw_stuff.lst

    for i in range(1, len(lst)):
        curr = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > curr and ascending
            descending_sort = i > 0 and lst[i - 1] < curr and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = curr
            draw_list(draw_stuff, {i - 1: draw_stuff.PINK, i: draw_stuff.LIGHT_BLUE}, 1)
            yield True
    return lst


def bubble_sort(draw_stuff, ascending = True):
    lst = draw_stuff.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_stuff, {j: draw_stuff.PINK, j + 1: draw_stuff.LIGHT_BLUE}, True)
                yield True
    return lst

def quick_sort(draw_stuff, ascending = True):
    pass

def do_work():
    run = True
    clock = pygame.time.Clock()
    sort_go = False
    ascending = True

    n = 150
    min_val = 0
    max_val = 150

    lst = start_list(n, min_val, max_val)

    draw_stuff = DrawStuff(WIDTH, HEIGHT, lst)

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    while run:
        clock.tick(260)

        reset_bttn = Button(22, 55, 25, 25, 'Reset', True)
        strt_bttn = Button(22, 50, 95, 25, 'Start', True)
        ascend_bttn = Button(22, 100, 165, 25, 'Ascending', True)
        descen_bttn = Button(22, 110, 280, 25, 'Descending', True)
        insert_sort_bttn = Button(22, 125, 410, 25, 'Insertion Sort', True)
        bubble_sort_bttn = Button(22, 110, 565, 25, 'Bubble Sort', True)
        quick_sort_bttn = Button(22, 110, 695, 25, 'Quick Sort', True)

        if sort_go:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sort_go = False
        else:
            draw(draw_stuff, sorting_algo_name, ascending)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()   

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and reset_bttn.isOver(pos) and reset_bttn.clicky():
                lst = start_list(n, min_val, max_val)
                draw_stuff.set_list(lst)
                sort_go = False          

            elif event.type == pygame.MOUSEBUTTONDOWN and strt_bttn.isOver(pos) and strt_bttn.clicky() and sort_go == False:
                sort_go = True
                sorting_algo_generator = sorting_algo(draw_stuff, ascending)
            
            # button mouse hover for sorting algos
            elif event.type == pygame.MOUSEBUTTONDOWN and bubble_sort_bttn.isOver(pos) and bubble_sort_bttn.clicky() and sort_go == False:
                sorting_algo = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.type == pygame.MOUSEBUTTONDOWN and insert_sort_bttn.isOver(pos) and insert_sort_bttn.clicky() and sort_go == False:
                sorting_algo = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.type == pygame.MOUSEBUTTONDOWN and quick_sort_bttn.isOver(pos) and quick_sort_bttn.clicky() and sort_go == False:
                sorting_algo = quick_sort
                sorting_algo_name = "Quick Sort"

            
            elif event.type == pygame.MOUSEBUTTONDOWN and ascend_bttn.isOver(pos) and ascend_bttn.clicky() and not sort_go:
                ascending = True

            elif event.type == pygame.MOUSEBUTTONDOWN and descen_bttn.isOver(pos) and descen_bttn.clicky() and not sort_go:
                ascending = False

    pygame.quit()


if __name__ == "__main__":
    do_work()
