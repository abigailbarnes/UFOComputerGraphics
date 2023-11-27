#!/bin/bash

# Step 1: Interpolating, 
echo "Step 1: Flipping Edges"
python3 starter.py

# Step 1: Creating Frames
echo "Step 2: Creating Frames"
#python3 blender_sample.py
python3 /Applications/Blender.app/Contents/MacOS/blender /Users/abigailbarnes/cmsc23700/final_project/blank.blend --background --python blender_sample.py

# Step 2: Video Processing
echo "Step 3: Video Processing"
python3 save_video.py


echo "Pipeline completed successfully"