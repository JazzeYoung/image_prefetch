#include "opencv2/opencv.hpp"
#include <iostream>
#include <fstream>
#include <string>
using namespace std;
using namespace cv;

void writeDiscard(char*); 
Mat truncateImage(Mat&, vector<Rect> );
int main(int argc, char* argv[])
{
    string xmlPath= "../data/haarcascades/haarcascade_frontalface_default.xml"; //argv[1];//"F:\\opencv3\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml"; 
    CascadeClassifier ccf;   //创建分类器对象
    Mat img=imread(argv[1]);   
    if(!ccf.load(xmlPath))   //加载训练文件
    {
        cout<<"不能加载指定的xml文件"<<endl;
        return 0;
    }
    vector<Rect> faces;  //创建一个容器保存检测出来的脸
    Mat gray;
    Mat truncImg;
    cvtColor(img,gray,CV_BGR2GRAY);
    equalizeHist(gray,gray);
    vector<Rect> people;
    ccf.detectMultiScale(gray,faces,1.1,3,0);
    if(faces.size()==0) {
        CascadeClassifier ccf2;
        ccf2.load("../data/hogcascades/hog_pedistrians.xml");
        ccf2.detectMultiScale(gray, people, 1.1, 3, 0);//, Size(), Size());
        if(people.size() ==0) {
            writeDiscard(argv[1]);
            return 0;
        }
        else {
            CascadeClassifier ccf3;
            ccf3.load("../data/haarcascades/haarcascade_profileface.xml");//"./data/lbpcascades/lbpcascade_profileface.xml");
            ccf3.detectMultiScale(gray, faces, 1.1, 3, 0);//, Size(10,10), Size(300, 300));
            if(faces.size()==0){
                writeDiscard(argv[1]);
                return 0;
            }
            else
                truncImg = truncateImage(img, faces);
        }
    }
    else {
        truncImg = truncateImage(img, faces);
    }
    cout << "cascade finished" << endl;
    char name[80];
    cout << argv[1] << endl;
    strcpy(name, argv[1]+17);
    cout << name << endl;
    string outfile = string(argv[2]) + "/truncated_" + string(name);
    imwrite(outfile, truncImg);
//    for(vector<Rect>::const_iterator iter=faces.begin();iter!=faces.end();iter++)
//    {
//        rectangle(img,*iter,Scalar(0,0,255),2,8); //画出脸部矩形
//    }
//    imwrite("faces.jpg",img);
    return 1;
}

void writeDiscard(char* name) {
    ofstream f;
    f.open("./discard.txt",std::fstream::app);
    f << name << endl;
}


Mat truncateImage(Mat& img, vector<Rect> roi) {
    cout << "truncate begin" <<endl;
    int x, y, width, height;
    int area = 0;
    int idx = 0;
    x = y = width = height = 0;
    Mat truncatedImg;

    if(roi.size() < 1) return truncatedImg;

    for(int i = 0; i < roi.size(); ++i) {
        int tmp = (int)roi[i].area();
        idx = tmp > area? i:idx;
        area = max(tmp, area);
    }
    int size = max(roi[idx].width, roi[idx].height);
    x =(roi[idx].x - cvRound(size/2.0))>0? (roi[idx].x - cvRound(size/2.0)) : 10;
    y = (roi[idx].y - cvRound(size/2.0))>0? (roi[idx].y - cvRound(size/2.0)) : 0;
    width = (x + 2*size > img.cols)? (img.cols - x): (size*2);
    height = (y + 2*size > img.rows)? (img.rows - y): (size*2);
    width = min(width, height);
    height = width;
    cout << x << " " << y << " " << width << " " << height <<endl;
    Rect finalROI(x, y, width, height);
    truncatedImg = img(finalROI);
    return truncatedImg;
}
