#pip install asyncio numpy opencv-python
import GapthChar
# =0 -> press any key to next frame| >0 auto frame count by ms
Time_Delay = 0

class StackNode:
    def __init__(self, val):
        self.val = val
        self.next = None


class Stack:
    def __init__(self):
        self.root = None

    def isEmpty(self):
        return True if self.root is None else False

    def printStack(self):
        res = []
        temp = self.root
        while temp != None:
            res.append(temp.val)
            temp = temp.next
        return res

    def push(self, val):
        newNode = StackNode(val)
        newNode.next = self.root
        self.root = newNode
        print("pushed to stack", (val))
        # GapthChar.draw_line((700,150),(1200,150),thickness=50,color=(0,0,0))
        global count
        if count > 560:
            count = 200
            GapthChar.clear_box((650, 180), (1200, 650))
            GapthChar.show_img(1)
        GapthChar.draw_text_debug("pushed to stack " + (val), (700, count))
        count += 20

    def pop(self):
        if (self.isEmpty()):
            return float('-inf')
        temp = self.root
        self.root = self.root.next
        popped = temp.val
        print("delete from stack", (popped))
        global count

        if count > 560:
            count = 200
            GapthChar.clear_box((650, 180), (1200, 650))
            GapthChar.show_img(1)

        GapthChar.draw_text_debug(
            "delete from stack " + (popped), (700, count))
        count += 20

        return popped

    def peek(self):
        if (self.isEmpty()):
            return float('-inf')
        return self.root.val

    def length(self) -> int:
        count = 0
        temp = self.root
        while temp != None:
            count += 1
            temp = temp.next
        return count


def check_list(l: list, e: str) -> bool:
    if e in l:
        return True
    return False


def check_node(s: set, l: list):
    for e in s:
        if not check_list(l, e):
            return True
    return False


def debug_log_stack(stack):
    #GapthChar.draw_line((700, 145), (1150, 145), thickness=30, color=c_bg)
    GapthChar.clear_box((650, 120), (1200, 160))
    GapthChar.draw_text_debug('stack='+str(stack.printStack()), (700, 150))
    GapthChar.show_img(1)


def debug_log_res(res):
    GapthChar.clear_box((650, 50), (1200, 110))
    GapthChar.draw_text_debug('res='+str(res), (700, 100))
    GapthChar.show_img(1)


def DFS(start: str, check: list) -> list:
    res = []
    stack = Stack()

    debug_log_stack(stack)
    debug_log_res(res)
    # start node
    GapthChar.draw_node(GapthChar.curr_pos[start], start, color=c_curr_node)
    GapthChar.show_img(Time_Delay)

    stack.push(start)
    debug_log_stack(stack)
    check.append(start)

    while (check_node(graph[start], check)) or (stack.length() > 0):
        while check_node(graph[start], check):

            for n in graph[start]:
                if not check_list(check, n):
                    # draw line
                    GapthChar.anim_line(start, n, c_curr_node, c_line)
                    GapthChar.show_img(1)
                    GapthChar.draw_node(
                        GapthChar.curr_pos[start], start, color=c_in_stack)
                    start = n
                    # start be n
                    GapthChar.draw_node(
                        GapthChar.curr_pos[start], start, color=c_curr_node)
                    GapthChar.show_img(Time_Delay)

                    stack.push(start)
                    debug_log_stack(stack)
                    check.append(start)

                    break

        GapthChar.draw_node(
            GapthChar.curr_pos[start], start, color=c_in_result)
        GapthChar.show_img(Time_Delay)

        res.append(stack.pop())
        debug_log_stack(stack)

        debug_log_res(res)

        if stack.peek() != float('-inf'):
            start = stack.peek()

    return res


if __name__ == '__main__':
    count = 200

    c_curr_node = (44, 107, 220)  # cam
    c_in_stack = (50, 142, 101)  # xanh luc
    c_in_result = (132, 108, 60)  # xanh bau troi
    c_line = (143, 83, 153)  # red
    # c_bg = (44, 60, 84)
    c_bg = (0, 0, 0)
    #GapthChar.background[:] = c_bg
    graph = {'A': (['B', 'C', 'D']),
             'B': (['A', 'E', 'F']),
             'C': (['A', 'D', 'G']),
             'D': (['A', 'C', 'G', 'H']),
             'E': (['B', 'F', 'I']),
             'F': (['B', 'E', 'G']),
             'G': (['F', 'C', 'D']),
             'H': (['D']),
             'I': (['E'])}

    check = []

    GapthChar.draw_circle_graph(graph)

    # print(DFS('A', check))
    print(('A', check))
    GapthChar.show_result()
