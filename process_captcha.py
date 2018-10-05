import cv2
import numpy as np
import os
import shutil
from matplotlib import pyplot as plt

pics_src = '/home/mahdi/Desktop/pics/'
parted_src = '/home/mahdi/Desktop/parted/'
if os.path.isdir(parted_src):
    shutil.rmtree(parted_src)
os.makedirs(parted_src)
num, dataset, x_train, y_train, x_test, y_test = 0, [], [], [], [], []
# letters = []
# falses = []

# from keras.models import model_from_json
#
# # load json and create model
# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# model = model_from_json(loaded_model_json)
# # load weights into new model
# model.load_weights("model.h5")
# print("Loaded model from disk")

pics = os.listdir(pics_src)
# print(pics)
for img_src in pics:
    name = img_src.split('.')[0]
    # if not os.path.isdir(parted_src + name):
    #     os.makedirs(parted_src + name)
    img = cv2.imread(pics_src + img_src)
    img = img[5:35, 5:145]

    n_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    color = ('b', 'g', 'r')
    selected_color_max, max_hist = 'n', cv2.calcHist([n_img], [0], None, [256], [0, 256]).max()
    # max_hist = 0
    min_hist = 10000
    selected_color_min = selected_color_max
    # print(str('n') + ' ' + str(max_hist) + ' ' + name)
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        if histr.max() > max_hist:
            max_hist = histr.max()
            selected_color_max = col
        if histr.max() < min_hist:
            min_hist = histr.max()
            selected_color_min = col
        # if name == 'RLXEP':
        #     print(str(col) + ' ' + str(max_hist) + ' ' + name)
        #     plt.plot(histr, color=col)
        #     plt.xlim([0, 256])
        #     plt.show()
    if max_hist < 1000:
        selected_color = selected_color_min
    else:
        selected_color = selected_color_max

    # if name == 'RLXEP':
    #     # cv2.imwrite('bw_image.png', img)
    #     selected_color = 'n'

    if selected_color == 'r':
        img[:, :, 1] = 0
        img[:, :, 2] = 0
    elif selected_color == 'g':
        img[:, :, 0] = 0
        img[:, :, 2] = 0
    elif selected_color == 'b':
        img[:, :, 1] = 0
        img[:, :, 0] = 0

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    print(name)
    print(hist.max())
    # plt.plot(hist)
    # plt.xlim([0, 256])
    # plt.show()

    if hist.max() > 1100:
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    else:
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # find the contours (continuous blobs of pixels) the image
    # contours = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
    #
    # letter_image_regions = []
    # 	# Sort the detected letter images based on the x coordinate to make sure
    # 	# we are processing them from left-to-right so we match the right image
    # 	# with the right letter
    # letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])
    # image, contours, hierarchy = cDv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # for contour in range(0,len(contours)):
    # 	(x, y, w, h) = cv2.boundingRect(contours[contour])
    # 	image = cv2.rectangle(img,(x,y),(x+w,y+h),(150,150,150),2)
    # 	letter_image_regions.append((x, y, w, h))
    # 	cv2.imshow('image'+str(contour),image)
    # 	cv2.waitKey(0)
    # 	cv2.destroyAllWindows()

    # for i in range(0, 5):
    #     if len(name) > 0:
    #         cv2.imwrite(parted_src + name + '/' + name[i] + '.png', img[:, max(i * 28 - 2, 1):min((i + 1) * 28 + 2, 139)])

    # x_dataset.append(img)
    # y_dataset.append(name[0:5])

    if img.shape == (30, 140) and len(name) >= 5:
        for j in range(0, 5):
            img1 = np.zeros((30, 28, 1))
            img1[:, :, 0] = img[:, j * 28: (j + 1) * 28]
            if num > len(pics):
                x_train.append(img1)
                y_train.append(ord(name[0:5][j]) - 97)
            else:
                x_test.append(img1)
                y_test.append(ord(name[0:5][j]) - 97)
            # letters.append(name[0:5][j])
            # if (name[0:5][j] == '￩'):
            #     falses.append(name)
            num += 1
        cv2.imwrite(parted_src + name + '.png', img)

# print(len(set(letters)))
# print((set(letters)))
# print(falses)
print(num)


x_train = np.array(x_train)
x_test = np.array(x_test)

y_train = np.array(y_train)
y_test = np.array(y_test)

dataset = (x_train, y_train), (x_test, y_test)

# prediction = list(model.predict(np.array([x_test[1], x_test[2]])))
# for predict in prediction:
#     print(chr(list(predict).index(float(1))+97))
#
# cv2.imshow('image', x_test[1])
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imshow('image', x_test[2])
# cv2.waitKey(0)
# cv2.destroyAllWindows()

np.array(dataset).dump(open('captcha.npy', 'wb'))
exit
# np.save('captcha', np.array(dataset))