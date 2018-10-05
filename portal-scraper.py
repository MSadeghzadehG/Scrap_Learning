import requests
import os
import cv2
from lxml import html
import json
from keras.models import model_from_json
import numpy as np
from time import sleep


main_url = 'https://portal.aut.ac.ir'
login_page = "https://portal.aut.ac.ir/aportal/"
login_captcha = 'https://portal.aut.ac.ir/aportal/PassImageServlet'
right_menu = 'https://portal.aut.ac.ir/aportal/regadm/style/menu/menu.student.jsp'

username = str('')
password = str('')
drop_wait = 1


menu_urls = []
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_mine_all')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_pre_register')
# menu_urls.append(
    # main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_math')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_physlab2')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_phys')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_physlab1')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_serv')
#menu_urls.append(
#    main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_english')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_history')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_andishe')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_persian')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_akhlagh')
menu_urls.append(main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_revel')
#menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_tafsir')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_phyedu1')
# menu_urls.append(
#     main_url + '/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_phyedu2')


def plans_output(all_courses, plans):
    with open('mycourses.html', 'w') as f:
        for plan in plans:
            f.write('<table>')
            for course in all_courses:
                for child in course.iter():
                    if child.tag == 'input':
                        if child.attrib['value'] in plan:
                            f.write(html.etree.tostring(course).decode('utf-8'))
            f.write('</table>')
            f.write('<hr>')


def courses_output(cookies, menu_urls):
    all_courses = []
    for tab in menu_urls:
        request = requests.get(tab, headers={'Cookie': cookies})
        all_courses.extend(find_elements_by_xpath(request.content.decode('utf-8'), '/html/body/form/table/tr[4]/td/table/tr'))
        f = open('menus/menu'+str(menu_urls.index(tab))+'.html', 'w')
        f.write(request.text)
        f.close()
    return all_courses


def find_elements_by_xpath(text, xpath):
    tree = html.fromstring(text)
    list = []
    for link in tree.xpath(xpath):
        list.append(link)
    return list


def filter_captcha(img):
    img = img[5:35, 5:145]
    n_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    color = ('b', 'g', 'r')
    selected_color_max, max_hist = 'n', cv2.calcHist([n_img], [0], None, [256], [0, 256]).max()
    min_hist = 10000
    selected_color_min = selected_color_max
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        if histr.max() > max_hist:
            max_hist = histr.max()
            selected_color_max = col
        if histr.max() < min_hist:
            min_hist = histr.max()
            selected_color_min = col
    if max_hist < 1000:
        selected_color = selected_color_min
    else:
        selected_color = selected_color_max
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

    if hist.max() > 1100:
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    else:
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return img


def get_course_filter_captcha(img):
    img = img[5:35,2:58]
    n_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    color = ('b', 'g', 'r')
    selected_color_max, max_hist = 'n', cv2.calcHist([n_img], [0], None, [256], [0, 256]).max()
    min_hist = 10000
    selected_color_min = selected_color_max
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        if histr.max() > max_hist:
            max_hist = histr.max()
            selected_color_max = col
        if histr.max() < min_hist:
            min_hist = histr.max()
            selected_color_min = col
    if max_hist < 1000:
        selected_color = selected_color_min
    else:
        selected_color = selected_color_max
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

    if hist.max() > 1100:
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    else:
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return img


def get_captcha(cookies):
    request = requests.get(login_captcha, headers={'Cookie': cookies}, stream=True)
    nparr = bytearray(b'')
    for chunk in request.iter_content(chunk_size=128):
        nparr.extend(chunk)
    nparr = np.fromstring(bytes(nparr), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # img = filter_captcha(img)
    return img


def get_course_captcha(model, cookies):
    num = 5
    captchas = []
    # print ('omad')
    for i in range(0, num):
        # sleep(1)
        captcha = ''
        img = get_captcha(cookies)
        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        img = get_course_filter_captcha(img)
        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        letters = []
        for j in range(0, 2):
            img1 = np.zeros((30, 27, 1))
            img1[:, :, 0] = img[:, j * 28 + 1: (j + 1) * 28]
            letters.append(img1)
        prediction = list(model.predict(np.array(letters)))
        for predict in prediction:
            # if float(1) in list(predict):
            captcha += (chr(list(predict).index(max(list(predict))) + 97))
            # else:
            #     print(predict)
        captchas.append(captcha)
    letters = []
    for j in range(0, 2):
        letter = []
        for i in range(0, num):
            letter.append(captchas[i][j])
        letters.append(max(set(letter), key=letter.count))
    captcha = ''.join(letters)
    print(captcha)
    # a = input()
    return captcha


def login(model):
    num = 15
    request = requests.get(login_page)
    # print(request.headers)
    cookies = 'JSESSIONID=' + str(
        request.headers['Set-Cookie'].split(';')[0].split('=')[1]) + ';_ga=GA1.3.787589358.1533647200'
    try:
        captchas = []
        for i in range(0, num):
            captcha = ''
            img = get_captcha(cookies)
            img = filter_captcha(img)
            # cv2.imshow('img', img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            letters = []
            for j in range(0, 5):
                img1 = np.zeros((30, 27, 1))
                img1[:, :, 0] = img[:, j * 28 + 1: (j + 1) * 28]
                letters.append(img1)
            prediction = list(model.predict(np.array(letters)))
            for predict in prediction:
                # if float(1) in list(predict):
                captcha += (chr(list(predict).index(max(list(predict)))+97))
                # else:
                #     print(predict)
            captchas.append(captcha)
        letters = []
        for j in range(0, 5):
            letter = []
            for i in range(0, num):
                letter.append(captchas[i][j])
            letters.append(max(set(letter), key=letter.count))
        captcha = ''.join(letters)
        print(captcha)
    except:
        captcha = 'aaaaa'
    # print('write the captcha:')
    # captcha = input()
    data = 'username=' + username + '&password=' + password + '&passline=' + captcha + '&login=%D9%88%D8%B1%D9%88%D8%AF+%D8%A8%D9%87+%D9%BE%D9%88%D8%B1%D8%AA%D8%A7%D9%84'
    request = requests.post(login_page + 'login.jsp?' + data, headers={'Cookie': cookies})
    # print(request.headers)
    request = requests.post(right_menu, headers={'Cookie': cookies})
    f = open('result1.html', 'w')
    f.write(request.text)
    f.close()
    if 'Set-Cookie' in request.headers.keys():
        return False, request.text, cookies
    else:
        return True, 'done', cookies


def login_control(model):
    while True:
        returns = login(model)
        if returns[0]:
            return returns[2]
        print('login failed')
        sleep(drop_wait)


def get_course(input_value, cookies, model):
    # input_value = '1051112_1__'
    get_course = 'https://portal.aut.ac.ir/aportal/regadm/student.portal/student.portal.jsp?action=apply_reg&st_info=add&st_reg_course='+input_value+'&addpassline='+get_course_captcha(model, cookies)+'&st_course_add=%D8%AF%D8%B1%D8%B3+%D8%B1%D8%A7+%D8%A7%D8%B6%D8%A7%D9%81%D9%87+%DA%A9%D9%86'
    # print(get_course)
    request = requests.post(get_course, headers={'Cookie': cookies})
    while '(3)' in request.text:
        print('course captcha failed')
        sleep(drop_wait)
        request = requests.post(get_course, headers={'Cookie': cookies})
    # print(request.text)
    f = open('result.html', 'w')
    f.write(request.text)
    f.close()
    if 'اخذ شده' in request.text:
        return True
    else:
        return False


def main():
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("model.h5")
    print("Loaded model from disk")

    plan1 = []
    darsha = ['rev']
    # plan1, darsha = [], ['mm', 'me', 'ae', 'am', 'ds', 'af', 'r2', 't2', 'z2']
    # p1
    # plan1.append(('3102013_2__', 'mm')) #mm sedighi
    #
    # plan1.append(('3102043_2__', 'me')) #me
    #
    # plan1.append(('3102051_3__', 'ae')) #ae
    #
    # plan1.append(('3102021_6__', 'am')) #am
    #
    # plan1.append(('3102033_2_3102030_1', 'ds'))  # ds
    # plan1.append(('3102033_2_3102030_2', 'ds'))  # ds
    #
    # plan1.append(('1040111_7__', 't2')) # t2
    #
    # plan1.append(('1022391_12__', 'af'))  # afr2
    # plan1.append(('1022391_11__', 'af'))  # afs1
    # plan1.append(('1022391_42__', 'af'))  # afr1
    # plan1.append(('1022391_41__', 'af'))  # afs2

    plan1.append(('1051412_15__', 'rev')) #z2
#    plan1.append(('1061032_4__', 'z2')) #z2

    # plan1.append(('1011103_3_1011100_4', 'r2')) #r2
#    plan1.append(('1011103_3_1011100_5', 'r2')) #r2
 #   plan1.append(('1011103_3_1011100_6', 'r2')) #r2
    #
    # p2
    # plan2.append('3102013_1__') #mm
    # plan2.append('3102043_2__') #me
    # plan2.append('3102051_3__') #ae
    # plan2.append('3102021_6__') #am
    # plan2.append('3102033_2_3102030_1') #ds
    # plan2.append('3102033_2_3102030_2') #ds
    # plan2.append('1022391_1__') #afg
    # plan2.append('1022391_2__') #afs
    # # plan2.append('1011103_2_1011100_1') # r2 :/
    # plan2.append('1011103_4_1011100_6') #r2
    # plan2.append('1040111_7__') #t2
    # plan2.append('1051412_11__') #em1
    # plan2.append('1051412_12__')#em2
    # plan2.append('1051112_2__') #nd
    # plan2.append('1051112_1__') #nk
    


    # request = requests.get(login_page)
    # # print(request.headers)
    # cookies = 'JSESSIONID=' + str(
    #     request.headers['Set-Cookie'].split(';')[0].split('=')[1]) + ';_ga=GA1.3.787589358.1533647200'

    cookies = login_control(model)
    print('login done')
    requests.get('https://portal.aut.ac.ir/aportal/regadm/student.portal/student.portal.jsp?action=edit&st_info=register&st_sub_info=u_mine_all', headers={'Cookie': cookies})
    # get_course('2305213_1_2305210_1', cookies, model)

    # plans = [plan1, plan2]
    # all_courses = courses_output(cookies)
    # plans_output(all_courses,plans)

    # done = []
    # while True:
    #     for dars in darsha:
    #         for course in plan1:
    #             if course[1] == dars and dars not in done:
    #                 sleep(drop_wait)
    #                 if get_course(course[0], cookies, model):
    #                     done.append(dars)
    #                     break
    #         if dars in done:
    #             print(dars + ' done')
    #         else:
    #             print(dars + ' failed')
    #         if len(done) == len(darsha):
    #             return

    while True:
        for tab in menu_urls:
            sleep(drop_wait)
            request = requests.get(tab, headers={'Cookie': cookies})
            for course in plan1:
                if course[0] in request.text:
                    get_course(course[0], cookies, model)

    # print(request.content)
    # < input class ="stdcheckbox" type="checkbox" id="st_reg_course" name="st_reg_course" value="{CousreId}_{GroupNo}_{AssistCourseId}_{AssistGroupNo}" >
    # < input class ="stdcheckbox" type="checkbox" id="st_reg_course" name="st_reg_course" value="1011103_1_1011100_1" >

    # 'https://portal.aut.ac.ir/aportal/regadm/student.portal/student.portal.jsp?action=apply_reg&st_info=add&st_reg_course=3159573_1__&addpassline=ub&st_course_add=%D8%AF%D8%B1%D8%B3+%D8%B1%D8%A7+%D8%A7%D8%B6%D8%A7%D9%81%D9%87+%DA%A9%D9%86'
    # 'https://portal.aut.ac.ir/aportal/regadm/student.portal/student.portal.jsp?action=apply_reg&st_info=add&st_reg_course=3159573_1__&addpassline=vv&st_course_add=%D8%AF%D8%B1%D8%B3+%D8%B1%D8%A7+%D8%A7%D8%B6%D8%A7%D9%81%D9%87+%DA%A9%D9%86'
    exit()


if __name__ == "__main__":
    try:
        main()
    except:
        main()
