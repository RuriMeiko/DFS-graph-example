from asyncio import sleep
import math
import numpy as np
import cv2


background = np.zeros((700, 1200, 3), dtype = "uint8")

# back ground color
background[:] = (0, 0, 0)
background = cv2.imread("bg.jpg", cv2.IMREAD_COLOR)
def clear_box(start,end):
    global background
    a = cv2.imread("bg.jpg", cv2.IMREAD_COLOR)

    x, y, w, h =start[0],start[1],end[0]-start[0],end[1]-start[1]
    sub_img = a[y:y+h, x:x+w]
    background[y:y+h, x:x+w] = sub_img

def draw_text_debug(text, org):
    global background
    background = cv2.putText(background, text, org, cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
# draw:
def draw_line(start, end, color = (255, 255, 255), thickness = 2):
    global background
    background = cv2.line(background, start, end, color, thickness)

def draw_node(center, text, radius = 20, color = (255, 255, 255), thickness = 2):
    global background
    org = (center[0] - radius//4, center[1] + radius//4)
    background = cv2.circle(background, center, radius, color, cv2.FILLED, thickness)
    background = cv2.putText(background, text, org, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), thickness-2, cv2.LINE_AA)

def reverse_list_tuple(list) -> list:
    new_list = []
    for i in range(len(list)-1, -1, -1):
        new_list.append(list[i]) 
    return new_list

# find line:
def find_line(start, end):
    a = (end[1] - start[1])/(end[0] - start[0])
    b = start[1] - a * start[0]
    return (a, b)

# line point:
def line_point(start, end) -> list:
    res = []
    X = start[0]

    if start[0] == end[0]:
        if start[1] < end[1]:
            for i in range(start[1], end[1], 2):
                res.append((start[0], i))
        elif start[1] > end[1]:
            for i in range(end[1], start[1], 2):
                res.append((start[0], i))
            res = reverse_list_tuple(res)
    elif start[1] == end[1]:
        if start[0] < end[0]:
            for i in range(start[0], end[0], 2):
                res.append((i, start[1]))
        elif start[0] > end[0]:
            for i in range(end[0], start[0], 2):
                res.append((i, start[1]))
            res = reverse_list_tuple(res)
    elif start[0] < end[0]:
        line = find_line(start, end)
        for i in range(start[0], end[0], 2):
            Y = line[0] * i + line[1]
            Y = round(Y)
            res.append((i, Y))
    elif start[0] > end[0]:
        line = find_line(start, end)
        for i in range(end[0], start[0], 2):
            Y = line[0] * i + line[1]
            Y = round(Y)
            res.append((i, Y))
        res = reverse_list_tuple(res)

    return res

# anim line:
def anim_line(start_name, end_name, start_color, linecolor):
    for i in line_point(curr_pos[start_name], curr_pos[end_name]):
        draw_line(curr_pos[start_name], i, linecolor, 2)
        draw_node(curr_pos[start_name], start_name, color = start_color)
        draw_node(curr_pos[end_name], end_name)

        cv2.imshow('Graph Demo', background)
        cv2.waitKey(1)
# check if line cross any pos

def pythagoras(a, c) -> float:
    return round(math.sqrt(math.pow(c, 2) - math.pow(a, 2)))

def rand_pos_circle_graph(graph: dict, center, step = 100):
    result = []

    first_total = math.floor(len(graph) / 2)
    second_total = math.ceil(len(graph) / 2)


    diameter = (second_total + 1) * step
    radius = diameter/2

    first_step = round(diameter / (first_total+1))

    print(radius)
    for i in range(0, diameter + 1, first_step):
        if i != 0 and i != diameter:
            x = radius - i if i <= radius else i - radius
            y = pythagoras(x, radius)
            result.append((int(center[0] - radius + i), int(center[1] - y)))

    for i in range(0, diameter + 1, step):
        if i != 0 and i != diameter:
            x = radius - i if i <= radius else i - radius
            y = pythagoras(x, radius) 
            result.append((int(center[0] - radius + i), int(center[1] + y)))

    return result

def draw_circle_graph(graph: dict):
    posList = rand_pos_circle_graph(graph, (350, 350))
    j = 0

    for i in graph.keys():
        curr_pos[i] = posList[j]
        j += 1

    print(posList)

    for i in graph:
        for j in graph[i]:
            draw_line(curr_pos[i], curr_pos[j])


    for i in curr_pos:
        draw_node(curr_pos[i], i)

curr_pos = {}

def show_img(num: int):
    cv2.imshow('Graph Demo', background)
    cv2.waitKey(num)

def show_result():
    cv2.imshow('Graph Demo', background)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def pause():
    cv2.waitKey(0)

