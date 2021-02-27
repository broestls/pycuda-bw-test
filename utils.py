def calc_bws(size, time):
    return format((size / 10**9) / time, '.4f')

def load_images(path, extension):
    # Returns a list of all the images in a directory matching the desired extension
    return glob.glob(path+'*'+extension)

def calc_gbs(size, time):
    return format((size / 1000) / time, '.4f')