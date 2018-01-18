"""
Dangol Jeshan
Keywords: passenger, carrier, composite_image

Algorithm:
Hide mode:
1	Encode image height and width as 16 bit digits in the first two columns of carrier image respectively.
	a.	Each bit of 16 bit digits are stored as last bit of pixel from top to bottom. (16 bits of min height required)
2	Replace the (level: var) number of lower bits of first 8 pixels (r,g,b) starting from (2,0) to (2,height)
3	Repeat (2) for all pixels in passenger image, encoding in pixels of carrier image from top to bottom.

Show mode:
1	Read header of the file.
	a. 	Collect the LSB of first 16 pixels in 1st and 2nd column of the composite image, to extract passenger image height and width respectively.
2	Start to read pixel data of passenger image from the 3rd column of composite image.
	a.	Write to the output file once 8 bit pixel data is collected from LSB

Specifications
1	Can take only png files as input, outputs file in png format.
2	Ensures carrier img is large enough to accommodate passenger img before hiding.
3	Fills in the  ( length x breadth )	number of pixels starting from top-left corner. 
	From top to bottom, then next column of pixels on the right

Problems:
	Hide mode:
1	Writing the pixel does not result in 8 pixels (solved)
2	For z=0 values, you cannot address them with [i:i+1], replace them with 0 manually (solved)
3 	How to write the info of original file, like resolution of passenger file inside the composite file.
	store magic word(can be 4LSB of length of composite image), length (16-bits), breadth (16-bits)
	
	Show mode:
1	Check if the composite image actually has file included in it.

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
	
	#Part1: reading data to be encoded
	r_vals = []
	g_vals = []
	b_vals = []

	#this whole data might be acquired using getpixels() function
	for x in xrange(passenger.size[0]):
		for y in xrange(passenger.size[1]):
			data = passenger.getpixel((x, y)) #returns a tuple of (r, g, b, _ )
			
			r = data[0]
			g = data[1]
			b = data[2]
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

	#Part2: encoding into carrier
	pixel_cursor = 0
	i = 0
	for x in xrange(2,carrier.size[0]): 	#start hiding from column 2 (3rd column)
		for y in xrange(carrier.size[1]):
			data = carrier.getpixel((x, y))

			r = data[0]
			g = data[1]
			b = data[2]

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

			i = i + level	#increment to use next (level) no. of bits in next loop
			if(i == 8):
				i = 0	# start from bit position 1 of next pixel
				pixel_cursor = pixel_cursor + 1	#use data of next pixel in array r_vals, g_vals, b_vals 

		"""outer loop"""

	#print (len(r_vals), "pixel data encoded inside the carrier")
	print "Encoding finished at cursor", (result_x, result_y) 
	return

def write_header():
	#write the header information into the carrier
	psngr_dimension = []
	#store resolution
	psngr_dimension.append (dec_to_bin(passenger.size[0], 16))	#return height as 1 bit binary values
	psngr_dimension.append (dec_to_bin(passenger.size[1], 16))
	print psngr_dimension[0], psngr_dimension[1]

	#write_header() : to encode height and width in first two columns
	for x in xrange(2):
		i = 0
		payload = psngr_dimension[x]
		for y in xrange(carrier.size[1]):
			data = carrier.getpixel((x, y))
		
			r = data[0]
			g = data[1]
			b = data[2]
			if(i < 16):	#16 digits to be written
				r = dec_to_bin(r)[:7] + payload[i:(i+1)]
				r = int(r,2)
				#print r
				i = i + 1
			else:
				break;
			output.putpixel((x,y), (r,g,b))	
	"""
	print "encoding psngr_height"
	x = 0
	i = 0	#bit_position
	for y in xrange(carrier.size[1]):	
		data = carrier.getpixel((x, y))
		
		r = data[0]
		g = data[1]
		b = data[2]
		if(i < 16):	#16 digits to be written
			r = dec_to_bin(r)[:7] + psngr_height[i:(i+1)]
			r = int(r,2)
			#print r
			i = i + 1

		output.putpixel((x,y), (r,g,b))	

	print "encoding psngr_width"
	x = 1
	i = 0
	for y in xrange(carrier.size[1]):
		data = carrier.getpixel((x, y))

		r = data[0]
		g = data[1]
		b = data[2]
		
		if(i < 16):	#16 digits to be written
			r = dec_to_bin(r)[:7] + psngr_width[i:(i+1)]
			r = int(r,2)
			#print r
			i = i + 1

		output.putpixel((x,y), (r,g,b))	
	"""

def hide(passenger,carrier,output):
	#new_img = Image.new('RGB', passenger.size)
	write_header()
	edit_pixel(passenger,carrier,output)
	
	# hist, bins = np.histogram(output,256,[0,256])
	# plt.hist(output,256,[0,256])
	# plt.title('Histogram for output piture')
	# plt.show()
	return

def read_header():
	dimension = ["",""]
	for x in range(2):	#from first 2 columns
		for y in range(16):
			data = composite_image.getpixel((x, y))
			#print r
			r = data[0]
			r = dec_to_bin(r,16)
			dimension[x] = dimension[x] +  r[15:16]
		print
	print "dimensions are", int(dimension[0],2), int(dimension[1],2)
	return int(dimension[0],2), int(dimension[1],2)

def show(composite_image, output):
	pixel_limit = output.size[0]*output.size[1]	#total number of pixels in the passenger image
	pixel_wrote = 0
	out_r = ""
	out_g = ""
	out_b = ""

	# the coordinates of passenger image being written
	passenger_x = 0
	passenger_y = 0

	for x in xrange(2,composite_image.size[0]): 	#start reading from column 2 (3rd column)
		for y in xrange(composite_image.size[1]):

			data = composite_image.getpixel((x, y))
			r = data[0]
			g = data[1]
			b = data[2]
			#extract bit from each pixel until the l*b pixel is reached, taking (level) number of bits from LSB
			if(pixel_wrote >= pixel_limit):
				return
			""""""
			out_r = out_r + dec_to_bin(r) [ 8 - level : 8 ]
			out_g = out_g + dec_to_bin(g) [ 8 - level : 8 ]
			out_b = out_b + dec_to_bin(b) [ 8 - level : 8 ]

			if(len(out_r) == 8):
				pixel_wrote += 1

				r = int(out_r,2)
				g = int(out_g,2)
				b = int(out_b,2)
				print "at", (passenger_x, passenger_y), ", wrote", (r, g, b) , "~", (out_r, out_g, out_b)
				output.putpixel( (passenger_x, passenger_y), ( r, g, b) )

				#advance the passenger image coordinates
				if(passenger_y < (output.size[1] - 1)):
					passenger_y += 1
				else:
					passenger_y = 0
					passenger_x += 1

				out_r = ""
				out_g = ""
				out_b = ""

			""""""
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

	"""program starts here"""
	level = 2	#number of LSB positions to use up for encoding

	if(len(sys.argv) <= 3):
		usage()

	if(sys.argv[1] == "hide" and len(sys.argv) == 5):
		print "hiding"
		passenger = Image.open(sys.argv[2])
		#print(passenger)
		carrier = Image.open(sys.argv[3])
		#print(carrier)

		output = Image.new('RGB', carrier.size)

		#create a system to ensure the carrier image is large enough to hold the header, and the passenger data
		size_required = passenger.size[0] * passenger.size[1] * (8/level)
		size_available = (carrier.size[0] - 2) * carrier.size[1] 	#2 columns are used to encode image resolution
		if(carrier.size[1] < 16 or size_available < size_required):
			print "ERROR: Carrier image not large enough to hide passenger image."
			exit(1)
		elif(passenger.size[0] > 32767 or passenger.size[1] > 32767):
			print "ERROR: Max height/width (= 32767) exceeded."
			exit(1)

		#start image processing
		hide(passenger, carrier, output)
		output.save(sys.argv[4], "PNG", optimize=True)
		#print(passenger.histogram)
		
		
	elif (sys.argv[1] == "show" and len(sys.argv) == 4):
		print "showing"
		composite_image = Image.open(sys.argv[2])

		#retrieve header, if unsuccessful decode not possible
		passenger_height, passenger_width = read_header()		

		output = Image.new('RGB', (passenger_height,passenger_width))	
		show(composite_image, output)
		output.save(sys.argv[3], "PNG", optimize=True)

	else:
		usage()