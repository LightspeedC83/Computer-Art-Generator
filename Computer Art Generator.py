import random
import math
from PIL import Image
import os

import turtle
screen = turtle.getscreen()
turtle.title("Computer Generated Art -Chase Lowney")
t = turtle.Turtle()
turtle.colormode(255)
turtle.bgcolor("light blue") #changing the background color
t.pencolor("blue") #changing pen color
t.shape("circle") 
t.shapesize(.1,.1,.1) #changing the size of the turtle
t.speed(1000)
t.penup()#putting the pen up

t.home() #putting the turtle at the center 
t.clear() #clearing the screen

#defining functions for later UserWarning
def find_distance(point1, point2): #function to find the distance between two points on the coordinate plane
  output = math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
  return output

def get_angle(point1, point2):
  if point1[0] == point2[0]: #if they have the same x-value
    if point1[1] < point2[1]:
      angle = math.pi/2
    else:
      angle = 3*math.pi/2

  elif point1[0] < point2[0]:
    angle = math.atan( (point2[1]-point1[1])/(point2[0]-point1[0]) )
  elif (point1[0] < point2[0]) and (point1[1] > point2[1]):
    angle = math.atan( (point2[1]-point1[1])/(point2[0]-point1[0]) ) + math.pi*2
  else:
    angle = math.atan( (point2[1]-point1[1])/(point2[0]-point1[0]) ) + math.pi

  return(angle)
    

while True:#asserting whether or not a reference image will be used
  use_reference = input("Would you like to use a reference image?(y/n): ").strip().lower()
  if use_reference in ["y", "yes", "yea", "ye"]:
    use_reference = True
    break
  elif use_reference in ["n", "no"]:
    use_reference = False
    break
  print("Please enter a yes/no answer")

if use_reference: #establishing the canvas size as the size of the reference image
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

  #getting a contrast value (to use when creating the black and white image)
  while True:
    contrast = input("Enter a contrast value for processing the image (2 is the reccomended value): ").strip()
    if contrast.isnumeric():
      contrast = int(contrast)
      if contrast <= 255 and contrast > 0:
        break
        
    print("You must enter a value between 1 and 255")
    
else:
  while True: #getting a canvas size from the user
    canvas_x = input("Enter a canvas size x-value: ").strip()
    canvas_y = input("Enter a canvas size y-value: ").strip()
    if canvas_x.isnumeric() and canvas_y.isnumeric():
      canvas_x = int(canvas_x)
      canvas_y = int(canvas_y)
      break
    print("Please enter only numbers")

#getting the number of points to use as a max in the random distribution
while True:
  min_points = input("Enter a minimum number of points: ").strip()
  max_points = input("Enter a maximum number of points: ").strip()
  if min_points.isnumeric() and max_points.isnumeric():
    min_points = int(min_points)
    max_points = int(max_points)
    if max_points > min_points:
      break
  print("Please enter an integer where the maximum value is greater than the minimum")
  
while True: #deciding whether or not to show the points
  show_points = input("Would you like to show the coordinates?(y/n): ").strip().lower()
  if show_points in ["y", "yes", "yea", "ye"]:
    show_points = True
    break
  elif show_points in ["n", "no"]:
    show_points = False
    break
  print("Please enter a yes/no answer")
  
while True: #getting input for a maximum number of vertices for the shapes
  max_vertices = input("Enter a maximum value of vertices: ").strip()
  if max_vertices.isnumeric():
    max_vertices = int(max_vertices)
    if max_vertices >= 3:
      break
  print("You must enter a number that is 3 or more")


#generating a list of coordinate pairs, if the program is not using a reference image
points = []
if use_reference:
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
        
  random.shuffle(allowed_points) #shuffling the points 
  
  #generating a list of random points that align with the normal map
  for x in range(min_points, max_points):
    while True:
      chosen = random.choice(allowed_points)
      if chosen in points:
        continue
      points.append(chosen)
      break

  #creating a "normal map" of cooridinates/pixel values according to the reference image
  # allowed_points = []
  # index = 0
  # for pixel in binary_pixels:
  #   if pixel[0] == 0: #if the pixel value is black
  #     #finding the x-value
  #     width_pos = index % canvas_x
  #     if width_pos == (canvas_x / 2):
  #       x_value = 0
  #     elif width_pos > (canvas_x /2):
  #       x_value = width_pos - (canvas_x /2)
  #     else: #if width_pos < (canvas_x /2)
  #       x_value = -1*((canvas_x /2) - width_pos)
  
  #     #finding the y-value
  #     distance_from_top = 0 #finding the distance the pixel is from the top of the image
  #     i = index
  #     while i > canvas_x:
  #       i -= canvas_x
  #       distance_from_top += 1
  
  #     if distance_from_top == (canvas_y /2):
  #       y_value = 0
  #     elif distance_from_top > (canvas_y /2):
  #       y_value = -1*(distance_from_top - (canvas_y /2)) 
  #     else: #if distance_from_top < (canvas_y /2)
  #       y_value = (canvas_y /2) - distance_from_top      
        
  #     index +=1
  #     allowed_points.append((x_value, y_value))
  
  #generating a list of random points that align with the normal map
  # for x in range(min_points, max_points):
  #   while True:
  #     chosen = random.choice(allowed_points)
  #     if chosen in points:
  #       continue
  #     points.append(chosen)
  #     break
      
else:
  for x in range(random.randint(min_points, max_points)):
    points.append((random.randint(-1*canvas_x, canvas_x), random.randint(-1*canvas_y, canvas_y)))

if show_points:
  for point in points: #drawing those coordinates, if requested
    t.penup()
    t.goto(point[0],point[1])
    t.dot(4)
t.pencolor("black")

for point in points:
  current_vertices = [point]
  for x in range(1,random.randint(3,max_vertices)):
    closest = points[0]
    shortest = find_distance(point, closest)
    
    for other in points:
      space = find_distance(point, other)
      if (space < shortest) and (other not in current_vertices):
        shortest = space
        closest = other
    current_vertices.append(closest)

  
  #drawing a shape with those verticies that shouldn't cross into itself by calling the get_angle function
  # correct_order = [current_vertices[0]]
  # visited_points = []
  # index = 0
  # for point in current_vertices:
  #   current_copy = current_vertices.copy()
  #   current_point = current_copy.pop(index)
  #   if index != 0:
  #     best = current_copy[0]
  #   else:
  #     best = current_copy[1]
  #   smallest = get_angle(point, best)
    
  #   for other in current_copy:
  #     angle = get_angle(point, other)
  #     if angle < shortest and other not in visited_points:
  #       best = other
  #       smallest = angle
  #   correct_order.append(best)
  #   if point != current_vertices[0]:
  #     visited_points.append(best)
  #   index += 1
  # print(correct_order)
  # #actually drawing the shape
  # t.fillcolor((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
  # t.penup()
  # t.goto((correct_order[0], correct_order[1]))
  # t.beginfill()
  # for vertex in correct_order:
  #   t.pendown()
  #   t.goto((vertex[0], vertex[1]))
  #   t.penup()
  # t.endfill()
  
  #code for drawing the shape, will produce a more spider-web like pattern  --first attempt
  t.fillcolor((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
  t.penup()
  t.goto(current_vertices[0][0], current_vertices[0][1])
  t.begin_fill()
  for vertex in current_vertices:
    t.pendown()
    t.goto(vertex[0], vertex[1])
    t.penup()
  t.pendown()
  t.goto(current_vertices[0][0], current_vertices[0][1])
  
  t.end_fill()

turtle.hideturtle()
