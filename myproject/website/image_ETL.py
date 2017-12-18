# image_ETL_v2.0
import os
import dlib
import glob
import time
import shutil
import numpy as np
from skimage import io
from datetime import datetime
from matplotlib import image
from PIL import Image, ImageDraw
from sklearn import mixture
from sklearn.externals import joblib

def dlib_face_cluster(pic_path,tmp_path,files_path): 
    global detector,sp,facerec
    predictor_path = files_path + '/shape_predictor_5_face_landmarks.dat'
    face_rec_model_path = files_path + '/dlib_face_recognition_resnet_model_v1.dat'

    faces_folder_path = pic_path
    output_folder_path = tmp_path

    # Load all the models we need: a detector to find the faces, a shape predictor
    # to find face landmarks so we can precisely localize the face, and finally the
    # face recognition model.
    if not 'detector' in globals():
        detector = dlib.get_frontal_face_detector()
    if not 'sp' in globals():
        sp = dlib.shape_predictor(predictor_path)
    if not 'facerec' in globals():    
        facerec = dlib.face_recognition_model_v1(face_rec_model_path)

    raw_image_list = glob.glob(os.path.join(faces_folder_path, "*.jpg"))
    raw_image_list.append(raw_image_list[0])
    counter = 1
    batch_index = 1
    # Now find all the faces and compute 128D face descriptors for each face.
    while(True):
        descriptors = []
        images = []
        while(True):
        #     print("Processing file: {}".format(f))
            try:
                f = raw_image_list.pop(0)
                counter += 1              
            except:
                break
            try:
                img = io.imread(f)
            except:
                print('[Debug] : something wrong at io.imread, {0}'.format(f))
                continue

            # Ask the detector to find the bounding boxes of each face. The 1 in the
            # second argument indicates that we should upsample the image 1 time. This
            # will make everything bigger and allow us to detect more faces.
            try:
                dets = detector(img, 1)
            except:
                print('[Debug] : something wrong at detector, {0}'.format(f))
                continue
        #     print("Number of faces detected: {}".format(len(dets)))

            # Now process each face we found.
            for k, d in enumerate(dets):
                # Get the landmarks/parts for the face in box d.
                shape = sp(img, d)

                # Compute the 128D vector that describes the face in img identified by
                # shape.
                try:
                    face_descriptor = facerec.compute_face_descriptor(img, shape)
                    descriptors.append(face_descriptor)
                    images.append((img, shape))
                except:
                    print('[Debug] : something wrong at facerec.compute_face_descriptor, {0}'.format(f))
                    continue
        
        # Now let's cluster the faces.  
        labels = dlib.chinese_whispers_clustering(descriptors, 0.5)
        num_classes = len(set(labels))
        # print("Number of clusters: {}".format(num_classes))
        # Find biggest class
        biggest_class = None
        biggest_class_length = 0
        for i in range(0, num_classes):
            class_length = len([label for label in labels if label == i])
            if class_length > biggest_class_length:
                biggest_class_length = class_length
                biggest_class = i

        # print("Biggest cluster id number: {}".format(biggest_class))
        # print("Number of faces in biggest cluster: {}".format(biggest_class_length))

        # Find the indices for the biggest class
        indices = []
        for i, label in enumerate(labels):
            if label == biggest_class:
                indices.append(i)

        # print("Indices of images in the biggest cluster: {}".format(str(indices)))

        # Ensure output directory exists
        if not os.path.isdir(output_folder_path):
            os.makedirs(output_folder_path)
        
        # Save the extracted faces
        # print("Saving faces in largest cluster to output folder...")
        for i, index in enumerate(indices):
            img, shape = images[index]
            file_path = os.path.join(output_folder_path,'batch{0}_{1}'.format(batch_index,i))
            dlib.save_face_chip(img, shape, file_path)
            break
        batch_index += 1

        if len(raw_image_list) == 0:
            break   
			
			
def dlib_face_point(pic_path,tmp_path,files_path):
    global predictor,black_pic_io,black_pic_im
    # 原始圖檔來源
    faces_path = glob.glob(pic_path + '/*.jpg')
    # 圖片輸出目的地
    output_path = tmp_path + '/'

    # 初始化所需要的物件
    predictor_path = files_path + "/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    if not 'predictor' in globals():
        predictor = dlib.shape_predictor(predictor_path)

    # 載入全黑圖片作為底圖，後續標記臉部特徵時使用
    if not 'black_pic_io' in globals():
        black_pic_io = io.imread(files_path + '/black.jpg')
    if not 'black_pic_im' in globals():    
        black_pic_im = Image.open(files_path + '/black.jpg')

    index = 0

    while(True):
        try:
            # 每次取出一張圖片的路徑，list為空時結束迴圈
            raw_img = io.imread(faces_path.pop(0))
        except:
            break

        img = raw_img.copy()

        # 初始化臉部各特徵的 List，用於紀錄相關座標點
        face_list = []
        lefteye_list = []
        righteye_list = []
        mouth_inner_edge_list = []
        mouth_outer_edge_list = []

        # 將所有物件以全黑底圖做初始化
        face_filled_im = black_pic_im.copy()
        eyes_filled_im = black_pic_im.copy()
        mouth_filled_im = black_pic_im.copy()

        # 將所有物件以全黑底圖做初始化
        face_point_io = black_pic_io.copy()
        lefteye_point_io = black_pic_io.copy()
        righteye_point_io = black_pic_io.copy()
        nose_point_io = black_pic_io.copy()
        mouth_point_io = black_pic_io.copy()
        eyebrow_point_io = black_pic_io.copy()

        dets = detector(img, 1)
        for i in range(len(dets)):
            # 將人臉全部的特徵點存放於矩陣中
            facepoint = np.array([[p.x, p.y] for p in predictor(img, dets[i]).parts()])

        for j in range(68):
            try:
                # 將特徵點標記於原始圖上
                img[facepoint[j,1],facepoint[j,0],:] = [255,0,0]
            except:
                print('[Debug]something wrong at {}'.format(index))
                continue

            # 分別記錄眼睛、嘴巴、臉的特徵點於矩陣中
            if j <= 16:
                face_point_io[facepoint[j,1],facepoint[j,0],:] = [255,255,255]
                face_list.append(tuple(facepoint[j]))
            elif j >= 17 and j <= 26:
                eyebrow_point_io[facepoint[j,1],facepoint[j,0],:] = [255,255,255]
            elif j >= 27 and j <= 35:
                nose_point_io[facepoint[j,1],facepoint[j,0],:] = [255,255,255]
            elif j >= 36 and j <= 41:
                lefteye_point_io[facepoint[j,1],facepoint[j,0],:] = [255,255,255]
                lefteye_list.append(tuple(facepoint[j])) 
            elif j >= 42 and j <= 47:
                righteye_point_io[facepoint[j,1],facepoint[j,0],:] = [255,255,255]
                righteye_list.append(tuple(facepoint[j])) 
            elif j >= 48:
                mouth_point_io[facepoint[j,1],facepoint[j,0],:] = [255,255,255]
                if j <= 59:
                    mouth_outer_edge_list.append(tuple(facepoint[j]))
                else:
                    mouth_inner_edge_list.append(tuple(facepoint[j]))  

        # 將臉、眼睛、嘴巴的輪廓實心填滿，存入物件中
        face_draw = ImageDraw.Draw(face_filled_im)
        face_draw.polygon(face_list,fill = (255, 255, 255))

        eyes_draw = ImageDraw.Draw(eyes_filled_im)
        eyes_draw.polygon(lefteye_list,fill = (255, 255, 255))
        eyes_draw.polygon(righteye_list,fill = (255, 255, 255))

        mouth_draw = ImageDraw.Draw(mouth_filled_im)
        mouth_draw.polygon(mouth_outer_edge_list,fill = (255, 255, 255))
        mouth_draw.polygon(mouth_inner_edge_list,fill = (0, 0, 0))

        # 截取出嘴巴的圖片
        mouth_point_r = mouth_point_io[:,:,0]
        mouth = np.array([np.where(mouth_point_r!=0)[0],np.where(mouth_point_r!=0)[1]])
        mouth = mouth.transpose()
        r_max = mouth[:,0].max()
        r_min = mouth[:,0].min()
        c_max = mouth[:,1].max()
        c_min = mouth[:,1].min()
        img_mouth = raw_img[r_min:r_max+1,c_min:c_max+1]

        # 物件使用完後刪除
        del face_draw
        del eyes_draw
        del mouth_draw
        
        # Ensure output directory exists
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
            
        # 將各特徵點分別輸出圖片
        dest = output_path + '{0}'.format(index)
        os.mkdir(dest)
        image.imsave(dest + '/raw_image.jpg', raw_img)
        image.imsave(dest + '/point_image.jpg', img)
        image.imsave(dest + '/point_face.jpg', face_point_io)
        image.imsave(dest + '/point_lefteye.jpg', lefteye_point_io)
        image.imsave(dest + '/point_righteye.jpg', righteye_point_io)
        image.imsave(dest + '/point_nose.jpg', nose_point_io)
        image.imsave(dest + '/point_mouth.jpg', mouth_point_io)
        image.imsave(dest + '/point_eyebrow.jpg', eyebrow_point_io)

        # 將填滿的實心物件輸出為檔案
        face_filled_im.save(dest + '/filled_face.jpg')
        eyes_filled_im.save(dest + '/filled_eyes.jpg')
        mouth_filled_im.save(dest + '/filled_mouth.jpg')

        # 將嘴巴圖片輸出為檔案
        image.imsave(dest + '/image_mouth.jpg',img_mouth)
        mouth_filled_im.crop((c_min-5, r_min-5, c_min+55, r_min+25)).save(dest + '/filled_mouth_cu.jpg')
        mouth_filled_im.crop((c_min-5, r_min-5, c_max+5, r_max+5)).resize((60,30), Image.ANTIALIAS)\
                                                                  .save(dest + '/filled_mouth_cu_resize.jpg')        
        mouth_filled_im.crop(((c_min+c_max)/2-30, 
                              (r_min+r_max)/2-15, 
                              (c_min+c_max)/2+30, 
                              (r_min+r_max)/2+15))\
                              .save(dest + '/filled_mouth_cu_center.jpg')
        index += 1 
		

def eye_face_rate_calc(image_path):
    # 圖片來源路徑
    pic_path = glob.glob(image_path + "/*")

    # 初始化 list
    faces_area = []
    eyes_area = []
    lefteye_area = []
    righteye_area = []

    for pic in pic_path:
        # 載入臉部圖片
        face_pic_io = io.imread(pic + '/filled_face.jpg')    
        # 計算臉部 pixel數，計算完畢加入 list中
        face_pixel = 0    
        for pixel in face_pic_io.flatten():
            if pixel >= 200:
                face_pixel += 1
        faces_area.append(face_pixel)

        # 載入眼睛圖片
        eyes_pic_io = io.imread(pic + '/filled_eyes.jpg')
        # 將圖片切開，區分出左眼與右眼
        lefteye_pic = eyes_pic_io[:,:int(len(eyes_pic_io[:,0,0])/2),:]
        righteye_pic = eyes_pic_io[:,int(len(eyes_pic_io[:,0,0])/2):,:]

        # 計算雙眼 pixel數，計算完畢加入 list中
        eyes_pixel = 0
        for pixel in eyes_pic_io.flatten():
            if pixel >= 200:
                eyes_pixel += 1
        eyes_area.append(eyes_pixel)

        # 計算左眼 pixel數，計算完畢加入 list中
        lefteye_pixel = 0
        for pixel in lefteye_pic.flatten():
            if pixel >= 200:
                lefteye_pixel += 1
        lefteye_area.append(lefteye_pixel)

        # 計算右眼 pixel數，計算完畢加入 list中
        righteye_pixel = 0
        for pixel in righteye_pic.flatten():
            if pixel >= 200:
                righteye_pixel += 1
        righteye_area.append(righteye_pixel)

    # 初始化 list    
    eye_face_rate = []
    two_eyes_rate = []

    for i in range(len(faces_area)) :
        try:
            # 計算雙眼與臉面積比例
            eye_face_rate.append(round((eyes_area[i] / faces_area[i]) * 100, 3))
        except Exception as err:
            print(err)
            eye_face_rate.append('')
        try:
            # 計算左眼與右眼面積比例
            two_eyes_rate.append(round(lefteye_area[i] / righteye_area[i], 3))
        except Exception as err:
            print(err)
            two_eyes_rate.append('')
    
    return eye_face_rate,two_eyes_rate
	
	
	
def fat_face_detector(image_path):
    # 圖片來源路徑
    pic_path = glob.glob(image_path + "/*")

    # 初始化 list
    faces_width = []
    faces_tall = []
    faces_left_dist = []
    faces_right_dist = []
    error_log = []

    err_counter = 0
    for pic in pic_path:
        # 載入臉部圖片
        face_pic_io = io.imread(pic + '/point_face.jpg')
        # 透過舉陣運算得出描繪臉型輪廓的點
        face_point_r = face_pic_io[:,:,0]
        face = np.array([np.where(face_point_r!=0)[0],
                         np.where(face_point_r!=0)[1]]).transpose()
        try :
            # 取出左臉頰、右臉頰、下巴各一個點，用以運算臉寬比例與左右臉對稱比例
            left_point = face[np.where(face[:,1] == sorted(face[:,1])[5])[0],:]
            bottom_point = face[np.where(face[:,1] == sorted(face[:,1])[8])[0],:]
            right_point = face[np.where(face[:,1] == sorted(face[:,1])[11])[0],:]
        except Exception as err:
            # print('[Degug]{} -- {},total errors : {}'.format(err,pic,err_counter))
            error_log.append(pic)
            err_counter += 1
            continue

        # 紀錄臉寬與高的數值
        faces_width.append(right_point[0,1] - left_point[0,1])
        faces_tall.append(bottom_point[0,0] - ((left_point[0,0] + right_point[0,0])/2))
        # 紀錄左臉頰與右臉頰到下巴垂線的水平距離
        faces_left_dist.append(abs(left_point[0,1] - bottom_point[0,1]))
        faces_right_dist.append(abs(right_point[0,1] - bottom_point[0,1]))

    #計算比例
    fat_faces_rate = []
    symm_faces_rate = []
    for i in range(len(faces_width)):
        fat_faces_rate.append(round(faces_width[i] / faces_tall[i], 3))
        symm_faces_rate.append(round(faces_left_dist[i] / faces_right_dist[i], 3))

    for error in error_log :
        pic_path.remove(error)
        
    return fat_faces_rate,symm_faces_rate
	

def mouth_cluster(image_path,files_path):
    global gmm
    # GMM分群
    pic_path = glob.glob(image_path + '/*')
   
    opic = []
    pic = []
    for file in pic_path:
        image = io.imread(file + '/filled_mouth_cu_center.jpg')
        opic.append(image)
        image = image[:,:,0]
        images = image.reshape((image.shape[0]*image.shape[1]))
        pic.append(images)
        
    if not 'gmm' in globals():
        gmm = joblib.load(files_path + '/mouth_10.pkl')

    return gmm.predict(pic)[0]
	
	
def image_ETL(pic_path,tmp_path,files_path):
    if not os.path.isdir(tmp_path):
        os.makedirs(tmp_path)   
    dlib_face_cluster(pic_path,tmp_path + '/1',files_path)
    dlib_face_point(tmp_path + '/1',tmp_path + '/2',files_path) 
    res1 = eye_face_rate_calc(tmp_path + '/2')  
    res2 = fat_face_detector(tmp_path + '/2') 
    res3 = mouth_cluster(tmp_path + '/2',files_path)
    
    shutil.rmtree(tmp_path)
    os.remove(glob.glob(pic_path + '/*')[0])
    return res1,res2,res3
	