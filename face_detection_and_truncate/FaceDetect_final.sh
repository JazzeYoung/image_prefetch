#!/bin/bash

g++ face_detection.cpp -o facedetect2 -I/data/yangqianwen/virtualenv/opencv/local/include/opencv -I/data/yangqianwen/virtualenv/opencv/local/include/ -L/data/yangqianwen/virtualenv/opencv/local/lib -lopencv_objdetect -lopencv_features2d -lopencv_imgproc -lopencv_highgui -lopencv_core -lopencv_imgcodecs

# find the jpg files and detect face-> truncate
# dir = `find ./crop3 -type f -name "*.jpg" -exec cat {}`
#dir = `find ./crop3 -name '*.jpg'`;
./facedetect ./crop3/cropped_10_11688_450_12306_814.jpg 

for file in  `find ./final -name '*.jpg'`
do
    if test -f ${file}
    then
#        echo ${file}
        ./facedetect2 "${file}" ./faces2
    fi
#    if test -d ${file}
#    then
#        echo ${file} 是目录
#    fi
done


