import pygame
import openai
import pyperclip
import pptx
from tkinter import filedialog
import tkinter as tk
from sys import platform as sys_pf

from Slide_data import slide_contents

# 設置你的OpenAI API密鑰
openai.api_key = ''

# slide_contents('SummerProject/PP_samples/5p_sample.pptx')

def select_file():

    # root = tk.Tk()
    # root.withdraw() # 隱藏主窗口
    # file_path = filedialog.askopenfilename() # 打開文件對話框選擇文件
    # print(f"選擇的文件路徑: {file_path}")
    # root.destroy()

    slide = slide_contents('PP_samples/5p_sample.pptx')
    return slide

def score_speech(speech):
    # 使用GPT-3.5來評分講稿（這部分可能需要自定義）
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=speech,
        max_tokens=50
    )

    # 返回回答作為分數（可能需要進一步處理來得到一個具體的分數）
    return response.choices[0].text

def score_speech4test(speech):
    print(speech)
    # 返回回答作為分數（可能需要進一步處理來得到一個具體的分數）
    return 4

def set_input_box(w_width,w_height):
    # 計算輸入框的位置和大小

    input_box_width = w_width * 0.7  # 輸入框寬度為視窗寬度的70%
    input_box_height = 200  # 輸入框高度固定為32
    input_box_x = (window_width - input_box_width) * 0.5  # 橫向位置
    input_box_y = w_height * 0.1  # 縱向位置
    input_box_result = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)

    return input_box_result

# PPT按鈕
load_ppt_button = pygame.Rect(50, 500, 200, 50)

# 初始化Pygame
pygame.init() # 初始化所有導入的pygame模塊

window_width, window_height = (800, 600)

screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE) # 創建800x600的可調整顯示窗口
pygame.display.set_caption("ChatBot") # 設置窗口標題為"ChatBot"
font = pygame.font.Font(None, 36) # 定義36點的字體

# 定義輸入框的位置和大小
input_box = set_input_box(window_width, window_height)

color_inactive = pygame.Color('lightskyblue3') # 定義非活動狀態的顏色
color_active = pygame.Color('dodgerblue2') # 定義活動狀態的顏色
color = color_inactive # 設置當前顏色為非活動狀態
active = False # 設置輸入框為非活動
text = '' # 初始化輸入文本
clock = pygame.time.Clock() # 用於控制遊戲迴圈的速度

while True:
    screen.fill((255, 255, 255)) # 將屏幕填充為白色
    txt_surface = font.render(text, True, color) # 以當前顏色渲染文本
    width = max(600, txt_surface.get_width() + 10)
    input_box.w = width # 設置輸入框的寬度
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5)) # 在螢幕上繪製文本
    pygame.draw.rect(screen, color, input_box, 2) # 繪製輸入框
    pygame.draw.rect(screen, (0, 128, 0), load_ppt_button)  # 繪製加載PPT按鈕
    load_label = font.render('Load PPT', True, (255, 255, 255))
    screen.blit(load_label, (load_ppt_button.x + 40, load_ppt_button.y + 10))


    for event in pygame.event.get(): # 遍歷所有事件

        if event.type == pygame.VIDEORESIZE:

            window_width, window_height = event.size
            screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

            base_input_box_width = window_width * 0.5  # 更新输入框基础宽度
            input_box = set_input_box(window_width, window_height) #重新定義框框

            # 重新計算輸入框等元素的大小和位置

        if event.type == pygame.QUIT: # 如果關閉窗口，退出程序
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN: # 如果鼠標單擊
            if input_box.collidepoint(event.pos): # 如果在輸入框上單擊，切換活動狀態
                active = not active

            elif load_ppt_button.collidepoint(event.pos):  # 如果在加載PPT按鈕上單擊
                select_file()

            else:
                active = False
            color = color_active if active else color_inactive # 更改顏色以反映活動狀態

        if event.type == pygame.KEYDOWN: # 如果按下鍵盤鍵

            if active: # 如果輸入框處於活動狀態

                if event.key == pygame.K_RETURN: # 如果按下回車，打印文本，得分，並清空文本
                    print(text)
                    # score = score_speech(text)
                    score = score_speech4test(text)
                    print(f'Score：{score}')
                    text = ''

                elif event.key == pygame.K_BACKSPACE: # 如果按下退格，刪除一個字符
                    text = text[:-1]

                elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_META:
                    # 如果按下Ctrl+C，則複製當前文字到剪貼板
                    pyperclip.copy(text)

                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_META:
                    # 如果按下Ctrl+V，則從剪貼板粘貼文字
                    text += pyperclip.paste()

                else:
                    text += event.unicode  # 否則，將按鍵添加到文本

    pygame.display.flip() # 更新整個顯示窗口
    clock.tick(30) # 控制遊戲迴圈速度，使每秒不超過30次迴圈
