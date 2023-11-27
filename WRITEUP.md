CMSC Final Project Write Up

Hi all,

For my Final Project, I used a downloaded a free UFO.obj mesh (https://www.turbosquid.com/3d-models/ufo-3d-model-1759467) as well as the spot.obj file from previous coursework.

For this assignment, I implimented edge flips on the spot.obj using the code from Assignment 3 as a guide. Specifically, I copied over the *meshing* folder elements as well as `starter.py`. Within the *meshing* folder, I modified the followng:
1. edit.py: At the end of the file, I included a class called EdgeFlip and, similar to Laplacian Smoothing, I built out my EdgeFlip related functions.One note is that, unlike Laplacian Smoothing, my implimentation of edge flipping takes in one edge to be referenced for flipping at a time.
2. mesh.py: I included the corresponding function for edgeFlip starting on line 63. I simply import the EdgeFlip class and call the function to flip the edge accordingly.
3. __init__.py: I added EdgeFlip to line four (from .edit)
4. starter.py: Outside of the meshing folder (one level back), I flip the edges. I create an array that the code self populates of edges to flip, and then those edges are flipped within `if name == "main":`. The output of the edge flips is `spot_edge_flipped.obj`.
5. blender_sample.py: I started by changing the path of the obj files that are called so they are no longer being called from data (this is important to note as starter.py saves the edge flipped obj file on the same level as the starter.py file, a.k.a. not in the data folder). Then, I modified a few of the trivial atributes of the file (color change, removal of the ground plane, and the addition of a second object). Under `if __name__ == "__main__":` on line 148, I include most of my modifications to the key frame outputs. I create a second obj mesh for the UFO (where as the first was the spot cow), change the number of frames from 10 to 500, create my splines for y-value interpolation for the cow and UFO (lines 196 - 201), and updated the locations and rotations for each obj. I then added the second UFO obj to the animation key frames. 
6. save_video.py: I added a background image (and the related code to superimpose the cow/UFO key frames onto the background image) (lines 16 - 18). I then modified the imgs loop to include the background (lines 28 - 44), and changed the key frames to 500 so that the animation was meeting the 10 second requirement. 
7. pipeline.sh: I run three of the python files in this bash script. I first call starter.py to flip the edges of the spot.obj file and create the output of `spot_edgeflipped.obj`, I then run blender_sample.py to create the animation key frames, and finally I run `save_video.py`. 


In summary, I ultimately selected Edge Flip for my algorithm, create a new obj file for the flipped edge obj, and create my key frames using bsplines for the y-value interpolation for the UFO and edge flipped spot objs. I then included sound effects in iMovie from the .mp4 that is output from running `save_video.py`. 

By calling `./pipeline.sh`, the user should be able to run the script created to run all steps in the pipeline in sequential order. 
