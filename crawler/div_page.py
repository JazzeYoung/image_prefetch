#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 14:34:19 2017

@author: ai
function: clip the whole page as individual images
"""

import tensorflow as tf
import numpy as np

import os
import datetime
import random
from PIL import Image
tf.app.flags.DEFINE_string('file_path', '/home/ai/istock', 'Input image directory')
tf.app.flags.DEFINE_string('gap_size', 10, 'Gap between images')
tf.app.flags.DEFINE_string('upper_limit', 450, 'Uppermost line for images')
tf.app.flags.DEFINE_string('lower_limit', 200, 'Lowermost line for images')
tf.app.flags.DEFINE_string('left_limit', 65, 'Leftmost line for images')
tf.app.flags.DEFINE_string('right_limit', 65, 'Rightmost line for images')
tf.app.flags.DEFINE_string('save_dir', '/home/ai/istock/crop', 'Output file path, where to store cropped images')
FLAGS = tf.app.flags.FLAGS


def _get_screenshot(file_path):
  """Returns a list of filenames and inferred class names.

  Args:
    dataset_dir: A directory containing a set of subdirectories representing
      class names. Each subdirectory should contain PNG or JPG encoded images.

  Returns:
    A list of image file paths, relative to `dataset_dir` and the list of
    subdirectories, representing class names.
  """
  #print 'file_path: %s' % file_path
  file_root = os.path.join(file_path, '')
  directories = []
  directories.append(file_root)
  #class_names = []
  #for filename in os.listdir(file_root):
  #  path = os.path.join(file_root, filename)
  #  if os.path.isdir(path):
  #    directories.append(path)
  ##    class_names.append(filename)

  photo_filenames = []
  for directory in directories:
    for filename in os.listdir(directory):
      flist = filename.split('.')
      if len(flist) > 1:
          if(flist[1]=='jpg' or flist[1]=='png'):
              path = os.path.join(directory, filename)
              photo_filenames.append(path)
      else:
          pass

  return photo_filenames


def divide_and_save_images(image_data, height, width, gap):
    """
    divide image by their gap
    images from gap in image_data
    """
    print 'w: %d, h: %d'% (width, height)
    # loop find gap and divide
    y_last = FLAGS.upper_limit
    i = FLAGS.upper_limit 
    while i < height:
        box = 0, i, width, i+gap-1
        cropped = image_data.crop(box)
        #sort(cropped.histogram())
        extremes = cropped.getextrema()
        if extremes[0][0]==extremes[0][1] and extremes[1][0]==extremes[1][1] and extremes[2][0]==extremes[2][1] and i > y_last+100:
            image = image_data.crop((0, y_last, width, i)) 
            print "image rows: 0 %d %d %d" %( y_last, width, i)
            x_last = FLAGS.left_limit
            j = FLAGS.left_limit 
            while j < width:
               h = image.size[1]
               box = j, 0, j+gap-1, h
               cropped = image.crop(box)
               extremes = cropped.getextrema()
               #print 'column:'
               #print extremes
               if extremes[0][0]==extremes[0][1] and extremes[1][0]==extremes[1][1] and extremes[2][0]==extremes[2][1] and j > x_last + 100:
                   save_image = image_data.crop((x_last,y_last, j, i))
                   save_name = "%s/cropped_%d_%d_%d_%d_%d.jpg"%(FLAGS.save_dir, x_last,y_last, i, j, random.randrange(1000) )
                   print 'save_name:%s' % save_name
                   print '%d, %d, %d, %d' % (x_last, y_last, j , i )
                   save_image.save(save_name) 
                   x_last = j + gap
                   j = x_last + 100 # 100 is the limitation for image size(normally all image size > 100*100)
                   if x_last > width - FLAGS.right_limit:
                       break
               else:
                   j = j + 1 
                    
            y_last = i + gap
            i = y_last + 100
            if y_last > height - FLAGS.lower_limit:
               break
        else:
            i = i + 1 
    return
def main():
    """
    divide the whole image for the connected images
    restore each separately
    """
    filenames = _get_screenshot(FLAGS.file_path)
    # Read the filename:
    for i in xrange(len(filenames)):
        print 'filename: %s'% filenames[i]
        image_data = Image.open(filenames[i])
        height = image_data.size[1]
        width = image_data.size[0]
        divide_and_save_images(image_data, height, width, FLAGS.gap_size)
        
if __name__=='__main__':
    main()

