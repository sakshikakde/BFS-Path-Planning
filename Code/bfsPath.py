
import numpy as np
import timeit
import argparse
import cv2
import matplotlib.pyplot as plt
import math
from Obstacle import *

class Node():
    def __init__(self, state, parent, move, cost): 

        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost
        
    def getState(self):
        return self.state
		
    def getParent(self):
        return self.parent
		
    def getMove(self):
	    return self.move
		
    def getCost(self):
        return self.cost

    def getFullPath(self):
        
        moves = []
        nodes = []
        current_node = self
        while(current_node.getMove() is not None):

            moves.append(current_node.getMove())
            nodes.append(current_node)
            current_node = current_node.getParent()

        nodes.append(current_node)
        moves.reverse()
        nodes.reverse()
        
        return moves, nodes

    def printStats(self):
        pass


def getBranches(node, step_size, space_size):

    moves = ["up", "down", "left", "right", "diagonal_right_up", "diagonal_right_down", "diagonal_left_up", "diagonal_left_down"]
    branches = []
    branches.append(Node(moveUp(node.getState(), step_size, space_size), node, moves[0], node.getCost() + 1))
    branches.append(Node(moveDown(node.getState(), step_size, space_size), node, moves[1], node.getCost() + 1))
    branches.append(Node(moveLeft(node.getState(), step_size, space_size), node, moves[2], node.getCost() + 1))
    branches.append(Node(moveRight(node.getState(), step_size, space_size), node, moves[3], node.getCost() + 1))

    branches.append(Node(moveDiagonalRightUp(node.getState(), step_size, space_size), node, moves[4], node.getCost() + np.sqrt(2)))
    branches.append(Node(moveDiagonalRightDown(node.getState(), step_size, space_size), node, moves[5], node.getCost() + np.sqrt(2)))
    branches.append(Node(moveDiagonalLeftUp(node.getState(), step_size, space_size), node, moves[6], node.getCost() + np.sqrt(2)))
    branches.append(Node(moveDiagonalLeftDown(node.getState(), step_size, space_size), node, moves[7], node.getCost() + np.sqrt(2)))

    #remove None nodes
    b = [branch for branch in branches if branch.getState() is not None]
            
    return b


def moveUp(state, step_size, space_size): #assuming we cat land on the borders

    size_x = space_size[1]
    size_y = space_size[0]

    current_position = state.copy()
    next_position = current_position.copy()
 
    if (current_position[1] < size_y - step_size) and check4Obstacle(current_position):
        next_position[1] = current_position[1] + step_size
        return next_position
    else:
        return None

def moveDown(state, step_size, grid_size):

    current_position = state.copy()
    next_position = current_position.copy()
 
    if (current_position[1] > 0 + step_size) and check4Obstacle(current_position):
        next_position[1] = current_position[1] - step_size
        return next_position
    else:
        return None

def moveRight(state, step_size, grid_size):

    size_x = sizex
    size_y = sizey

    current_position = state.copy()
    next_position = current_position.copy()
 
    if (current_position[0] < size_x - step_size) and check4Obstacle(current_position):
        next_position[0] = current_position[0] + step_size
        return next_position
    else:
        return None

def moveLeft(state, step_size, grid_size):
    current_position = state.copy()
    next_position = current_position.copy()
 
    if (current_position[0] > 0 + step_size) and check4Obstacle(current_position):
        next_position[0] = current_position[0] - step_size
        return next_position
    else:
        return None

def moveDiagonalRightUp(state, step_size, grid_size):

    size_x = sizex
    size_y = sizey

    current_position = state.copy()
    next_position = current_position.copy()
 
    if ((current_position[0] < size_x - step_size) and (current_position[1] < size_y - step_size)) and check4Obstacle(current_position):
        next_position[0] = current_position[0] + step_size
        next_position[1] = current_position[1] + step_size
        return next_position
    else:
        return None


def moveDiagonalRightDown(state, step_size, grid_size):
    size_x = sizex
    size_y = sizey

    current_position = state.copy()
    next_position = current_position.copy()
 
    if ((current_position[0] < size_x - step_size) and (current_position[1] > 0 + step_size)) and check4Obstacle(current_position):
        next_position[0] = current_position[0] + step_size
        next_position[1] = current_position[1] - step_size
        if next_position[1] < 0:
            print("right_down")
        return next_position
    else:
        return None

def moveDiagonalLeftUp(state, step_size, grid_size):
    size_x = sizex
    size_y = sizey

    current_position = state.copy()
    next_position = current_position.copy()
 
    if ((current_position[0] > 0 + step_size) and (current_position[1] < size_y - step_size)) and check4Obstacle(current_position):
        next_position[0] = current_position[0] - step_size
        next_position[1] = current_position[1] + step_size
        return next_position
    else:
        return None


def moveDiagonalLeftDown(state, step_size, grid_size):
    current_position = state.copy()
    next_position = current_position.copy()
 
    if ((current_position[0] > 0 + step_size) and (current_position[1] > 0 + step_size)) and check4Obstacle(current_position):
        next_position[0] = current_position[0] - step_size
        next_position[1] = current_position[1] - step_size
        return next_position
    else:
        return None

def bfsSearch(init_state, goal_state, grid_size):

    nodes = list()
    visited_states = list()

    init_node = Node(init_state, 0, None, 0)
    nodes.append(init_node)

    while(nodes):

        current_node = nodes.pop()
        visited_states.append(current_node.getState())

        
        #print("number of visited nodes: ", len(visited_states))

        if np.array_equal(current_node.getState(), goal_state):
            
            print("Goal Reached!")
            print("Total number of nodes explored:", len(visited_states))
            print("The cost of path: ", current_node.getCost())
            full_path, node_path = current_node.getFullPath()
            return full_path, node_path

        else:
            branches = getBranches(current_node, grid_size) 
            
            for branch in branches:
                branch_state = branch.getState()
                if branch_state not in visited_states:
                    nodes.insert(0, branch)
  

def check4Obstacle(state):

    x, y = state
    if ((x - circle_offset_x)**2 + (y - circle_offset_y)**2 <= circle_radius**2): #circle
        return False
    
    elif ((x - ellipse_offset_x)/ellipse_radius_x) **2 + ((y - ellipse_offset_y)/ellipse_radius_y)**2 <= 1: #ellipse
        return False

    elif ((x - c_offset_x) >=0) and ((x - c_offset_x) <= c_length_x) and ((y - c_offset_y) <= 0) and ((c_offset_y - y) <= c_length_y): #c shape
        if ((x - c_offset_x) <= c_width) or ((c_offset_y - y) <= c_width) or ((c_offset_y - y) >= c_length_y - c_width):
            return False
        else:
            return True

    elif (x >= rect_x_min) and (x <= rect_x_max) and (y >= rect_y_min) and (y <= rect_y_max): #rectangle
        if (y > (np.tan(rect_angle) * (x - rect_corner1_x)  + rect_corner1_y)) and (y < (np.tan(rect_angle) * (x -rect_corner4_x)  + rect_corner4_y)):
            if (y > (-np.tan(np.pi/2 - rect_angle) * (x -rect_corner4_x)  + rect_corner4_y)) and (y < (-np.tan(np.pi/2 - rect_angle) * (x -rect_corner3_x)  + rect_corner3_y)):
                return False
            else:
                return True
        else:
            return True  

    # elif #polygon  
    elif (x >= poly_x_min) and (x <= poly_x_max) and (y >= poly_y_min) and (y <= poly_y_max): #polygon
        if (y > (np.tan(poly_angle) * (x - poly_corner1_x)  + poly_corner1_y)) and (y < (np.tan(poly_angle) * (x - poly_corner4_x)  + poly_corner4_y)):
            if (y > (-np.tan(np.pi/2 - poly_angle) * (x - poly_corner4_x)  + poly_corner4_y)):
                if(y < (tan65 * (x - poly_corner6_x)  + poly_corner6_y)) or (y < (tan36 * (x - poly_corner3_x)  + poly_corner3_y)):
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True
            
    else:
        return True  
     

def updateMap(space_map, state, color):
    X, Y, _ = space_map.shape
    transformed_y = state[0]
    transformed_x = X - state[1]
    space_map[transformed_x, transformed_y, :] = color 
    return space_map

def visualize(space_map, visited_states, node_path, result, show_video):
    
        for state in visited_states:
                space_map = updateMap(space_map, state, [0, 255, 0])
                if show_video:
                    cv2.imshow('frame',space_map)
                result.write(space_map)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        for node in node_path:
                pos = node.getState()
                space_map = updateMap(space_map, pos, [0, 0, 255])
                if show_video:
                    cv2.imshow('frame',space_map)
                result.write(space_map)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break


        cv2.waitKey() 
        cv2.destroyAllWindows()



def addObstacles2Map(space_map):

    #circle
    for i in range(circle_offset_x - circle_radius, circle_offset_x + circle_radius):
        for j in range(circle_offset_y - circle_radius, circle_offset_y + circle_radius):
            if (i - circle_offset_x) **2 + (j - circle_offset_y)**2 <= circle_radius**2:
                updateMap(space_map, [i, j], [255, 0, 0])

    #ellipse
    for i in range(ellipse_offset_x - ellipse_radius_x, ellipse_offset_x + ellipse_radius_x):
        for j in range(ellipse_offset_y - ellipse_radius_y, ellipse_offset_y + ellipse_radius_y):
            if ((i - ellipse_offset_x)/ellipse_radius_x) **2 + ((j - ellipse_offset_y)/ellipse_radius_y)**2 <= 1:
                updateMap(space_map, [i, j], [255, 0, 0])


    #C shape
    for i in range(c_offset_x, c_offset_x + c_length_x):
        for j in range(c_offset_y - c_length_y, c_offset_y):
            if (i <= (c_offset_x + c_width)):
                updateMap(space_map, [i, j], [255, 0, 0])
            if (j >= c_offset_y - c_width) or (j <= c_offset_y - c_height - c_width):
                updateMap(space_map, [i, j], [255, 0, 0])

    # rectangle
    for i in range(rect_x_min, rect_x_max):
        for j in range(rect_y_min, rect_y_max):
            if (j >= (np.tan(rect_angle) * (i -rect_corner1_x)  + rect_corner1_y)) and (j <= (np.tan(rect_angle) * (i -rect_corner4_x)  + rect_corner4_y)):
                if (j >= (-np.tan(np.pi/2 - rect_angle) * (i -rect_corner4_x)  + rect_corner4_y)) and (j <= (-np.tan(np.pi/2 - rect_angle) * (i -rect_corner3_x)  + rect_corner3_y)):
                    updateMap(space_map, [i, j], [255, 0, 0])
    
    # polygon
    for i in range(poly_x_min, poly_x_max):
        for j in range(poly_y_min, poly_y_max):
            if (j >= (np.tan(poly_angle) * (i - poly_corner1_x)  + poly_corner1_y)) and (j <= (np.tan(poly_angle) * (i - poly_corner4_x)  + poly_corner4_y)):
                if (j >= (-np.tan(np.pi/2 - poly_angle) * (i - poly_corner4_x)  + poly_corner4_y)):
                    if(j <= (tan65 * (i - poly_corner6_x)  + poly_corner6_y)) or (j <= (tan36 * (i - poly_corner3_x)  + poly_corner3_y)):
                        updateMap(space_map, [i, j], [255, 0, 0])

    return space_map



def main():
    Parser = argparse.ArgumentParser()
    Parser.add_argument("--InitState", nargs='+', type=int, default= [100, 200], help = 'init state')
    Parser.add_argument("--GoalState", nargs='+', type=int, default= [350, 250], help = 'goal state')
    Parser.add_argument('--SaveFolderName', default='/home/sakshi/courses/ENPM661/proj2_sakshi_kakde/Results/', help='Base path of project1 where the results will be saved, Default:/home/sakshi/courses/ENPM661/proj2_sakshi_kakde/Results/')
    Parser.add_argument("--ShowVideo", type=bool, default= False, help = 'Do you ant to see the video?')
    


    Args = Parser.parse_args()
    save_folder_name = Args.SaveFolderName
    init_state = Args.InitState
    goal_state = Args.GoalState
    show_video = Args.ShowVideo
    SaveFileName = save_folder_name + "path.avi"

    # check if init and goal are inside obstacle?
    #check obstacle returns false if obstacle present
    states_correct = False
    if not check4Obstacle(init_state):
        print("Init state not valid.")

    if not check4Obstacle(goal_state):
        print("Goal state not valid.")

    if check4Obstacle(init_state) and check4Obstacle(goal_state):
        states_correct = True




    print("The initial state is ", init_state)
    print("The goal state is ", goal_state)


    space_size = [sizey, sizex]
    # init_state = [300, 200]
    # goal_state = [350, 250]
    step_size = 1
    result = cv2.VideoWriter(SaveFileName,  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         300, (sizex, sizey))

    space_map = np.zeros([space_size[0], space_size[1], 3], dtype=np.uint8)
    space_map = updateMap(space_map, init_state, [0,0,255])
    space_map = updateMap(space_map, goal_state, [0,0,255])
    space_map = addObstacles2Map(space_map)

    print("Press any key to continue after the map pops up.")
    cv2.imshow("map", space_map)
    cv2.waitKey() 
    cv2.destroyAllWindows()

    if states_correct:

        nodes = list()
        visited_states = list()
        node_path = list()
        
        print("Searching...")
        init_node = Node(init_state, 0, None, 0)
        nodes.append(init_node)

        while(nodes):

            current_node = nodes.pop()
            if np.array_equal(current_node.getState(), goal_state):
                
                print("Goal Reached!")
                print("Total number of nodes explored:", len(visited_states))
                print("The cost of path: ", current_node.getCost())
                full_path, node_path = current_node.getFullPath()
                break

            else:
                branches = getBranches(current_node, step_size, space_size) 
                
                for branch in branches:
                    branch_state = branch.getState()
                    if branch_state not in visited_states:
                        nodes.insert(0, branch)
                        visited_states.append(branch_state)

        visualize(space_map, visited_states, node_path, result, show_video)

    else:
        print("Check init and goal states!!!!")

if __name__ == "__main__":
    main()

