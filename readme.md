# Simple Steganography
### Keywords: passenger, carrier, composite_image

## Specifications
-	Can take only png files as input, outputs file in png format.
-	Ensures carrier img is large enough to accommodate passenger img before hiding.
-	Fills in the  ( length x breadth )	number of pixels starting from top-left corner. 
	From top to bottom, then next column of pixels on the right
	
## Algorithm:

### Hide mode:
1.	Encode image height and width as 16 bit digits in the first two columns of carrier image respectively.
	a.	Each bit of 16 bit digits are stored as last bit of pixel from top to bottom. (16 bits of min height required)
2. Replace the (level: var) number of lower bits of first 8 pixels (r,g,b) starting from (2,0) to (2,height)
3. Repeat (2) for all pixels in passenger image, encoding in pixels of carrier image from top to bottom.

### Show mode:
1.	Read header of the file.
	a. 	Collect the LSB of first 16 pixels in 1st and 2nd column of the composite image, to extract passenger image height and width respectively.
2.	Start to read pixel data of passenger image from the 3rd column of composite image.
	a.	Write to the output file once 8 bit pixel data is collected from LSB

## Problems:
### Hide mode:
-	Writing the pixel does not result in 8 pixels (solved)
-	For z=0 values, you cannot address them with [i:i+1], replace them with 0 manually (solved)
-	How to write the info of original file, like resolution of passenger file inside the composite file.
	store magic word(can be 4LSB of length of composite image), length (16-bits), breadth (16-bits)
	
### Show mode:
-	Check if the composite image actually has file included in it.
