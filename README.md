# wallpaper-merge
Simple script to merge a bunch of portrait images into landscape wallpaper sizes, by random order.
This tool is ideal to be used for a wallpaper slideshow.

## Documentation
1. This code takes 2 random images from the InputFolder and merges them horizontally (left and right).
2. Only images that are in portrait (Height > Width), or a square (1:1) will be merged.
3. Images that are does not meet the above will be outputted without modification.
4. Output image are in the size of 1920x1080, and will be in the folder OutputFolder.
5. If compatible input images are odd numbered, the right side of the final image will be a repeat of a random image.
6. InputFolder and OutputFolder must be in the same directory as merge.py


## Usage
Python3 with OpenCV2 is required.

Run the command `python merge.py <InputFolder> <OutputFolder>`

## Note
Special characters in filenames will cause errors.
