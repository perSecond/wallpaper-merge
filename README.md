# wallpaper-merge
Simple script to merge portraits into landscape wallpaper sizes

This code takes images from the InputFolder and merges them horizontally (left and right).
Only images that are in portrait (Height > Width), or a square (1:1) will be merged.
Images that are not the above will be outputted without modification.
Images are merged randomly.
Output image are in the size of 1920x1080, and will be in the folder OutputFolder.
If compatible input images are odd numbered, the right side of the final image will be a repeat of a random image.

Commands:
	python merge.py <InputFolder> <OutputFolder>
