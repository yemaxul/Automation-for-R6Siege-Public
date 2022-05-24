import time
import numpy as np
import roi_mate
import sim_input as si
GameStep = 0


def FastMode_program():  #快速选择模式，即选择地点、干员、确认通过三次回车完成
    global GameStep     #标志位用于确认当前游戏状态和识别步骤
    print("------------------------gamming_program------------------------")
    print("GameStep", GameStep)
    if (GameStep > 4):     #当GameStep>4时置零从新开始识别
        print("GameStep", GameStep)
        print("------------------------sim_input_Failed------------------------")
        print("retry_gamming_program")
        GameStep = 0
        FastMode_program()
    elif (GameStep == 3):   #当GameStep==3时，对是否进入游戏回合内识别
        if (roi_mate.roi_mate(GameStep) == 1):  #如果识别到进入游戏回合内
            si.sim_keyboard(GameStep)       #模拟玩家进行输入，防止系统踢出
        else:              #没识别到进入回合，GameStep+1进入下一个识别步骤
            si.sim_endkeyboard
            GameStep = GameStep+1
        FastMode_program()
    elif (GameStep <= 4 and GameStep != 3 and roi_mate.roi_mate(GameStep) == 1):    #识别是否进入选择地点、干员、确认、重开阶段
        si.sim_click(roi_mate.click_point, GameStep)        #做出点击确认操作
        print("GameStep", GameStep)
        if(GameStep==0):             #在快速确认模式中检测到在选择地点时，通过点击三次回车快速完成选择地点、干员确认三次操作
            GameStep=3
            si.sim_Enterkeyboard()
            time.sleep(0.5)
            si.sim_Enterkeyboard()
            time.sleep(0.5)
            si.sim_Enterkeyboard()
            print("press_Enter*3")
        FastMode_program()
    elif (GameStep<=4):         #识别失败，进入下一个识别阶段
        GameStep = GameStep+1
        FastMode_program()

def gamming_program():      #普通选择模式，即选择地点、干员、确认通过cv2进行识别确认后再进行操作，结构和快速模式相似
    global GameStep
    print("------------------------gamming_program------------------------")
    print("GameStep", GameStep)
    if (GameStep > 4):
        print("GameStep", GameStep)
        print("------------------------sim_input_Failed------------------------")
        print("retry_gamming_program")
        GameStep = 0
        gamming_program()
    elif (GameStep == 3):
        if (roi_mate.roi_mate(GameStep) == 1):
            si.sim_keyboard(GameStep)
        else:
            GameStep = GameStep+1
        gamming_program()
    elif (GameStep <= 4 and GameStep != 3 and roi_mate.roi_mate(GameStep) == 1):
        si.sim_click(roi_mate.click_point, GameStep)
        print("GameStep", GameStep)
        if (GameStep == 2 ):  
            time.sleep(0)
        if (GameStep==4):      
            si.sim_endkeyboard()
        GameStep = GameStep+1
        gamming_program()
    elif (GameStep<=4):
        GameStep = GameStep+1
        gamming_program()

roi_mate.Screen_Resolution()    #通过用户的输入，确认玩家游戏的分辨率并进行适配
time.sleep(3)
roi_mate.mate_Setting()     #对用于定位的图像Setting进行识别增加程序鲁棒性
roi_mate.Match_Constant()   #对已经进行标定的图像坐标轴，根据定位图像Setting和玩家输入的分辨率进行重新标定
#FastMode_program()      #a.快速选小叮当  
#gamming_program()      #b.cv模板匹配慢选  
roi_mate.draw_test()   # roi绘图坐标匹配调试
