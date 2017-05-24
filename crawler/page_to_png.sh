#!/bin/bash

# input the website from list.txt or produce from shifting page=i

#total_page = 9392
for(( i = 200; i < 224; ++i))
do
    url="http://www.istockphoto.com/hk/photos/beautiful-women-face?excludenudity=true&mediatype=photography&page="${i}"&phrase=beautiful%20women%20face&sort=best"
    outfile="/data/yangqianwen/istock/tmp4/"${i}".png"
    /data/yangqianwen/istock/phantomjs-bin/bin/phantomjs /data/yangqianwen/istock/rasterize.js ${url} ${outfile}
done
