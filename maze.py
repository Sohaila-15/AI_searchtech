import pygame
import sys
import heapq
from collections import deque
pygame.font.init()
font = pygame.font.Font(None, 36)

class Node:
    def _init_(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.h = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.h < other.h
        
    def __lt__(self, other):
        return self.position < other.position

def is_valid(maze, visited, row, col):
    rows, cols = len(maze), len(maze[0])
    return (0 <= row < rows) and (0 <= col < cols) and (maze[row][col] == 0) and not visited[row][col]

def BreadthF(maze, start, end):
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  #### left , down ,right ,up
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    explore=[]
    explored_cells=[]
    fringe = deque()
    fringe.append((start[1], start[0]))
    visited[start[1]][start[0]] = (start[0], start[1])
    ct=0
    while fringe:
        current_pos = fringe.popleft()
        row,col = current_pos

        explore.append(current_pos)
        explored_cells.append([(pos[1], pos[0]) for pos in explore])
        if ((current_pos[1], current_pos[0]) == end) or ((current_pos[1], current_pos[0]) in end) :
            path = []
            while current_pos[1] != start[0] and current_pos[0] !=start[1]:
                path.append((current_pos[1], current_pos[0]))
                current_pos = visited[current_pos[0]][current_pos[1]]
            path.append((current_pos[1], current_pos[0]))
            path.append((start[0], start[1]))

            return [path[::-1],explored_cells]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if is_valid(maze, visited, new_row, new_col):
                fringe.append((new_row, new_col))
                visited[new_row][new_col] = (row, col)

    return[-1,-1]


def best_first_search(maze, start, end):
    path = []
    expand_nodes=[]
    visited=[]
    start2=start
    start=(start2[1],start2[0])
    start_node = Node(start,None)
   # extra_start_node=(start_node.position[1],start_node.position[0])
    end_node = Node(end, None)

    fringe = []
    visited=[]

    heapq.heapify(fringe)
    # heapq.heappush(fringe, start_node)
    fringe.append(start_node)

    movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while len(fringe) > 0:
        #current_path = fringe2.pop()
        #print(current_path)
        current_node = heapq.heappop(fringe)
        #fringe2.append(current_path + [current_node.position])
        visited.append(current_node.position)
        expand_nodes.append([(pos[1], pos[0]) for pos in visited])
    
        if end_node.position[0] == current_node.position[1] and current_node.position[0] == end_node.position[1]:
            #print("current node:",current_node.position)
            #print("end node:",end_node.position)
            # extra_node2=visited.pop(0)
            # swapped_node2=(extra_node2[1],extra_node2[0])
            # extra_node2=swapped_node2
            # visited.insert(0,extra_node2)
            # expand_nodes.pop()
            # expand_nodes.append([(pos[1], pos[0]) for pos in visited])
            # print(extra_node2.position)
            # fringe2.append(current_path + [extra_node2.position])
            # draw(current_node.position[0], current_node.position[1])
         
            while current_node != start_node:
                path.append((current_node.position[1], current_node.position[0]))
                current_node = current_node.parent
            # extra_node=path.pop(len(path)-1)
            # swapped_node = (extra_node[1], extra_node[0])
            # extra_node=swapped_node
            path.append((current_node.position[1], current_node.position[0]))
            #print(path)
            return [path[::-1], expand_nodes]

        for move in movements:
             child_position = (
                 current_node.position[0] + move[0], current_node.position[1] + move[1])
         
             if (child_position[0] < 0 or child_position[0] >= len(maze) or child_position[1] < 0 or child_position[1] >= len(maze[0])):
                 continue
         
             if maze[child_position[0]][child_position[1]] != 0:
                 continue
         
             child_node = Node(child_position, current_node)
         
             if child_node.position in visited:
                 continue
         
             child_node.h = abs(
                 child_position[0] - end_node.position[1]) + abs(child_position[1] - end_node.position[0])
         
             if child_node.position in [node.position for node in fringe]:
                 continue
             
             heapq.heappush(fringe, child_node)
             #child=(child_node.position[0],child_node.position[1])
             #fringe2.append(current_path + [child])####HERE#####

    return [-1,-1]
 
def dfs_solve(maze, start, goals):
    visited = set()
    visited.add(start)
    fringe = [start]
    fringe2 = [[start]]
    final_path = []
    explored_paths = []

    def create_fringe(current):
        return [
            (current[0] + 1, current[1]),   # Down
            (current[0] - 1, current[1]),  # Up
            (current[0], current[1] - 1),  # Left
            (current[0], current[1] + 1),  # Right
        ]

    def check_validity(next_check):
        if 0 <= next_check[0] < len(maze[0]) and 0 <= next_check[1] < len(maze):
            #if ct==19 or ct==20 or ct==21:
                # print(f"check : {next_check}")
                # print(f"visited : {visited}")
            if next_check not in visited:
                if maze[next_check[1]][next_check[0]] == 0:
                    return next_check
        return None
 
    ct=-1
    while fringe:
        ct=ct+1
        current_path = fringe2.pop()
        # if ct>=0 and ct<=10:
        #     print(f"ct : {ct}")
        #     print(f"fring : {fringe}")
        current = fringe.pop()
        visited.add(current)
        # if ct==19 or ct==20 or ct==21:
        #     print(f"current : {current}")
        explored_paths.append(current_path)

        if current in goals:
            final_path = current_path
            break

        neighbors = create_fringe(current)
        # if ct==19 or ct==20 or ct==21:
        #     print(f"neighbors : {neighbors}")
        for neighbor in neighbors:
            next_cell = check_validity(neighbor)
            if next_cell is not None:
                fringe.append(next_cell)
                # if ct==19 or ct==20 or ct==21:
                #     print(f"accepted : {next_cell}")
                fringe2.append(current_path + [next_cell])

    return [final_path, explored_paths]




# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze")

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
gray = (50, 50, 50)
blue = (0,0,255)

# Load player image (replace with Pacman image)
player_rect = pygame.Rect(0, 0, width // 20, height // 20)
player_color = (255, 255, 0)  # Yellow color for Pacman
player_pos = [-1,-1]

# Load goal image
goal_rect = pygame.Rect(0, 0, width // 20, height // 20)
goal_color = (100, 50, 150)
goal_pos = []

# Maze representation (0 for empty, 1 for wall)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

explored_paths = []
final_path = []
flag_move = False
flagKeepDrawing = False
ct = 0


def draw_popup():
    popup_text = font.render("Choose Algorithm:", True, white)
    dfs_button = pygame.Rect(200, 200, 200, 50)
    bfs_button = pygame.Rect(200, 300, 200, 50)
    greedy_button = pygame.Rect(200, 400, 200, 50)

    pygame.draw.rect(screen, gray, dfs_button)
    pygame.draw.rect(screen, gray, bfs_button)
    pygame.draw.rect(screen, gray, greedy_button)

    dfs_text = font.render("DFS", True, white)
    bfs_text = font.render("BFS", True, white)
    greedy_text = font.render("Greedy", True, white)

    screen.blit(popup_text, (200, 150))
    screen.blit(dfs_text, (dfs_button.x + 10, dfs_button.y + 10))
    screen.blit(bfs_text, (bfs_button.x + 10, bfs_button.y + 10))
    screen.blit(greedy_text, (greedy_button.x + 10, greedy_button.y + 10))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if dfs_button.collidepoint(x, y):
                    return 1  # DFS
                elif bfs_button.collidepoint(x, y):
                    return 2  # BFS
                elif greedy_button.collidepoint(x, y):
                    return 3  # Greedy
                
def draw():
    global player_pos, explored_paths, final_path, flag_move, flagKeepDrawing

    # Clear the screen
    screen.fill(black)

    # Draw the maze
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * (width // len(maze[0])), y * (height // len(maze)),
                               width // len(maze[0]), height // len(maze))
            if cell == 1:
                pygame.draw.rect(screen, blue, rect, border_radius=5)

    # Draw the explored path
    if explored_paths and flag_move:
        path = explored_paths[0]
        for pos in path:
            x, y = pos  # Unpack the tuple
            rect = pygame.Rect(x * (width // len(maze[0])), y * (height // len(maze)),
                               width // len(maze[0]), height // len(maze))
            pygame.draw.rect(screen, gray, rect, border_radius=5)
        # Remove the drawn path
        explored_paths = explored_paths[1:]

    # Draw the final path in green when the player reaches each goal
    if player_pos in goal_pos and flag_move:
        for pos in final_path:
            x, y = pos  # Unpack the tuple
            rect = pygame.Rect(x * (width // len(maze[0])), y * (height // len(maze)),
                               width // len(maze[0]), height // len(maze))
            pygame.draw.rect(screen, green, rect, border_radius=5)
        # Stop further movements and drawing
        flag_move = False

    # Draw the goals
    for goal in goal_pos:
        goal_rect.topleft = (goal[0] * (width // len(maze[0])), goal[1] * (height // len(maze)))
        pygame.draw.rect(screen, goal_color, goal_rect, border_radius=50)

    if player_pos is not None:
        x, y = player_pos  # Unpack the tuple
        player_rect.topleft = (x * (width // len(maze[0])), y * (height // len(maze)))
        pygame.draw.rect(screen, player_color, player_rect, border_radius=50)

    # Update the display
    if not flagKeepDrawing:
        pygame.display.flip()
    if player_pos in goal_pos:
        flagKeepDrawing = True

    pygame.time.delay(150)  # Adjust delay for a smoother visualization

    # Control the frames per second
    pygame.time.Clock().tick(8)

# Main game loop
flagAlgo = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not flag_move:
            x, y = event.pos
            maze_x = x // (width // len(maze[0]))
            maze_y = y // (height // len(maze))
            if 0 <= maze_y < len(maze) and 0 <= maze_x < len(maze[0]):
                maze[maze_y][maze_x] = 1 if maze[maze_y][maze_x] == 0 else 0

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not flag_move:
            x, y = event.pos
            maze_x = x // (width // len(maze[0]))
            maze_y = y // (height // len(maze))

            if ct == 0:
                maze[maze_y][maze_x] = 0
                player_pos = (maze_x, maze_y)
            else:
                maze[maze_y][maze_x] = 0
                goal_pos.append((maze_x, maze_y))
            ct=ct+1
            
        elif event.type == pygame.KEYDOWN and not flag_move:
            if event.key == pygame.K_SPACE:
                #algorithm_choice = draw_popup()
                #print("User chose algorithm:", algorithm_choice)
                flagALgo=draw_popup()
                flag_move = True
            elif event.key == pygame.K_RETURN:
                pygame.quit()
                sys.exit()
            

    if flag_move:
        if flagALgo==1:
            solution = dfs_solve(maze, player_pos, goal_pos) #MAI
        elif flagALgo==3:
            solution = best_first_search(maze, player_pos, goal_pos[0]) #ROFAIDA
        else:
            solution=BreadthF(maze, player_pos, goal_pos) #SOHAILA
        #print(solution)
        if solution:
            final_path, explored_paths = solution
            #print(explored_paths)
            #print(final_path)
            for step in explored_paths:
                player_pos = step[-1]
                draw()
                pygame.time.delay(100)
            if player_pos in goal_pos:
                for step in final_path:
                    player_pos = step
                    draw()
                    pygame.time.delay(100)

            flag_move = False
            

    draw()
    pygame.display.flip()
    pygame.time.Clock().tick(8)