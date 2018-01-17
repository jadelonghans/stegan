"""
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
1	Can take only png files as input. 
2	Fills in the first ( length x breadth )	number of pixels. starting from top to bottom, then next column of pixels on the right

Problems:
##Currently reading carrier of 1920x1080 and passenger file as 170x170
1	Writing the pixel does not result in 8 pixels
2	For z=0 values, you cannot address them with [i:i+1], replace them with 0 manually

"""
from PIL import Image
import sys

def dec_to_bin(x):
	# from stackoverflow
	# returns dec_to_bin(12) as 00001100,
	ans = bin(x)[2:]
	while (len(ans) < 8):
		ans = "0" + ans
	return (ans)		#returns in the form of list, need to cast using int before use as integer. e.g. int(dec_to_bin(10))[:7]

def edit_pixel(pic,carrier,output):
	# reading data to be encoded
	r_vals = []
	g_vals = []
	b_vals = []

	#this whole data might be acquired using getpixels() function
	for x in xrange(pic.size[0]):
		for y in xrange(pic.size[1]):
			r, g, b, _ = pic.getpixel((x, y))
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

	# for x in xrange(0,500):		#find the occurence of first red value of pixel which is not "0"
	# 	print r_vals[x]
	# 	if(r_vals[x] != "0"):
	# 		break

	#return 			""""""""""""""""""""""""""""""""""""""""""""""""

	length = len(r_vals)

	# reading data of the carrier image
	print "here"

	pixel_cursor = 0
	i = 0
	for x in xrange(carrier.size[0]):
		for y in xrange(carrier.size[1]):
			r, g, b, _ = carrier.getpixel((x, y))

			# print r_vals[pixel_cursor], g_vals[pixel_cursor], b_vals[pixel_cursor]
			# print r_vals[pixel_cursor][i:(i+1)], g_vals[pixel_cursor][i:(i+1)], b_vals[pixel_cursor][i:(i+1)]

			# if(r_vals[pixel_cursor] == "0"):
			# 	r_cr_bin = dec_to_bin(r)[:7] + "0"	
			# else:
			r_cr_bin = dec_to_bin(r)[:7] + r_vals[pixel_cursor][i:(i+1)]

			# if(g_vals[pixel_cursor] == "0"):	
			# 	g_cr_bin = dec_to_bin(g)[:7] + "0"
			# else:
			g_cr_bin = dec_to_bin(g)[:7] + g_vals[pixel_cursor][i:(i+1)]

			# if(b_vals[pixel_cursor] == "0"):	
			# 	b_cr_bin = dec_to_bin(b)[:7] + "0"
			# else:
			b_cr_bin = dec_to_bin(b)[:7] + b_vals[pixel_cursor][i:(i+1)]


			if(len(r_cr_bin)!=8 or len(g_cr_bin)!=8 or len(b_cr_bin)!=8):
				print "final r,g,b value did not make 8 digits"
				exit(1)

			r = int(r_cr_bin,2)
			g = int(g_cr_bin,2)
			b = int(b_cr_bin,2)

			print "at", (x,y), (dec_to_bin(r),dec_to_bin(g),dec_to_bin(b)), "->", (r_cr_bin,g_cr_bin,b_cr_bin)#, "->", (r,g,b) #

			output.putpixel((x,y), (r,g,b))
	
		# 	i = i + 1
		# 	if(i == 8):
		# 		break
		# if(i == 8):
		# 	break

			i = i + 1
			if(i == 8):
				i = 0	# start from bit position 1 of next pixel
				pixel_cursor = pixel_cursor + 1	#use data of next pixel in array r_vals, g_vals, b_vals 
			if(pixel_cursor == (length-1)):
				print "hiding finished at", (x,y)
				break

		if(pixel_cursor == (length-1)):
			break

	print len(r_vals), "pixels encountered"

def read_pixel(pic,carrier,output):
	#new_img = Image.new('RGB', pic.size)
	edit_pixel(pic,carrier,output)
	output.save("output.png", "PNG", optimize=True)
	return

def usage():
	print ("Usage:\n # stego.py hide file.png carrier.png output.png \n # stego.py show carrier.png output.png")
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
		print

	print (dec_to_bin(x)[:6] + "01")	#checking to see if this add is possible

	if(len(sys.argv) <= 3):
		usage()

	if(sys.argv[1] == "hide" and len(sys.argv) == 5):
		print ("hiding")
		pic = Image.open(sys.argv[2])
		print(pic)
		carrier = Image.open(sys.argv[3])
		print(carrier)
		output = Image.new('RGB', carrier.size)
		read_pixel(pic, carrier, output)
		print(pic.histogram)
		
		
	elif (sys.argv[1] == "show" and len(sys.argv) == 4):
		print ("showing")

	else:
		usage()


