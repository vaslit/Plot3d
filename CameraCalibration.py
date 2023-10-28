import numpy as np
import cv2 as cv2
import glob
from Calculation import *
import math

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2) * 21.95
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

n = 1
ret, frame = cam.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Display the resulting frame
cv2.imshow('frame', frame)
while(True):
    # Capture the video frame
    # by frame
    ret, frame = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        # # Find the chess board corners
        # ret, corners = cv2.findChessboardCorners(frame, (7,7), None)
        #     # If found, add object points, image points (after refining them)
        # if ret == True:
        #     objpoints.append(objp)
        # corners2 = cv2.cornerSubPix(frame,corners, (11,11), (-1,-1), criteria)
        # imgpoints.append(corners2)
        cv2.imwrite(f".\images\cb_{n}.png", frame)
        # # Draw and display the corners
        # cv2.drawChessboardCorners(frame, (7,7), corners2, ret)
        # cv2.imshow('frame', frame)
        cv2.waitKey(0)
        n = n + 1
cv2.destroyAllWindows()

# images = glob.glob('.\images\cb_*.png')
# shape = None
# for fname in images:
#     img = cv2.imread(fname)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     shape = gray.shape[::-1]
#     # Find the chess board corners
#     ret, corners = cv2.findChessboardCorners(gray, (7,7), None)
#     # If found, add object points, image points (after refining them)
#     if ret == True:
#         objpoints.append(objp)
#     corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
#     imgpoints.append(corners2)
#     # Draw and display the corners
#     cv2.drawChessboardCorners(img, (7,7), corners2, ret)
#     cv2.imshow('img', img)
#     cv2.waitKey(10)
h, w = 720,1280
# ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,(w, h), None, None)
# `np.savez("cam.z", mtx, dist)`
f = np.load("cam.z.npz")
mtx = f['arr_0']
dist = f['arr_1']

#mtx = np.array([[1.43598787e+03, 0.00000000e+00, 6.31426449e+02], [0.00000000e+00, 1.43848294e+03, 3.31539804e+02], [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
#dist = np.array([[ 1.61790013e-01, -1.40470691e-01, -1.00522427e-03, -3.18221410e-03,  -1.37656187e+00]])
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
x, y, w, h = roi
mode = False
right_img = left_img = None
numDisparities=1
blockSize=15
show_d = False
d_img = None
points = np.array([[0.0,0.0,10.0]])
rvec = np.array([[0,0,0],], float)
tvec = np.array([[0,0,0],], float)
i_points = cv2.projectPoints(points,rvec,tvec,mtx,dist)
while(True):
    # Capture the video frame by frame 
    ret, frame = cam.read() 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    # undistort        
    remap_frame = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
    #remap_frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    #remap_frame = remap_frame[y:y+h, x:x+w]
    if mode:
        frame = remap_frame[y:y + h, x:x + w].copy()
        #frame = remap_frame.copy()
        cv2.putText(frame, f'mode: on',(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1, cv2.LINE_AA)
    else:
        #frame = frame[y:y + h, x:x + w].copy()
        cv2.putText(frame, f'mode: off', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1, cv2.LINE_AA)
    # if d_img is not None and mode:
    #     frame = depthTest(left_img,right_img,numDisparities*16,blockSize)
    # else:
    #     frame = remap_frame
    # cv2.putText(frame, f'mode: off',(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1, cv2.LINE_AA)
    # cv2.putText(frame, f'numDisparities: {numDisparities}',(50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1, cv2.LINE_AA)
    # cv2.putText(frame, f'blockSize: {blockSize}',(50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1, cv2.LINE_AA)
    cv2.imshow('frame', frame) 
    # the 'q' button is set as the quitting button you may use any desired button of your choice 
    key = cv2.waitKey(1)
    print(f'key: {key}')
    if key == ord('`'): 
        break    
    elif key == ord('m'): 
        mode = not mode
    elif key == ord('l'): 
        d_img = None
        left_img = remap_frame.copy()
        cv2.imwrite(".\\images\\left.png",left_img)
    elif key == ord('r'): 
        d_img = None
        right_img = remap_frame.copy()
        cv2.imwrite(".\\images\\right.png",right_img)
    elif key == ord('d'): 
        d_img = depthTest(left_img,right_img,numDisparities*16,blockSize)   
    elif key == ord('x'): 
        d_img = None
    elif key == ord('a'): 
        numDisparities=numDisparities-1
    elif key == ord('s'): 
        numDisparities=numDisparities+1
    elif key == ord('q'): 
        blockSize=blockSize-1        
    elif key == ord('w'): 
        blockSize=blockSize+1
    elif key == ord('p'):
        cv2.imwrite(".\\images\\frame.png",frame)
cv2.destroyAllWindows()