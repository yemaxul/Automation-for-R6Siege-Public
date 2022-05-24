import cv2
import pyautogui
import time
import numpy as np

Screen_Width = 1920
Screen_Height = 1080
Width_Scale = 1
Height_Scale = 1

OSetting_center_point = (1883, 36)  # 原生1080p全屏状态下Setting的位置
Setting_center_point = [1883, 36]  # 实际用户对应分辨率Setting的位置
click_point = []  # 保存返回的坐标轴

Constant = {"place": (131, 305), "noob": (111, 279), "confirm": (
    280, 279), "round": (727, 973), "end": (1334, 966)}  # 保存原生1080p全屏状态下标定好的坐标
MConstant = {}  # 保存匹配分辨率后，标定好的坐标
Step = ["place", "noob", "confirm", "round", "end"]  # 保存对应标定图像的文件名


def Match_Constant():  # 对Constant进行遍历，并根据分辨率和实际Setting的位置重新匹配写入到MConstant
    print("-------------------------roi_mate.Match_Constant------------------------")
    global OSetting_center_point
    global Setting_center_point
    global Width_Scale
    global Height_Scale
    global MConstant
    MConstant.clear()
    for key, value in Constant.items():
        tW = int(
            Setting_center_point[0]-int((OSetting_center_point[0]-value[0])*Width_Scale))
        tH = int(
            Setting_center_point[1]-int((OSetting_center_point[1]-value[1])*Height_Scale))
        print(Setting_center_point[0], int(
            (OSetting_center_point[0]-value[0])*Width_Scale))
        MConstant[key] = (tW, tH)
    for item in MConstant.items():  # 输出结果方便调试和检查状态
        print(item)
    print("-------------------------roi_mate.Match_Constant------------------------")


def Screen_Resolution():  # 向用户询问游戏分辨率并重新匹配变量
    print("-------------------------roi_mate.Screen_Resolution------------------------")
    global Screen_Width
    global Screen_Height
    global Width_Scale
    global Height_Scale
    global Screen_Width
    print("please input your width of game window")
    Screen_Width = 1920
    Screen_Width = input()
    print("please input your height of game window")
    Screen_Height = 1080
    Screen_Height = input()
    Width_Scale = int(Screen_Width)/1920
    Height_Scale = int(Screen_Height)/1080
    print("GameWindow_Resolution,matched")
    print(Screen_Width, Screen_Height, Width_Scale, Width_Scale)
    print("-------------------------roi_mate.Screen_Resolution------------------------")
    return ()


def get_screenshot():  # 截取屏幕图像并保存
    screenshot = pyautogui.screenshot()
    screenshot.save("./screenshot.png")
    time.sleep(0.6)
    print("get_screenshot,Succeed")


def mate_Setting():  # 使用Canny边缘检测，对Setting图标在相应分辨率下定位，确认其在游戏内的坐标
    print("-------------------------roi_mate.mate_Setting------------------------")
    global Setting_center_point
    Setting = cv2.imread("./matchedpng/setting.png")
    (tH, tW) = Setting.shape[:2]
    RWidth = int(tH*Width_Scale)
    RHight = int(tW*Height_Scale)
    Setting = cv2.resize(Setting, (RWidth, RHight))    # 对模板图像进行分辨率匹配
    Setting = cv2.cvtColor(Setting, cv2.COLOR_RGB2BGR)  # RGB2BGR
    Setting = cv2.cvtColor(Setting, cv2.COLOR_BGR2GRAY)  # 转换为灰度图片
    Setting = cv2.Canny(Setting, 50, 200)  # 执行边缘检测
    (tH, tW) = Setting.shape[:2]
    cv2.imwrite("./test/candy_setting.png", Setting)
    get_screenshot()
    img1 = cv2.imread("./screenshot.png")
    img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)  # RGB2BGR
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)    # 转换为灰度图片
    edged = cv2.Canny(img1, 50, 200)
    cv2.imwrite("./test/candy_edged.png", edged)

    result = cv2.matchTemplate(edged, Setting, cv2.TM_CCOEFF)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    clone = np.dstack([edged, edged, edged])
    cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
                  (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
    Setting_center_point[0:2] = [int(maxLoc[0]+tW/2), int(maxLoc[1] + tH/2)]
    cv2.circle
    cv2.imwrite("./test/mate_setting.png", clone)
    print("Setting_center_point:", Setting_center_point)
    print("mate_Setting,Succeed")
    print("-------------------------roi_mate.mate_Setting------------------------")
    return Setting_center_point


def mate1(img1, img2):  # 对img1进行模版匹配，识别其在img2的位置并返回坐标
    print("-------------------------roi_mate.mate1------------------------")
    tH, tW, = img2.shape[:2]  # 获取模板图像的高宽
    RWidth = int(tW*Width_Scale)
    RHight = int(tH*Height_Scale)
    img2 = cv2.resize(img2, (RWidth, RHight))
    tH, tW, = img2.shape[:2]
    cv2.imwrite("./test/resize_img2.png", img2)
    print("matchedpng:", tW, tH)
    result = cv2.matchTemplate(img1, img2, cv2.TM_SQDIFF_NORMED)
    upper_left = cv2.minMaxLoc(result)[2]
    clone = img1.copy()
    cv2.rectangle(clone, (upper_left[0], upper_left[1]),
                  (upper_left[0] + tW, upper_left[1] + tH), (0, 0, 255), 2)
    center_point = (int(upper_left[0]+(tW/2)),
                    int(upper_left[1]+(tH/2)))
    print("mate1_center_point:", center_point)
    cv2.imwrite("./test/mate1.png", clone)
    print("-------------------------roi_mate.mate1------------------------")
    return center_point

# 读取需要匹配的图像，对mate1(img1, img2)返回的坐标和实际Setting的坐标进行匹配，匹配成功后才进行操作，增加程序鲁棒性
def roi_mate(i):
    print("-------------------------roi_mate.roi_mate------------------------")
    global Step
    global MConstant
    global click_point
    click_point.clear()
    print(Step[i])
    value1 = MConstant.get(Step[i])
    get_screenshot()
    img1 = cv2.imread("./screenshot.png")
    img2 = cv2.imread("./matchedpng/"+Step[i]+".png")
    value2 = mate1(img1, img2)
    if ((int(value1[0])-10) <= int(value2[0]) <= (int(value1[0])+10)) and ((int(value1[1])-10) <= int(value2[1]) <= (int(value1[1])+10)):
        print("roi_mate_Succeed", value1, value2)
        flag = 1
        click_point = [value2[0], value2[1]]
    else:
        print("roi_mate_Failed", value1, value2)
        flag = 0
    print("-------------------------roi_mate.roi_mate------------------------")
    return flag


def draw_test():  # 绘图测试用于调试
    # mate_Setting()
    # Match_Constant()
    global click_points
    print("-------------------------roi_mate.draw_test------------------------")
    get_screenshot()
    img1 = cv2.imread("./screenshot.png")
    img2 = cv2.imread("./matchedpng/round.png")
    img3 = img1.copy()
    center_point = mate1(img1, img2)
    # roi_mate(i)
    #center_point = (int(click_point[0]),int(click_point[1]))
    #cv2.circle(img3,center_point , 20, (0, 255, 255), 2)
    cv2.circle(img3, center_point, 20, (0, 255, 255), 2)
    cv2.imwrite("./test/draw_test.png", img3)
    print("draw_test,Succeed")
    print("-------------------------roi_mate.draw_test------------------------")
