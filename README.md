# wallpaper-merge
Simple script to merge portraits into landscape wallpaper sizes

## Documentation
1. This code takes images from the InputFolder and merges them horizontally (left and right).
2. Only images that are in portrait (Height > Width), or a square (1:1) will be merged.
3. Images that are not the above will be outputted without modification.
4. Images are merged randomly.
5. Output image are in the size of 1920x1080, and will be in the folder OutputFolder.
6. If compatible input images are odd numbered, the right side of the final image will be a repeat of a random image.
7. InputFolder and OutputFolder must be in the same directory as merge.py


## Usage
Python3 with OpenCV2 is required.

Run the command `python merge.py <InputFolder> <OutputFolder>`

Commands:
	`python merge.py <InputFolder> <OutputFolder>`

## Note
	Special characters in filenames are not supported in this version.



