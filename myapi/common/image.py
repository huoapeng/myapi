''' tk_image_view_url_io_resize.py
display an image from a URL using Tkinter, PIL and data_stream
also resize the web image to fit a certain size display widget
retaining its aspect ratio
Pil facilitates resizing and allows file formats other then gif
tested with Python27 and Python33 by vegaseat 18mar2013
'''
# import io
from PIL import Image#, ImageTk
from myapi.model.enum import file_type
from myapi import app
import os, random
from werkzeug.utils import secure_filename

# try:
#   # Python2
#   import Tkinter as tk
#   from urllib2 import urlopen
# except ImportError:
#   # Python3
#   import tkinter as tk
#   from urllib.request import urlopen
def resize(pil_image, w_box, h_box):
    '''
    resize a pil_image object so it will fit into
    a box of size w_box times h_box, but retain aspect ratio
    '''
    pil_image = Image.open(pil_image)
    w, h = pil_image.size
    f1 = 1.0 * w_box / w # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    #print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def getFileUrl(userid, fileType, fileName):
    return 'http://{}/{}{}{}'.format(\
        app.config['SERVER_NAME'], \
        app.config['UPLOAD_FOLDER'], \
        filePath[fileType](userid), \
        fileName)

filePath = {
    file_type.profile : lambda userid: '{}/profile/'.format(userid),
    file_type.version : lambda userid: '{}/version/'.format(userid),
    file_type.authorityPrivateFront : lambda userid: '{}/authorityPrivateFront/'.format(userid),
    file_type.authorityPrivateBack : lambda userid: '{}/authorityPrivateBack/'.format(userid),
    file_type.companyLience : lambda userid: '{}/companyLience/'.format(userid),
    file_type.companyContactCard : lambda userid: '{}/companyContactCard/'.format(userid),
    file_type.work : lambda userid: '{}/work/'.format(userid),
    file_type.workThumbnail : lambda userid: '{}/workThumbnail/'.format(userid),
    file_type.recommend : lambda userid: 'recommend/{}_recommend/'.format(userid),
    file_type.workFile : lambda userid: '{}/workfile/'.format(userid)
}

def allowedFile(fileName, fileType):
    ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
    ALLOWED_FILE_EXTENSIONS = set(['zip', 'rar'])
    if fileType > 50:
        return '.' in fileName and fileName.rsplit('.', 1)[1] in ALLOWED_FILE_EXTENSIONS
    else:
        return '.' in fileName and fileName.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS

def getServerPath(filename, fileType, userid):
    serverPath = os.path.join(app.config['ROOT_PATH'], \
        app.config['UPLOAD_FOLDER'], filePath[fileType](userid))
    if not os.path.exists(serverPath):
        os.makedirs(serverPath)

    fname = secure_filename(filename)
    sf = os.path.join(serverPath, fname)
    
    while os.path.exists(sf):
        randomString = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ',10))
        sf = sf.replace(fname, randomString + fname)
    return sf

# root = tk.Tk()
# # size of image display box you want
# w_box = 400
# h_box = 350
# # find yourself a picture on an internet web page you like
# # (right click on the picture, under properties copy the address)
# # a larger (1600 x 1200) picture from the internet
# # url name is long, so split it
# url1 = "http://freeflowerpictures.net/image/flowers/petunia/"
# url2 = "petunia-flower.jpg"
# url = url1 + url2
# image_bytes = urlopen(url).read()
# # internal data file
# data_stream = io.BytesIO(image_bytes)
# # open as a PIL image object
# pil_image = Image.open(data_stream)
# # get the size of the image
# w, h = pil_image.size
# # resize the image so it retains its aspect ration
# # but fits into the specified display box
# pil_image_resized = resize(pil_image, w_box, h_box)
# # optionally show resized image info ...
# # get the size of the resized image
# wr, hr = pil_image_resized.size
# # split off image file name
# fname = url.split('/')[-1]
# sf = "resized {} ({}x{})".format(fname, wr, hr)
# root.title(sf)
# # convert PIL image object to Tkinter PhotoImage object
# tk_image = ImageTk.PhotoImage(pil_image_resized)
# # put the image on a widget the size of the specified display box
# label = tk.Label(root, image=tk_image, width=w_box, height=h_box)
# label.pack(padx=5, pady=5)
# root.mainloop()