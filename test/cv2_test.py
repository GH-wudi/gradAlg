import cv2
import numpy as np
image2 = cv2.imread("C:\\Users\\Emc2\\Desktop\\test2.png")
print(image2.shape)
image = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
# BGR = numpy.array([0,0,0])
# upper = BGR + 20
# lower = BGR - 20
# mask = cv2.inRange(image,lower,upper)
# cv2.imshow("Mask",mask)
# cv2.waitKey()

(contours,hicrarchy) = cv2.findContours(image.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
new_label = np.zeros(image.shape,np.uint8)
# contours.sort(key=len, reverse=False)
contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)
print(contours[0].shape)
print(contours[0])
print("number of contours:%d" %(len(contours))) 
# for i in range(100):
temp = np.zeros(image.shape,np.uint8)
#     temp[image == i] = i
#     for num,values in enumerate(contours):
#         if cv2.contourArea(values) < 500:
#             cv2.drawContours(temp,contours,num,0,thickness=-1)
#     new_label += temp
# img1 = new_label
# for i in range(5):
#     temp += cv2.drawContours(temp,[contours[i]],0,255,cv2.FILLED)
temp = [ cv2.drawContours(temp,[contours[i]],0,255,cv2.FILLED)  for i in range(5)]    

# mask = cv2.fillPoly(image,)
cv2.imwrite('C:\\Users\\Emc2\\Desktop\\test8.png',temp)

# alllakesImage = image.copy()
# cv2.drawContours(image2.copy(),contours,-1,(0,0,255),1)
# cv2.waitKey()
# cv2.imshow("Image of All Lake",alllakesImage)
# cv2.waitKey()
# theLargestLake = image.copy()
# contours.sort(key=len,reverse=True)
# (contours,hicrarchy) = cv2.findContours(theLargestLake,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# kernel = np.ones((5, 5), np.uint8)
# theLargestLake = cv2.morphologyEx(theLargestLake, cv2.MORPH_OPEN, kernel)
# (contours,hicrarchy) = cv2.findContours(theLargestLake,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# print("number of contours:%d" %(len(contours)))
# cv2.drawContours(theLargestLake,[contours[0]],-1,(0,0,255),2)
# cv2.imshow("Image of the Largest Lake",theLargestLake)
# def cnt_area(cnt):
#   area = cv2.contourArea(cnt)
#   return area
# img = [contours[0].astype(np.uint8)]
# img = np.ascontiguousarray(img)
# contours.sort(key = cnt_area, reverse=False)
for i in range(0, len(contours)):
  (x, y, w, h) = cv2.boundingRect(contours[i])
  cv2.rectangle(image,(x,y),(x+w, y+h),(255,0,0),2, cv2.LINE_AA)
#   cv2.putText(image,"No.%d"%(i+1),(x,y-5),font,0.8,(255,0,0),2)

# cv2.imshow("contours", image)
# cv2.imwrite("result1.jpg",img)
# cv2.waitKey()
# cv2.imwrite('C:\\Users\\Emc2\\Desktop\\test6.png', mask)
# cv2.waitKey()
