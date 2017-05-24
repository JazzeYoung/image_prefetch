"""
 json file for upload images
"""

import json
import os
import datetime

def _get_filenames(file_path):
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

  photo_filenames = []
  for directory in directories:
    for filename in os.listdir(directory):
      flist = filename.split('.')
      if len(flist) > 1:
          if(flist[1]=='jpg' or flist[1]=='png'):
              path = os.path.join('', filename)
              photo_filenames.append(path)
      else:
          pass

  return photo_filenames

def _write_json(filename):
  """filename"""

if __name__=="__main__":
  filenames = _get_filenames('/data/yangqianwen/istock/faces2')
  f = open('./upload.data', 'w')
  for name in filenames:
      #print '%s' % name
      url = os.path.join('http://cms.ishield.cn/files/faces2/',name)
      item = {'url':url, 'group_id':'0', 'image':name, 'score':0.1, 'total_impression':0, 'tag':0, 'file':os.path.join('/data/yangqianwen/istock/faces2/', name)}

      save = json.dumps(item)
      f.write(save)
      f.write('\n')
  f.close()

