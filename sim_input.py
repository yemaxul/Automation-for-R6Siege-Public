import random
import time

from pynput.keyboard import Key, Controller as c_keyboard
from pynput.mouse import Button, Controller as c_mouse

keyboard = c_keyboard()
mouse = c_mouse()


def sim_click(click_point: list, i):    #根据返回的坐标，随机生成新的临近坐标，模拟鼠标点击
    print("-------------------------sim_input.sim_click------------------------")
    rclick_point = (int(click_point[0])+random.randint(-10, 10),
                    int(click_point[0])+random.randint(-10, 10))
    mouse.position=(rclick_point[0], rclick_point[1])
    time.sleep(0.2)
    mouse.click(Button.left)
    time.sleep(0.2)
    #pyautogui.moveTo(rclick_point[0], rclick_point[1])
    keyboard.press(Key.enter)
    time.sleep(0.2)
    keyboard.release(Key.enter)
    print("sim_click_Succeed", i, rclick_point)


def sim_endkeyboard():  #模拟键盘TAB输入
    keyboard.press(Key.tab)
    time.sleep(0.1)
    keyboard.release(Key.tab)


def sim_Enterkeyboard():    #模拟键盘Enter输入
    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)


def sim_keyboard(i):    #游戏回合内随机模拟键盘输入
    print("-------------------------sim_input.sim_keyboard------------------------")

    key = ["v", "q", "e", "c", "1", "2"]
    randon_num = random.randint(0, 5)
    keyboard.press(key[randon_num])
    time.sleep(0.5)
    keyboard.release(key[randon_num])
    print(i, "Keyboard", key[randon_num])
    time.sleep(random.randint(3, 8))
