import random
import math
from PIL import Image
import os

import turtle
screen = turtle.getscreen()
turtle.title("Computer Generated Art -Chase Lowney")
t = turtle.Turtle()
turtle.colormode(255)
turtle.bgcolor("black") #changing the background color
t.pencolor("blue") #changing pen color
t.shape("circle")
turtle.hideturtle()
t.shapesize(.1,.1,.1) #changing the size of the turtle
t.speed(1000)
t.penup()#putting the pen up

t.home() #putting the turtle at the center 
t.clear() #clearing the screen


##################################
#defining functions for later use#
##################################

def find_distance(point1, point2): #function to find the distance between two points on the coordinate plane
  output = math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
  return output

def get_angle(point1, point2): #function to find the angle between two points
  if point1[0] == point2[0]: #if they have the same x-value
    if point1[1] < point2[1]:
      angle = math.pi/2
    else:
      angle = 3*math.pi/2

  elif point1[0] > point2[0]: #if the second point is in the 2nd or 3rd quadrant 
    angle = math.atan( (point2[1]-point1[1])/(point2[0]-point1[0]) ) + math.pi
  else: #if the second point is in the 1st or 4th quadrant
    if point1[1] > point2[1]: #if it is in the 4th quadrant
      angle = math.atan( (point2[1]-point1[1])/(point2[0]-point1[0]) ) + math.pi*2
    else: #if it is in the 1st quadrant
      angle = math.atan( (point2[1]-point1[1])/(point2[0]-point1[0]) )
  
  return(angle)


#######################
#start of main program#
#######################

print('-'*50 + '\nThis program generates art\n' + '-'*50) #title

#choosing which polygon generation system to use
while True: 
  fancy_generation = input("Choose a mesh generation system: \n\t1) Trig-based polygon generation system \n\t2) Pseudo-random web-like generation\n").strip().lower()
  if fancy_generation in ['1', 'one', 'trig', 'trig based', 'trig-based', 'fancy', 'trigonometry']: #checking input validity
    fancy_generation = True
    break
  elif fancy_generation in ['2', 'two', 'web', 'pseudo random', 'pseudo-random']:
    fancy_generation = False
    break
  print("Please select one of the options")#if input is invalid

#determining the maximum number of connections able to be made per node
while True:
  regulate_nodes = input("Would you like to regulate the number of connections per vertex?(y/n): ").strip().lower()
  if regulate_nodes in ["y", "ye", "yes", "yea", "ya", "1"]:
    regulate_nodes = True
    
    while True: #getting a value for the max number of connections
      max_connections = input("Enter a maximum number of connections per node: ").strip()
      if max_connections.isnumeric():
        max_connections = int(max_connections)
        if max_connections >3:
          break
      print("Please enter an integer that is greater than 3.")
    break
    
  elif regulate_nodes in ["no", "n", "0"]:
    regulate_nodes = False
    max_connections = 1 
    break
  print("Please enter a yes/no answer")


#dealing with reference images (which will be used to create normal maps)
while True: #asserting whether or not a reference image will be used
  use_reference = input("Would you like to use a reference image?(y/n): ").strip().lower()
  if use_reference in ["y", "yes", "yea", "ye"]: #checking input validity
    use_reference = True
    break
  elif use_reference in ["n", "no"]:
    use_reference = False
    break
  print("Please enter a yes/no answer")

if use_reference: #loading the image and establishing the canvas size as the size of the reference image
  while True: #getting the image name
    image_name = input("Enter the name of the image file: ").strip()
    if os.path.exists(image_name):
      break
    print("This file does not exist")

  #getting the image data
  reference = Image.open(image_name)
  image_pixels = reference.getdata()
  canvas_x, canvas_y = reference.size
  print(f"The canvas width will be {canvas_x}, and the height will be {canvas_y}.")


  #determining whether or not to do a binary normal map or to change the shape's color based on the reference
  color_by_image = False #needs to be set to false at the beginning so that if no image was selected, the code will still run
  while True:
    color_by_image = input("In which way would you like to use the image:\n\t1) A normal map, governing the distribution of points\n\t2) A map governing the colors of the shapes\n").strip().lower()
    if color_by_image in ["1", "normal map", "normal", "normals"]:
      color_by_image = False
      
      while True: #getting a contrast value (to use when creating the black and white image)
        contrast = input("Enter a contrast value for processing the image (2 is the reccomended value): ").strip()
        if contrast.isnumeric():
          contrast = int(contrast)
          if contrast <= 10 and contrast > 0:
            break
        print("You must enter a value between 0 and 10")
        
      while True: #determining whether to use white values or black values for the points
        black_normals = input("Would you like to: \n\t1) Use dark values to distribute the points\n\t2) Use light values to distribute the points\n").strip().lower()
        if black_normals in ["1", "dark", "dark values", "black"]:
          black_normals = True
          break
        elif black_normals in ["2", "light","light values", "white"]:
          black_normals = False
          break
        print("Please select one of the options.")
        
      while True: #determining if the image should be used to color the points on the normal map
        regulate_normal_color = input("Would you like to determine polygon color based on the reference?(y/n): ").strip().lower()
        if regulate_normal_color in ["y", "ye", "yes", "1", "yea"]:
          regulate_normal_color = True
          break
        elif regulate_normal_color in ["n", "no", "0"]:
          regulate_normal_color = False
          break
        print("Please enter a yes/no answer.")
        
      break
    elif color_by_image in ['2', "colors"]:
      color_by_image = True
      break
    print("Please select one of the options.")
    
    
else:
  while True: #getting a canvas size from the user, if no reference image is specified
    canvas_x = input("Enter a canvas size x-value: ").strip()
    canvas_y = input("Enter a canvas size y-value: ").strip()
    if canvas_x.isnumeric() and canvas_y.isnumeric():
      canvas_x = int(canvas_x)
      canvas_y = int(canvas_y)
      break
    print("Please enter only numbers")


#getting the number of points to use as a min and max in the random distribution
while True:
  min_points = input("Enter a minimum number of points: ").strip()
  max_points = input("Enter a maximum number of points: ").strip()
  if min_points.isnumeric() and max_points.isnumeric(): #input check
    min_points = int(min_points)
    max_points = int(max_points)
    if max_points > min_points:
      break
  print("Please enter an integer where the maximum value is greater than the minimum")


#deciding whether or not to show the points
while True: 
  show_points = input("Would you like to show the coordinates?(y/n): ").strip().lower()
  if show_points in ["y", "yes", "yea", "ye"]: #input check
    show_points = True
    break
  elif show_points in ["n", "no"]:
    show_points = False
    break
  print("Please enter a yes/no answer")

#getting input for a maximum number of vertices for the shapes
while True: 
  max_vertices = input("Enter a maximum value of vertices: ").strip()
  if max_vertices.isnumeric(): #input check
    max_vertices = int(max_vertices)
    if max_vertices >= 3:
      break
  print("You must enter a number that is 3 or more")


#generating a list of coordinate pairs, if the program is using a reference image
points = []
if use_reference and not color_by_image:
  #getting the image to a black and white image 
  binary_pixels = []
  for pixel in image_pixels:
    average = (pixel[0] + pixel[1] + pixel[2]) //3
    if average < (255//contrast):
      binary_pixels.append((0, 0, 0))
    else:
      binary_pixels.append((255, 255, 255))
  binary_image = Image.new("RGB", reference.size)
  binary_image.putdata(binary_pixels)
  binary_image.save("normal map.jpg")
  

  #creating a "normal map" of cooridinates/pixel values according to the reference image using the PIL built in coordinate system
  allowed_points = []
  for x_value in range(canvas_x//2*-1, canvas_x//2):
    for y_value in range(canvas_y//2*-1, canvas_y//2):
      coordinate = (x_value, y_value)
      pixel_value = binary_image.getpixel(coordinate)
      
      if black_normals: #if the program should distribute points onto the black parts of the image
        if pixel_value == (0,0,0):
          converted_coordinate = (coordinate[0], coordinate[1]*-1) #doing some reflection and translation to convert the coordiantes from the PIL format 
          if converted_coordinate[0] > 0 and converted_coordinate[1] > 0: #if the coordinate is in quadrant 1
            converted_coordinate = (converted_coordinate[0]-(canvas_x/2), converted_coordinate[1]-(canvas_y/2))
          elif converted_coordinate[0] < 0 and converted_coordinate[1] > 0: #if it is in quadrant 2
            converted_coordinate = (converted_coordinate[0]+(canvas_x/2), converted_coordinate[1]-(canvas_y/2))
          elif converted_coordinate[0] < 0 and converted_coordinate[1] < 0: #if it is in quadrant 3
            converted_coordinate = converted_coordinate[0]+(canvas_x/2), converted_coordinate[1]+(canvas_y/2)
          elif converted_coordinate[0] > 0 and converted_coordinate[1] < 0: #if it is in quadrant 4
            converted_coordinate = converted_coordinate[0]-(canvas_x/2), converted_coordinate[1]+(canvas_y/2)
          allowed_points.append(converted_coordinate)

      elif not black_normals: #if the program should distribute points onto the white parts of the image
        if pixel_value == (255,255,255): #basically doing the same thing with the translations of coordinates before appending them
          converted_coordinate = (coordinate[0], coordinate[1]*-1) #doing some reflection and translation to convert the coordiantes from the PIL format 
          if converted_coordinate[0] > 0 and converted_coordinate[1] > 0: #if the coordinate is in quadrant 1
            converted_coordinate = (converted_coordinate[0]-(canvas_x/2), converted_coordinate[1]-(canvas_y/2))
          elif converted_coordinate[0] < 0 and converted_coordinate[1] > 0: #if it is in quadrant 2
            converted_coordinate = (converted_coordinate[0]+(canvas_x/2), converted_coordinate[1]-(canvas_y/2))
          elif converted_coordinate[0] < 0 and converted_coordinate[1] < 0: #if it is in quadrant 3
            converted_coordinate = converted_coordinate[0]+(canvas_x/2), converted_coordinate[1]+(canvas_y/2)
          elif converted_coordinate[0] > 0 and converted_coordinate[1] < 0: #if it is in quadrant 4
            converted_coordinate = converted_coordinate[0]-(canvas_x/2), converted_coordinate[1]+(canvas_y/2)
          allowed_points.append(converted_coordinate)
          
  random.shuffle(allowed_points) #shuffling the points 
  
    
  #generating a list of random points that align with the normal map
  points_left = allowed_points.copy()
  for x in range(random.randint(min_points, max_points)):
    if len(points_left) > 0:
      points.append(points_left.pop(random.randint(0, len(points_left)-1) ))
    else:
      print(f"Only {len(points)} points were able are able to be made, this is constrained by the size of the input image")

if color_by_image or regulate_normal_color: #if we are to use the image as a color map (image_pixels contains the pixel data)
  color_map = {}
  for x_value in range(math.ceil(canvas_x/2*-1), math.ceil(canvas_x/2)):
    for y_value in range(math.ceil(canvas_y/2*-1), math.ceil(canvas_y/2)):
      coordinate = (x_value, y_value) 
      pixel_value = image_pixels.getpixel(coordinate)
      #doing some translation to convert the coordiantes from the PIL format 
      if coordinate[0] > 0 and coordinate[1] > 0: #if the coordinate is in quadrant 1
        coordinate = (coordinate[0]-(canvas_x/2), coordinate[1]-(canvas_y/2))
      elif coordinate[0] < 0 and coordinate[1] > 0: #if it is in quadrant 2
        coordinate = (coordinate[0]+(canvas_x/2), coordinate[1]-(canvas_y/2))
      elif coordinate[0] < 0 and coordinate[1] < 0: #if it is in quadrant 3
        coordinate = coordinate[0]+(canvas_x/2), coordinate[1]+(canvas_y/2)
      elif coordinate[0] > 0 and coordinate[1] < 0: #if it is in quadrant 4
        coordinate = coordinate[0]-(canvas_x/2), coordinate[1]+(canvas_y/2)
      else:
        coordinate = (0,0)

      coordinate = (int(coordinate[0]), int(coordinate[1]*-1)) #important that the y axis is reflected
      color_map[coordinate] = pixel_value

  if color_by_image:  #this code won't run if we are useing a normal map, making sure that the program won't add vertices to the canvas in any old place 
    for x in range(random.randint(min_points, max_points)): 
      point = (random.randint(int(-1*canvas_x//2), int(canvas_x//2)), random.randint(int(-1*canvas_y//2), int(canvas_y//2)))
      if point in color_map:
        points.append(point)
        
#getting the list of coordinate pairs if no reference image is used for a normal map
elif not use_reference: #if use_reference is false, we still may be using a normal map, so we don't want this code to run and put points randomly.
  for x in range(random.randint(min_points, max_points)):
    points.append((random.randint(-1*canvas_x, canvas_x), random.randint(-1*canvas_y, canvas_y)))

#drawing all the coordinates, if requested
if show_points:
  for point in points: 
    t.penup()
    t.goto(point[0],point[1])
    t.dot(4)
t.pencolor("black")

#creatinng a dictionary of the points and the amount of times they are allowed to be used
point_uses = {}
for point in points:
  point_uses[point] = max_connections

#generating a list of coordinates that are close to eachother to use to draw the shape
for point in points:
  current_vertices = [point]
  for x in range(0,random.randint(3,max_vertices)):
    first_index = points.index(point) #this whole first index thing is done so that the first list of points the program generates isn't all that first point.
    if first_index == 0:
      first_index = 1
    else:
      first_index -=1
      
    closest = points[first_index]
    shortest = find_distance(point, closest)
    for other in points: #finding the point with the shortest distance
      space = find_distance(point, other)
      if point_uses[other] > 0: #makes sure that node doesn't have too many connections
        if (space < shortest) and (other not in current_vertices):
          shortest = space
          closest = other
        #if point[1] > 0: #if it is above the x axis
          #if (space < shortest) and (other not in current_vertices) and (point[1] > other[1]):
            #shortest = space
            #closest = other
        #else: #if it's below
          #if (space < shortest) and (other not in current_vertices) and (point[1] < other[1]):
            #shortest = space
            #closest = other

          
    current_vertices.append(closest)
    if regulate_nodes: #it will only decrease the connections availiable for that point if the user had decided to regulate the nodes
      point_uses[closest] -= 1
      
  #drawing a shape with those verticies that shouldn't cross into itself by calling the get_angle function --the fancy way
  if fancy_generation:
    lowest_y = current_vertices[0]#finding the point with the lowest y coordinate to use as the first point
    for point in current_vertices:
      if point[1] < lowest_y[1]:
        lowest_y = point
    
    correct_order = [] #getting the best order to draw them in
    availiable_points = current_vertices.copy()
    next_point = availiable_points.index(lowest_y)
    for point in current_vertices:
      main_point = availiable_points.pop(next_point) #removing the next point from the list of availiable points
      correct_order.append(main_point)
      #finding the next next point
      try:
        smallest_angle = get_angle(main_point, availiable_points[0])
        best_point = availiable_points[0]
      except IndexError:
        break
      for other in availiable_points: #comparing the angles with all the points to find the next point to go to
        angle = get_angle(main_point, other)
        if angle < smallest_angle:
          best_point = other
          smallest_angle = angle
          
      next_point = availiable_points.index(best_point)
    
    #actually drawing the shape
    if color_by_image or regulate_normal_color: #yes, the bit where these parameters were selected could be condensed so that this only uses one variable, but I'm lazy so....
      #getting the average of all the colors represented by the points it wants to draw
      average_r = 0
      average_g = 0
      average_b = 0
      
      for point in correct_order:
        point = (int(point[0]), int(point[1]))
        average_r += color_map[point][0]
        average_g += color_map[point][1]
        average_b += color_map[point][2]
      average_r //= len(correct_order)
      average_g //= len(correct_order)
      average_b //= len(correct_order)
      t.fillcolor(average_r, average_g, average_b) #setting the fill color to the average
    else:
      t.fillcolor((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) #setting fill color to random
      
    t.goto((correct_order[0][0], correct_order[0][1])) #drawing it
    t.begin_fill() 
    for vertex in correct_order:
      t.goto((vertex[0], vertex[1]))
    
    t.goto((correct_order[0][0], correct_order[0][1]))
    t.end_fill()

  #the alternative method for drawing the shape, will produce more spidery images
  else:
    if color_by_image or regulate_normal_color:
      #getting the average of all the colors represented by the points it wants to draw
      average_r = 0
      average_g = 0
      average_b = 0
      for point in current_vertices:
        point = (int(point[0]), int(point[1]))
        average_r += color_map[point][0]
        average_g += color_map[point][1]
        average_b += color_map[point][2]
      average_r //= len(correct_order)
      average_g //= len(correct_order)
      average_b //= len(correct_order)
      t.fillcolor(average_r, average_g, average_b) #setting the fill color to the average
      
    else:
      t.fillcolor((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) #setting random fill color
    t.penup()
    t.goto(current_vertices[0][0], current_vertices[0][1]) #drawing it as it appeared when gathered as points closest to one main point
    t.begin_fill()
    for vertex in current_vertices:
      t.pendown()
      t.goto(vertex[0], vertex[1])
      t.penup()
    t.pendown()
    t.goto(current_vertices[0][0], current_vertices[0][1])
    
    t.end_fill()


