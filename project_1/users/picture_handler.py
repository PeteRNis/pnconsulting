################################################################################
# The purpose of this page, is to handle pictures. Therefore we import PIL
################################################################################

import os
from PIL import Image
from flask import url_for, current_app

#######################################################################################
# Now we create a function that allow the user to handle their profile picture.
#   1. The ext_type allow us to split the filename by the dot, and determine whether
#       we are actually dealing with a png or jpg.
#   2. The storage filename will ensure that the picture is saved as
#       my_username.file_type
#   3. Filepath, says: grab the root path of your application, look for static\profile_pics
#       and then it is going to store the storage filename.
#   4. Output size determines size of the image
#   5. pic says: Take the picture the user uploaded
#   6. pic.thumbnail() squeeses the image to the orientation you like
#   7. At last pic.save ensures that the image is saved
######################################################################################
def add_profile_pic(pic_upload, username):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(username)+'.'+ext_type

    filepath = os.path.join(current_app.root_path,'static\profile_pics',storage_filename)

    output_size = (200,200)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
