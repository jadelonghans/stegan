from PIL import Image
import sys

def main():
	if(len(sys.argv) != 3):
		print "Usage: image_verifier.py file1.png file2.png"
		exit(1)
	
	file1 = Image.open(sys.argv[1])
	file2 = Image.open(sys.argv[2])

	if(file1.size != file2.size):
		print "Image resolution mismatch"
		exit(1)
	else:
		for x in xrange(file1.size[0]):
			for y in xrange (file1.size[1]):
				file1_data = file1.getpixel((x,y))
				file2_data = file2.getpixel((x,y))

				if( file1_data[0] != file2_data[0] or
					file1_data[1] != file2_data[1] or
					file1_data[2] != file2_data[2]
					):

					print "Pixel mismatch at", (x,y)
					exit(-1)

		print "All pixels are identical."
	pass

if __name__ == '__main__':
	main()