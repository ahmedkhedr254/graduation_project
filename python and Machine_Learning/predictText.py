import cv2
import os
import numpy as np
from sklearn.cluster import KMeans
from keras.models import model_from_yaml
import numpy as np
from keras import backend as K
from flask import Flask, request, make_response
from tensorflow.python.keras.backend import set_session
from flask_uploads import UploadSet, configure_uploads, IMAGES

myImages=[]
visited=[]
def distanceBetwenTwoPoint(x1,y1,x2,y2):
    return np.sqrt(((y1-y2)**2)+((x1-x2)**2))
    
def nearestCharacterFromLeft(inndex,contour):
    global myImages
    minn=1000000
    res=0
    x,y,w,h = cv2.boundingRect(contour)
    for i in range(len(myImages)):
        if not i==inndex:
            xi,yi,wi,hi = cv2.boundingRect(myImages[i])
            if xi+wi<((x+(x+w))/2):
                if distanceBetwenTwoPoint(xi+wi,(yi+hi+yi)/2,x,(y+y+h)/2)<minn:
                    minn=distanceBetwenTwoPoint(xi+wi,(yi+hi+yi)/2,x,(y+y+h)/2)
                    res=i
    return res
        
    
def nearestCharacterFromRight(inndex,contour):
    global myImages
    minn=100000
    res=0
    x,y,w,h = cv2.boundingRect(contour)
    for i in range(len(myImages)):
        if not i==inndex:
            xi,yi,wi,hi = cv2.boundingRect(myImages[i])
            if xi>((x+(x+w))/2):
                if distanceBetwenTwoPoint(xi,(yi+yi+hi)/2,x+w,(y+y+h)/2)<minn:
                    minn=distanceBetwenTwoPoint(xi,(yi+yi+hi)/2,x+w,(y+y+h)/2)
                    res=i
    return res


def dfsLeft(i,LineComponentList):
    global visited
    global myImages
    visited[i]=True
    LineComponentList.append(i)
    myLeftChar=nearestCharacterFromLeft(i,myImages[i])
   # myRightChar=nearestCharacterFromRight(i,LastContourList,LastContourList[i])
    x,y,w,h = cv2.boundingRect(myImages[i])
    xLeft,yLeft,wLeft,hLeft = cv2.boundingRect(myImages[myLeftChar])
    #xRight,yRight,wRight,hRight = cv2.boundingRect(myImages[myRightChar])
    if( yLeft <(y+h) and (yLeft+hLeft)>y )and not visited[myLeftChar]:
        dfsLeft(myLeftChar,LineComponentList)
        
        
def dfsRight(i,LineComponentList):
    global myImages
    global visited
    visited[i]=True
    LineComponentList.append(i)
  #  myLeftChar=nearestCharacterFromLeft(i,myImages,LastContourList[i])
    myRightChar=nearestCharacterFromRight(i,myImages[i])
    x,y,w,h = cv2.boundingRect(myImages[i])
  #  xLeft,yLeft,wLeft,hLeft = cv2.boundingRect(LastContourList[myLeftChar])
    xRight,yRight,wRight,hRight = cv2.boundingRect(myImages[myRightChar])
    
        
    if (yRight <(y+h)and (yRight+hRight)>y) and  not visited[myRightChar]:
        dfsRight(myRightChar,LineComponentList)
def getLineCmopenent():
    global myImages
    global visited
    res=[]
    
    for i in range(len(myImages)):
        
        if not visited[i]:
            LineComponentList=[]
            dfsLeft(i,LineComponentList)
            dfsRight(i,LineComponentList)
            res.append(LineComponentList)            
    return res



def guessQuets(img,loaded_model):
    
     
    # evaluate loaded model on test data
    img=np.reshape(img, [1,28,28,1])
    img=img/255
    rs=loaded_model.predict(img)
    dic={0:'.',1:","}
    return dic[np.argmax(rs)]
def guessChar(img,loaded_model):
    
     
    # evaluate loaded model on test data
    img=np.reshape(img, [1,28,28,1])
    img=img/255
    rs=loaded_model.predict(img)
    dic={0:'0',1:"1",2:"2",3:"3",4:"4",5:'5',6:"6",7:"7",8:"8",9:"9",10:"A"
         ,11:'B',12:"C",13:"D",14:"E",15:"F",16:"G",17:"H",18:"I",19:"J"
         ,20:"K",21:"L",22:"M",23:"N",24:"O",25:"P",26:"Q",27:"R",28:"S",29:"T",30:"U",31:"V"
         ,32:"W",33:"X",34:"Y",35:"Z",
         
         36:"a"
         ,37:'b',38:"c",39:"d",40:"e",41:"f",42:"g",43:"h",44:"i",45:"j"
         ,46:"k",47:"l",48:"m",49:"n",50:"o",51:"p",52:"q",53:"r",54:"s",55:"t",56:"u",57:"v"
         ,58:"w",59:"x",60:"y",61:"z",
         }
    return dic[np.argmax(rs)]
def resize_image(image):
 
        # Get height and width for image
        height, width = image.shape
     
        if height >= width:
     
            # Calculate width with height 20
            width = 20 * width // height
     
            # Resize the image 20 * width
            new_image = cv2.resize(image, (width, 20))
     
            # Create the white space to set it in left and right in image
            width_image = np.ones((20, (28 - width) // 2)) * 255
     
            # Set the white space in left and right to the image to be width approximately 28
            new_image = np.concatenate((width_image, new_image, width_image), axis=1)
     
            # Resize the image to be width exactly 28
            new_image = cv2.resize(new_image, (28, 20))
     
            # Create the white space to set it in top and bottom in image
            height_image = np.ones((4, 28)) * 255
     
            # Set the white space in top and bottom to the image to be width exactly 28
            new_image = np.concatenate((height_image, new_image, height_image), axis=0)
        else:
            # Calculate height with width 20
            height = 20 * height // width
     
            # Resize the image height * 20
            new_image = cv2.resize(image, (20, height))
     
            # create the white space to set it in left and right in image
            height_image = np.ones(((28 - height) // 2, 20)) * 255
     
            # Set the white space in left and right to the image to be height approximately 28
            new_image = np.concatenate((height_image, new_image, height_image), axis=0)
     
            # Resize the image to be height exactly 28
            new_image = cv2.resize(new_image, (20, 28))
     
            # Create the white space to set it in top and bottom in image
            width_image = np.ones((28, 4)) * 255
     
            # Set the white space in top and bottom to the image to be width exactly 28
            new_image = np.concatenate((width_image, new_image, width_image), axis=1)
     
        # Return the new image
        return new_image
def intersection(lst1, lst2): 
    lst1=lst1.tolist()
    lst2=lst2.tolist()
    return [item for item in lst1 if item in lst2] 
def inside(contour,contours):
    x,y,w,h = cv2.boundingRect(contour)
    midx=((x+w)+x)/2
    midy=(y+h)+(h)+1
    for i in range(len(contours)):
      xi,yi,wi,hi = cv2.boundingRect(contours[i])
      if (xi<midx and midx<xi+wi and   yi<midy and midy<yi+hi   ):
          return (True,i )
    return (False,False)           
        
def isContour1InsideContour2(contour1,contour2):
    x1,y1,w1,h1 = cv2.boundingRect(contour1)
    x2,y2,w2,h2 = cv2.boundingRect(contour2)
    if (x1>=x2 and x1<=x2+w2 and y1>=y2 and y1<=y2+h2) and (x1+w1<=x2+w2 and y1+h1>=y2 and y1+h1<=y2+h2):
        return True
    else:
        return False
def heightAvg(mycontours):
    sum=0
    for h,tcnt in enumerate(mycontours):
        x,y,w,h = cv2.boundingRect(tcnt)
        sum=sum+h
    if (len(mycontours))==0:
        return 0
    else:
        return sum/len(mycontours)
    
#************************
import tensorflow as tf
gpu_options = tf.GPUOptions(allow_growth=True)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
tf.compat.v1.keras.backend.set_session( sess)


graph =tf.compat.v1.get_default_graph()

#loadModel
yaml_file = open('/home/ahmed_m_khedr97/blinds/newmodel.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
# load weights into new model
loaded_model.load_weights("/home/ahmed_m_khedr97/blinds/newmodel.h5")
print("Loaded model from disk")
#******************************

#*************load Quets model
quets_yaml_file = open('/home/ahmed_m_khedr97/blinds/quets.yaml', 'r')
quets_loaded_model_yaml = quets_yaml_file.read()
quets_yaml_file.close()
quets_loaded_model = model_from_yaml(quets_loaded_model_yaml)
# load weights into new model
quets_loaded_model.load_weights("/home/ahmed_m_khedr97/blinds/quets.h5")
print("Loaded model from disk")












def ConvertImageToText(z):
    
    global graph
    global sess
    #z=cv2.medianBlur(z,5)
    zz=np.zeros((z.shape[0],z.shape[1]))
    #bin_img = cv2.adaptiveThreshold(z,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,81,17)
    bin_img=z
    bin_img1 = bin_img.copy()
    bin_img2 = bin_img.copy()
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    kernel1 = np.array([[1,0,1],[0,1,0],[1,0,1]], dtype = np.uint8)
    # final_thr = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
    # final_thr = cv2.dilate(bin_img,kernel1,iterations = 1)
    print("Noise Removal From Image.........")
    
    bin_img = cv2.adaptiveThreshold(bin_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,69,10)
    
    
    final_thr = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)
    _,contours, hierarchy = cv2.findContours(final_thr,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    
    
    for i in range(len(contours)):
        x,y,w,h = cv2.boundingRect(contours[i])
        if w>0.1*z.shape[1]:
           final_thr[y:y+h,x:x+w]=0 
    kernel = np.ones((2,60),np.uint8)
    copyOf_final_thr=final_thr.copy()
    
    new_final_thr = 255- cv2.dilate(final_thr,kernel,iterations = 1)
    
    final_thr=new_final_thr
    final_thr=255-final_thr
    
    area=0    
    MyLineAxess=[]
    lines=[]
    
    MyLineAxess.sort(key=lambda tup: tup[1])
    _x,CharContours, Charhierarchy = cv2.findContours(copyOf_final_thr,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    
    
    
    
    
    
    
    
    
    myContour=CharContours.copy()
    isQuates=[False for i in CharContours ]
    heightav=heightAvg(CharContours)
    for i in range(len(CharContours)):
          x,y,w,h = cv2.boundingRect(CharContours[i])
          area = cv2.contourArea(CharContours[i])
          if (h<(heightav*3/4)):
                  if inside(CharContours[i],CharContours)[0]:
                      cont2Index=inside(CharContours[i],CharContours)[1]
                      xi,yi,wi,hi = cv2.boundingRect(CharContours[cont2Index ])
                      concat=np.concatenate((CharContours[i],CharContours[cont2Index]), axis=0)
                      myContour[i]=[]
                      
                      myContour[ inside(CharContours[i],CharContours)[1]]=[]
                      myContour.append(concat)
                      isQuates.append(False)
                      
                      #cv2.rectangle(copyOf_final_thr,(xi,y),(xi+wi,yi+hi),(255,255,255),1)
                  else:
                      
                     #copyOf_final_thr[y:y+h,x:x+w]=0
                     #final_thr[y:y+h,x:x+w]=0
                     isQuates[i]=True
                     #myContour[i]=[]
    
    
    
    _,contours, hierarchy = cv2.findContours(final_thr,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    
    
    for i in range(len(contours)):
          x,y,w,h = cv2.boundingRect(contours[i])
          area = area+cv2.contourArea(contours[i])
          #cv2.rectangle(final_thr,(x,y),(x+w,y+h),(255,255,255),1)
    if len(contours)==0:
        area=0
    else:
        area=area/len(contours)
    lineCondtour=[]
    for i in range(len(contours)):
          x,y,w,h = cv2.boundingRect(contours[i])
          if (w*h)>(area/2):
              MyLineAxess.append((contours[i], y) )
              lines.append([])
              #cv2.rectangle(final_thr,(x,y),(x+w,y+h),(255,255,255),3)
          else:
              final_thr[y:y+h,x:x+w]=0 
    c=0
    
    MyLineAxess.sort(key=lambda tup: tup[1])
    
    
    
    
    
    for i in range(len(myContour)):
        if not len(myContour[i])==0:
            x,y,w,h = cv2.boundingRect(myContour[i])
            for j in range(len(MyLineAxess)):
                if cv2.pointPolygonTest(MyLineAxess[j][0],((x+w+x)/2,(y+y+h)/2),True)>=0.0 :#and  cv2.pointPolygonTest(MyLineAxess[j][0],(x+w,y+h),True)>=0.0:
                   
                    lines[j].append((myContour[i],x,isQuates[i]))
    s=""
    count=0
    lineSpace=[]
    cv2.imwrite("zxc.png",255-final_thr)
    for i in lines:
        i.sort(key=lambda tup: tup[1])
        lineSpace.append([])
        av=0
        for k in range(len(i)) :
             if not k==0:
                
                x,y,w,h = cv2.boundingRect(i[k][0])
                x0,y0,w0,h0 = cv2.boundingRect(i[k-1][0])
            
                
            
                lineSpace[count].append(x-(x0+w0))
                av=av+x-(x0+w0)
        lineSpace[count].append(av/len(i)*3)
        lineSpace[count].append(av/len(i)*3)
        lineSpace[count]=np.array(lineSpace[count])
       # lineSpace[count]=np.sort(lineSpace[count])
        
        kmeans = KMeans(n_clusters=2, random_state=0).fit(lineSpace[count].reshape(-1,1))
        lineSpace[count]=kmeans.labels_
        charSpace=0
        if np.count_nonzero(lineSpace[count]==1)>np.count_nonzero(lineSpace[count]==0):
            charSpace=1
        else:
            charSpace=0
        countt=0
        for j in range(len(i)):
          with graph.as_default():
                tf.compat.v1.keras.backend.set_session( sess)
                x,y,w,h = cv2.boundingRect(i[j][0])
                isqts=i[j][2]
                myImg=255-copyOf_final_thr[y:y+h,x:x+w]
                myImg=resize_image(myImg)
                if not(j==0 ) :
                    x0,y0,w0,h0 = cv2.boundingRect(i[j-1][0])
                    if isqts:
                        if (y-y0)**2>((y-(y0+w0))**2):
                            s=s+guessQuets(myImg,quets_loaded_model)
                            #if  lineSpace[count][j-1]==charSpace:
                             #   print((lineSpace[count][j],lineSpace[count][j-1]))
                                
                              #  s=s+","
                            #else:
                            #    s=s+" "+","
                        else:
                            if  lineSpace[count][j-1]==charSpace:
                                
                                s=s+"'"
                            else:
                                s=s+" "+"'"
                    else:
                            if  lineSpace[count][j-1]==charSpace:
                                
                                s=s+guessChar(myImg,loaded_model)
                            else:
                                s=s+" "+guessChar(myImg,loaded_model)
                            
                else:
                    s=s+guessChar(myImg,loaded_model)
                #cv2.imwrite("w"+str(countt)+".png",myImg)
                cv2.rectangle(copyOf_final_thr,(x,y),(x+w,y+h),(255,255,255),1)
                countt=countt+1
        
        
        count=count+1
        s=s+"\n"
    s=s.replace('0', 'o')
    s=s.replace('9', 'g')
    s=s.lower()
    return s


#************************************************************
#**********************
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOADED_IMAGES_DEST'] = 'images'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

@app.route('/', methods=['GET'])
def index():
    img = request.files['image']
    img.filename = 'x.png'
    filename = images.save(img)
    path = "/home/ahmed_m_khedr97/blinds/images/" + filename

    image = cv2.imread(path, 0);
    text = ConvertImageToText(image)
    os.remove("/home/ahmed_m_khedr97/blinds/images/" + img.filename)
    response = make_response(text)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)




#************************************************************
#**********************
