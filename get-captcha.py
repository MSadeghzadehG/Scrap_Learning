import requests
import os
import cv2
import shutil


def main():

    mainUrl = "https://portal.aut.ac.ir/aportal/index.jsp"
    img_url = 'https://portal.aut.ac.ir/aportal/PassImageServlet'
    pics_src = '/home/mahdi/Desktop/pics/'
    if not os.path.isdir(pics_src):
        os.makedirs(pics_src)
    num = len(os.listdir(pics_src))
    flag = True

    while flag:
        print(str(num) + ' file saved')
        request1 = requests.get(mainUrl, allow_redirects=True)
        cookies = request1.cookies
        request = requests.get(img_url, allow_redirects=True, stream=True, cookies=cookies)
        print(request.status_code)
        with open('/home/mahdi/Desktop/bw_image', 'wb') as out_file:
            shutil.copyfileobj(request.raw, out_file)
        img = cv2.imread('/home/mahdi/Desktop/bw_image')

        print('write the captcha:')
        name = ''
        cv2.namedWindow("captcha")
        while True:
            cv2.imshow("captcha", img)
            # print(cv2.waitKey())
            k = (cv2.waitKey())
            # print(k)
            if k == 10:
                break
            elif k == 65288:
                name = name[0:len(name)-1]
            else:
                name += chr(k)
            print(name)
        # cv2.destroyAllWindows()

        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # name = input()

        if name == 'x':
            flag = False
            break

        cv2.imwrite(pics_src + name + '.jpeg', img)
        for i in range(1, 100):
            request = requests.get(img_url, allow_redirects=True, stream=True, cookies=cookies)
            with open('/home/mahdi/Desktop/bw_image', 'wb') as out_file:
                shutil.copyfileobj(request.raw, out_file)
            img = cv2.imread('/home/mahdi/Desktop/bw_image')
            cv2.imwrite(pics_src+name+str(i)+'.jpeg', img)

        num += 100


if __name__== "__main__":
    main()