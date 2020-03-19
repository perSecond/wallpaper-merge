import cv2
import os
import sys
import random
import numpy

desired_height = 1080
desired_width = 960
max_ratio = 1
desired_ratio = (float(desired_width)/desired_height)
output_name = 1

in_pth = sys.argv[1]
#in_pth = "Testfile"
out_pth = sys.argv[2]
#out_pth = "output"

list1 = []
list2 = []

# /*
 # Various border types, image boundaries are denoted with '|'

 # * BORDER_REPLICATE:     aaaaaa|abcdefgh|hhhhhhh
 # * BORDER_REFLECT:       fedcba|abcdefgh|hgfedcb
 # * BORDER_REFLECT_101:   gfedcb|abcdefgh|gfedcba
 # * BORDER_WRAP:          cdefgh|abcdefgh|abcdefg
 # * BORDER_CONSTANT:      iiiiii|abcdefgh|iiiiiii  with some specified 'i'
 # */
 
borderType = cv2.BORDER_CONSTANT
color = [255,255,255]

def script(list):
	global output_name
	random.shuffle(list)
	number_infiles = len(list)
	#If only one file
	if(number_infiles == 1):
		print("There is only 1 applicable file! Outputing as it is. Output: " + str(output_name) + ".jpg")
		new_im = resizeImgFull(os.path.join(in_pth, list[0]))
		if not cv2.imwrite(os.path.join(out_pth, str(output_name) + '.jpg'), new_im):
				raise Exception("Could not write image")
		output_name = output_name + 1
	#If odd number of input files
	elif not (number_infiles % 2 == 0):
		print("ODD with " + str(number_infiles) + " number of files!")
		for file1,file2 in zip(list[0:-1:2], list[1::2]):
			in_path1 = os.path.join(in_pth, file1)
			in_path2 = os.path.join(in_pth, file2)
			concatImg(in_path1, in_path2, str(output_name) + '.jpg')
			print("Concatenated " + file1 + " with " + file2 + ". Output: " + str(output_name) + ".jpg")
			output_name = output_name + 1
		file1 = list[-1]
		file2 = list[1::2][random.randint(0, len(list[1::2]))]
		in_path1 = os.path.join(in_pth, file1)
		in_path2 = os.path.join(in_pth, file2)
		concatImg(in_path1, in_path2, str(output_name) + '.jpg')
		print("Concatenated " + file1 + " with " + file2 + ". Output: " + str(output_name) + ".jpg")
		output_name = output_name + 1
	
	else:
		print("EVEN with " + str(number_infiles) + " number of files!")
		for file1,file2 in zip(list[0::2], list[1::2]):
			in_path1 = os.path.join(in_pth, file1)
			in_path2 = os.path.join(in_pth, file2)
			print(in_path1)
			print(in_path2)
			concatImg(in_path1, in_path2, str(output_name) + '.jpg')
			print("Concatenated " + file1 + " with " + file2 + ". Output: " + str(output_name) + ".jpg")
			output_name = output_name + 1

def checkReso(file):
	global output_name
	in_path = os.path.join(in_pth, file)
	
	#stream = open(in_path, 'rb')
	#bytes = bytearray(stream.read())
	#numpyarray = numpy.asarray(bytes, dtype=numpy.uint8)
	#im = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
	
	im = cv2.imread(in_path)
	#print(in_path)
	#print(file[-4:])
	if(file[-4:] == ".gif"):
		print("Filename: " + file + " is not compatible in format, its a gif")
		return
	elif(im.shape[1]/im.shape[0] > desired_ratio): 
		if(im.shape[1]/im.shape[0] > max_ratio): # if image fits better without merging
			print("Filename: " + file + " is not compatible in size, outputing as it is. Output: " + str(output_name) + ".jpg")
			new_im = resizeImgFull(in_path)
			if not cv2.imwrite(os.path.join(out_pth, str(output_name) + '.jpg'), new_im):
				raise Exception("Could not write image")
			output_name = output_name + 1
			return
		else: # if image fits better with merging but resize will be to full width
			list1.append(file)
			return #incompatible
	else: # if image fits better with merging but resize will be to full height
		list2.append(file)
		return #compatible
		
def concatImg(im_pth1,im_pth2, outname):
	end_file = cv2.hconcat((resizeImg(im_pth1),(resizeImg(im_pth2))))
#	  cv2.imshow("end", end_file)
#	  cv2.waitKey(100)
#	  cv2.destroyAllWindows()
	if not cv2.imwrite(os.path.join(out_pth, outname),end_file):
		 raise Exception("Could not write image")
	return

def resizeImgFull(imgpath): #used when image does not require merging
	#stream = open(imgpath, 'rb')
	#bytes = bytearray(stream.read())
	#numpyarray = numpy.asarray(bytes, dtype=numpy.uint8)
	#im = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
	
	im = cv2.imread(imgpath)
	old_size = (im.shape[0],im.shape[1])
	if(im.shape[1]/im.shape[0] > float(desired_width*2)/desired_height):
		desired_size = desired_width*2
		multiply_ratio = float(desired_size)/im.shape[1]
	else:
		desired_size = desired_height
		multiply_ratio = float(desired_size)/im.shape[0]
	new_size = tuple([int(x*multiply_ratio) for x in old_size])
	#print(multiply_ratio)
	#print(str(old_size[1]) + " " + str(old_size[0]))
	#print(str(new_size[1]) + " " + str(new_size[0]))
	# new_size should be in (width, height) format

	im = cv2.resize(im, (new_size[1], new_size[0]))

	delta_w = desired_width*2 - new_size[1]
	delta_h = desired_height - new_size[0]

	top, bottom = delta_h//2, delta_h-(delta_h//2)
	left, right = delta_w//2, delta_w-(delta_w//2)
	#print("top" + str(top) + " left" + str(left))
	
	new_im = cv2.copyMakeBorder(im, top, bottom, left, right, borderType, value=color)
	#cv2.imshow("image", new_im)
	#print("Height:" + str(new_im.shape[0]) + " Width:" + str(new_im.shape[1]))
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	return new_im
	
def resizeImg(imgpath):
	#stream = open(imgpath, 'rb')
	#bytes = bytearray(stream.read())
	#numpyarray = numpy.asarray(bytes, dtype=numpy.uint8)
	#im = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
	
	im = cv2.imread(imgpath)
	
	# if(im.shape[1]/im.shape[0] > w_h_ratio + 0.1):
		# raise Exception("Incompatible size found")
		# exit()
		
	old_size = (im.shape[0],im.shape[1]) # old_size is in (height, width) format
	
	if(im.shape[1]/im.shape[0] > desired_ratio):
		desired_size = desired_width
		multiply_ratio = float(desired_size)/im.shape[1]
	else:
		desired_size = desired_height
		multiply_ratio = float(desired_size)/im.shape[0]
	#print(str(im.shape[1]/im.shape[0]) + " " + str(desired_ratio))

	new_size = tuple([int(x*multiply_ratio) for x in old_size])
	#print(multiply_ratio)
	#print(str(old_size[1]) + " " + str(old_size[0]))
	#print(str(new_size[1]) + " " + str(new_size[0]))
	# new_size should be in (width, height) format

	im = cv2.resize(im, (new_size[1], new_size[0]))

	delta_w = desired_width - new_size[1]
	delta_h = desired_height - new_size[0]
	
	top, bottom = delta_h//2, delta_h-(delta_h//2)
	left, right = delta_w//2, delta_w-(delta_w//2)
	#print("top" + str(top) + " left" + str(left))
	
	new_im = cv2.copyMakeBorder(im, top, bottom, left, right, borderType, value=color)
	#cv2.imshow("image", new_im)
	#print("Height:" + str(new_im.shape[0]) + " Width:" + str(new_im.shape[1]))
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	return new_im

#If input directory does not exist
if not os.path.isdir(in_pth):
	raise Exception("Input directory not found")
	exit()

#Create output directory called output if doesn't exist
if os.path.isdir(out_pth):
	outlist = os.listdir(out_pth) # dir is your directory path
	number_outfiles = len(outlist)
	if not (number_outfiles == 0):
		pass
#		  raise Exception("Output folder exists with files inside")
#		  exit()
	else:
		pass
else:
	os.mkdir(out_pth)

inlist = os.listdir(in_pth) # dir is your directory path

#Check if image resolution is okay	
for file in inlist:
	checkReso(file)

#Loop the input files
#random.shuffle(inlist)

print("\nPerforming merges with padding on top and bottom")
script(list1)

print("\nPerforming merges with padding on left and right")
script(list2)


		