import os
import numpy as np
from pathlib import Path
# pip install imageio
# pip install imageio-ffmpeg
import imageio
from PIL import Image


def save_video(path):
    # save a video using of all images in a folder
    file_paths = Path(path).glob("*.png")


    #my added code for the background
    background_image_path = "background.jpg" 
    background_image = Image.open(background_image_path)
    background_image_arr = np.asarray(background_image)

    # imgs is a list of numpy array images
    imgs = []
    '''for file_path in sorted(file_paths):
        print(file_path)
        img = Image.open(file_path)
        img_arr = np.asarray(img)
        imgs.append(img_arr)'''
    
    for file_path in sorted(file_paths):
        print(file_path)
        img = Image.open(file_path)
        img_arr = np.asarray(img)

        #print(background_image_arr.shape)
        #print(img_arr.shape)

        img_arr = img_arr[:, :, :3]

        background_image_resized = background_image.resize((960, 540))
        background_image_arr = np.asarray(background_image_resized)

        # Blend the frame with the background image
        blended_img_arr = np.where(img_arr != 0, img_arr, background_image_arr)

        imgs.append(blended_img_arr)

    
    fps = 50 # frames per second
    #fps = 5

    write_to = 'output/animations/{}.mp4'.format('animation')  # have a folder of output where output files could be stored.
    writer = imageio.get_writer(write_to, format='mp4', mode='I', fps=fps)

    for img in imgs:
        writer.append_data(img[:])
    writer.close()

# Here is an example which saves images in the animation_renders folder to a video file at 5 fps
save_video('/Users/abigailbarnes/cmsc23700/final_project/output/animation_renders')