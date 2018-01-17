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
1	Can take only png files as input. Currently reading carrier of 1920x1080 and passenger file as 170x170
2	Hold the r,g,b data of passenger file in memory, 170x170x3 8-bit values

Problems:
1	Writing the pixel does not result in 8 pixels

"""
from PIL import Image
import sys

def dec_to_bin(x):
	# from stackoverflow
	# bin(7) returns 0b111
    return (bin(x)[2:])		#returns in the form of list, need to cast using int. e.g. int(dec_to_bin(10))[:7]

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

			r_vals.append(r_bin)
			g_vals.append(g_bin)
			b_vals.append(b_bin)

	#print (r_vals,g_vals,b_vals)

	# reading data of the carrier image
	print carrier

	pixel_cursor = 0
	i = 0
	for x in xrange(carrier.size[0]):
		for y in xrange(carrier.size[1]):
			r, g, b, _ = carrier.getpixel((x, y))
			#if (r % 8 == 1 or g % 8 == 1 or b % 8 == 1):
			#print(r,g,b)

			print r_bin[i:(i+1)], g_bin[i:(i+1)], b_bin[i:(i+1)]
			
			r_cr_bin = dec_to_bin(r)[:7] + r_bin[i:(i+1)]
			g_cr_bin = dec_to_bin(g)[:7] + g_bin[i:(i+1)]
			b_cr_bin = dec_to_bin(b)[:7] + b_bin[i:(i+1)]

			print (dec_to_bin(r),dec_to_bin(g),dec_to_bin(b)), "->", (r_cr_bin,g_cr_bin,b_cr_bin) #

			r = int(r_cr_bin,2)
			g = int(g_cr_bin,2)
			b = int(b_cr_bin,2)
			
			output.putpixel((x,y), (r,g,b))
			"""
			i = i + 1
			if(i == 8):
				i = 0
			"""

			i = i + 1
			if(i == 8):
				break

		if(i == 8):
			break


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
	y = 179
	i = 7
	print (dec_to_bin(x) + " " + dec_to_bin(y))
	for i in xrange(0,8):
		print i
		print (dec_to_bin(x)[:7] + dec_to_bin(y)[i:(i+1)])

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


