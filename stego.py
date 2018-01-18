"""
Keywords: passenger, carrier, composite_image

Algorithm:
1	Hold in memory the rgb data of each pixel in the passenger file.
2	Replace the LSB of rgb data of each pixel in the carrier file.

Pseudocode:

for each pixel(x,y) in passenger_file:
	convert r,g,b values to binary representation
	store all of r,g,b values of all pixels in array for r,g,b

for each pixel(x,y) in carrier_file:
	convert r,g,b values to binary representation
	#replace LSB of each r,g,b values with that of passenger file
	r = 7bits of carrier + 1 bit of passenger

Specifications
1	Can take only png files as input, outputs file in png format.
2	Ensures carrier img is large enough to accommodate passenger img before hiding.
3	Fills in the  ( length x breadth )	number of pixels starting from top-left corner. 
	From top to bottom, then next column of pixels on the right

Problems:
##Currently reading carrier of 1920x1080 and passenger file as 170x170
1	Writing the pixel does not result in 8 pixels (solved)
2	For z=0 values, you cannot address them with [i:i+1], replace them with 0 manually (solved)
3 	How to write the info of original file, like resolution of passenger file inside the composite file.
	store magic word(can be 4LSB of length of composite image), length (16-bits), breadth (16-bits)

"""
from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt
# import cv2
import sys

def dec_to_bin(x, length = 8):	#default length is 8 bits
	# from stackoverflow
	# returns dec_to_bin(12) as 00001100,
	ans = bin(x)[2:]
	while (len(ans) < length):
		ans = "0" + ans
	return (ans)		#returns in the form of list, need to cast using int before use as integer. e.g. int(dec_to_bin(10))[:7]

def edit_pixel(passenger,carrier,output):
	# reading data to be encoded

	level = 2	#number of LSB positions to use up for encoding
	r_vals = []
	g_vals = []
	b_vals = []

	#this whole data might be acquired using getpixels() function
	for x in xrange(passenger.size[0]):
		for y in xrange(passenger.size[1]):
			r, g, b, _ = passenger.getpixel((x, y))
			#if (r % 8 == 1 or g % 8 == 1 or b % 8 == 1):
			#print(r,g,b)
			#r,g,b = (255,255,0)
			r_bin = dec_to_bin(r)
			g_bin = dec_to_bin(g)
			b_bin = dec_to_bin(b)

			#r_bin = r_bin + (8 - len(r_bin))
			print (r,g,b),"->",(r_bin,g_bin,b_bin)
			if( r_bin != "0" and g_bin != "0" and b_bin != "0"):
				if(len(r_bin)!=8 or len(g_bin)!=8 or len(b_bin)!=8):
					print "passenger r,g,b value did not make 8 digits"
					#exit(1)

			#8 digit binary values of r,g,b stored in the respective lists
			r_vals.append(r_bin)
			g_vals.append(g_bin)
			b_vals.append(b_bin)

	#return 			""""""""""""""""""""""""""""""""""""""""""""""""

	last_index = len(r_vals) - 1

	# reading data of the carrier image
	print ("here")

	pixel_cursor = 0
	i = 0
	for x in xrange(2,carrier.size[0]): 	#start hiding from column 2 (3rd column)
		for y in xrange(carrier.size[1]):
			r, g, b, _ = carrier.getpixel((x, y))

			#if hiding is not finished yet
			if(pixel_cursor <= last_index):
				# print r_vals[pixel_cursor], g_vals[pixel_cursor], b_vals[pixel_cursor]
				# print r_vals[pixel_cursor][i:(i+1)], g_vals[pixel_cursor][i:(i+1)], b_vals[pixel_cursor][i:(i+1)]

				r_cr_bin = dec_to_bin(r)[:(8-level)] + r_vals[pixel_cursor][i:(i+level)]

				g_cr_bin = dec_to_bin(g)[:(8-level)] + g_vals[pixel_cursor][i:(i+level)]

				b_cr_bin = dec_to_bin(b)[:(8-level)] + b_vals[pixel_cursor][i:(i+level)]

				if(len(r_cr_bin) != 8 or len(g_cr_bin) != 8 or len(b_cr_bin) != 8):
					print "final r,g,b value did not make 8 digits"
					exit(1)

				r = int(r_cr_bin,2)
				g = int(g_cr_bin,2)
				b = int(b_cr_bin,2)

				print "at", (x,y), (dec_to_bin(r),dec_to_bin(g),dec_to_bin(b)), "->", (r_cr_bin,g_cr_bin,b_cr_bin)#, "->", (r,g,b) #

			elif(pixel_cursor == (last_index + 1)):
				result_x, result_y = (x,y)	#for showing information at last

			# else:
			# 	print ("at", (x,y), "writing unchanged data")

			# write pixel data to the output file
			output.putpixel((x,y), (r,g,b))	

			#i = i + 1
			i = i + level	#increment to use next (level) no. of bits in next loop
			if(i == 8):
				i = 0	# start from bit position 1 of next pixel
				pixel_cursor = pixel_cursor + 1	#use data of next pixel in array r_vals, g_vals, b_vals 

		"""outer loop"""

	#print (len(r_vals), "pixel data encoded inside the carrier")
	print "Finished"
	print "Encoding finished at cursor", (result_x, result_y) 
	return

def write_header():
	#write the header information into the carrier
	#store resolution
	psngr_height = dec_to_bin(passenger.size[0], 16)		#return height as 1 bit binary values
	psngr_width = dec_to_bin(passenger.size[1], 16)
	print psngr_height,psngr_width

	#write_header() : to encode height and width in first two columns
	print "encoding psngr_height"
	x = 0
	i = 0	#bit_position
	for y in xrange(carrier.size[1]):	
		r, g, b, _ = carrier.getpixel((x, y))
		
		if(i < 16):	#16 digits to be written
			r = dec_to_bin(r)[:7] + psngr_height[i:(i+1)]
			r = int(r,2)
			print r
			i = i + 1

		output.putpixel((x,y), (r,g,b))	

	print "encoding psngr_width"
	x = 1
	i = 0
	for y in xrange(carrier.size[1]):
		r, g, b, _ = carrier.getpixel((x, y))
		
		if(i < 16):	#16 digits to be written
			r = dec_to_bin(r)[:7] + psngr_width[i:(i+1)]
			r = int(r,2)
			print r
			i = i + 1

		output.putpixel((x,y), (r,g,b))	

def hide(passenger,carrier,output):
	#new_img = Image.new('RGB', passenger.size)
	write_header()
	#edit_pixel(passenger,carrier,output)
	output.save("output.png", "PNG", optimize=True)
	
	# hist, bins = np.histogram(output,256,[0,256])
	# plt.hist(output,256,[0,256])
	# plt.title('Histogram for output piture')
	# plt.show()
	return

def read_header():
	dimension = ["",""]
	for x in range(2):	#from first 2 columns
		for y in range(16):
			r, _ , _ = composite_image.getpixel((x, y))
			#print r
			r = dec_to_bin(r,16)
			dimension[x] = dimension[x] +  r[15:16]
		print
	print "dimensions are", int(dimension[0],2), int(dimension[1],2)
	return int(dimension[0],2), int(dimension[1],2)

def show(composite_image, output):
	for x in xrange(2,composite_image.size[0]): 	#start reading from column 2 (3rd column)
		for y in xrange(composite_image.size[1]):
			r, g, b = composite_image.getpixel((x, y))
			#extract bit from each pixel until the l*b pixel is reached, taking (level) number of bits from LSB
		print
	return

def usage():
	print "Usage:\n # stego.py hide file.png carrier.png output.png \n # stego.py show composite_image.png output.png"
	exit()
	
if __name__ == '__main__':
	# Usage
	# stego.py hide file.png carrier.png output.png
	# stego.py show carrier.png output.png
	print("Hello")

	x = 250
	y = 127
	i = 7
	print (dec_to_bin(x) + " " + dec_to_bin(y))
	print "12", dec_to_bin(12)
	for i in xrange(0,8):
		#print i, (dec_to_bin(x)[:7] + dec_to_bin(y)[i:(i+1)])
		print ()

	print dec_to_bin(x)[:6] + "01"	#checking to see if this add is possible

	if(len(sys.argv) <= 3):
		usage()

	if(sys.argv[1] == "hide" and len(sys.argv) == 5):
		print "hiding"
		passenger = Image.open(sys.argv[2])
		print(passenger)
		carrier = Image.open(sys.argv[3])
		print(carrier)
		#need to encode the number of pixels edited too, for decoding
		output = Image.new('RGB', carrier.size)

		#create a system to ensure the carrier image is large enough to hold the header, and the passenger data
		size_required = passenger.size[0] * passenger.size[1]
		size_available = (carrier.size[0] - 2) * carrier.size[1]
		if(carrier.size[1] < 16 or size_available < size_required):
			print "ERROR: Carrier image not large enough to hide passenger image."
			exit(1)

		#start image processing
		hide(passenger, carrier, output)

		#print(passenger.histogram)
		
		
	elif (sys.argv[1] == "show" and len(sys.argv) == 4):
		print "showing"
		composite_image = Image.open(sys.argv[2])

		#retrieve header, if unsuccessful decode not possible
		passenger_height, passenger_width = read_header()		

		output = Image.new('RGB', (passenger_height,passenger_width))	#SIZE IS NOT APPROPRIATE
		show(composite_image, output)

	else:
		usage()


