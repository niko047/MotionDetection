# Python programniccolodiana
# WebCam Motion Detector 

# importing OpenCV, numpy and random libraries

import cv2, random
import numpy as np


def get_base_img():
    #gets the video file from the specified path
    vidcap = cv2.VideoCapture('/Users/niccolodiana/Desktop/IntelliSis/example.mp4')
    
    #reads the video and returns a status (failure or success) and a certain frame from the vid
    success,image = vidcap.read()
    
    #path on where I want the first frame to be stored
    path = "/Users/niccolodiana/Desktop/IntelliSis/frame.jpg"
    
    #saves the frame as a JPEG file in the path
    cv2.imwrite(path, image)
    
    #reads the image in terms of a numpy 2D array with 0 meaning in Black and White
    base_img_matrix = cv2.imread(path, 0)
                    
    #returns the matrix of data in data type int64
    return np.int64(base_img_matrix)

#assigns the base frame of the video
base_matrix = get_base_img()

#will store every frame where movement happens with respect to the base frame
array_of_active_frames = []
    
#monitoring is the action of monitoring 25 pixels at the time once change is detected
monitoring = False

def monitor_changes():
    vidcap = cv2.VideoCapture('/Users/niccolodiana/Desktop/IntelliSis/example.mp4')
    success,image = vidcap.read()
    
    #sets the count of the frame, 0 means first frame will be analyzed
    count = 0
    
    #first threshold that will "ring" the first bell signaling movement
    first_threshold = 100**2 
    
    #while the frame keep coming
    while success:
        
        #take the global variable monitoring as a reference
        global monitoring
        
        #create files JPEG in the specified path containing frames
        cv2.imwrite("/Users/niccolodiana/Desktop/IntelliSis/frame%d.jpg" % count, image)
        
        #same thing as above
        success,image = vidcap.read()
        
        #just tells me in the console that a new frame has been read
        print ('Read a new frame: ', success)
        
        #will read the image files created to extract data 
        next_frame_matrix = cv2.imread("/Users/niccolodiana/Desktop/IntelliSis/frame%d.jpg" % count, 0)
        next_frame_matrix = np.int64(next_frame_matrix)
        
        #computes the difference between each value in the two matrices for the same i,j position
        differences = np.subtract(base_matrix, next_frame_matrix)
        
        #takes the square of every element in the matrix
        differences_squared = differences ** 2
        
        #if the algorithm has not yet identified a change to monitor
        if not monitoring:
            should_append_frame = False
            
            #looping through rows and columns for every element in the matrix
            for row in differences_squared:
                for element in row:
                    
                    #if there is an element greater than the set threshold
                    if element > first_threshold:
                        
                        #start monitoring
                        monitoring = True
                        should_append_frame = True
                        
            #appends frame 
            if should_append_frame:
                array_of_active_frames.append(count)
                        
        if monitoring :
            
            #finds the maximum value inside the matrix
            maxValue = np.amax(differences_squared)
            
            #gets the position of the pixels where that is happening
            result = np.where(differences_squared == maxValue)
            all_coordinates = list(zip(result[0], result[1]))
            
            #since there may be multiple occurrences, randomly selects a point to be tracked
            random_coords = random.choice(all_coordinates)
            
            #separates the tuple assigning the x and the y values
            random_coord_x = random_coords[0]
            random_coord_y = random_coords[1]
            
            #checks if the value of the tracked pixel is borderline in the image
            #assuming the standard image 1552*720 in video
            if random_coord_x in [1,2,3, 1550, 1551, 1552]:
                print('pixel is borderline')
                break
                
            if random_coord_y in [1,2,3, 718, 719, 720]:
                print('pixel is borderline')
                break
            
            #computes an array looping twice from i,j = 1 to 5
            pixel_square_poss = []
            pixel_square_vals = []
            
            #computes the 5x5 square that surrounds the "hot" pixel
            for i in range(random_coord_x - 2, random_coord_x +3):
                for j in range(random_coord_y - 2, random_coord_y +3):
                    pixel_square_vals.append(differences_squared[i][j])
                    pixel_square_poss.append((i , j))
            
            #some sum variable s
            s = 0
            
            #sum the values contained in that square of pixels
            for element in pixel_square_vals:
                s += element
                
            #take the average change in the pixel box
            average_vals = s / len(pixel_square_vals)
                
            #second threshold
            second_threshold = 30**2
            
            #if the average is above a second threshold, append the frame to the array
            if average_vals > second_threshold:
                array_of_active_frames.append(count)
                print(f'Changes in picture small square pixels at frame {count}')
            
            #otherwise just set monitoring to false, and stop monitoring that pixel square
            else:
                print('Monitoring FALSE')
                monitoring = False
                
        #increases the count of the frame and begins the loop again
        count += 1
        
#function call
monitor_changes()
