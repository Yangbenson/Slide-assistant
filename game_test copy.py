import pygame
import openai
import pyperclip
import pandas as pd
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


def file2prompt(file): #file = page_dataframe, 這邊要把每頁slide轉成prompt，然後存入dataframe

    prompts = {}

    for index, data in file.iterrows():

        prompts[f"page{index}"] = [
                {"role": "system",
                 "content": "As a presenter who wants to present slides into an interesting tone speech that is less than 250 words."},
                {"role": "user",
                 "content": f"Giving the information in one slide, with the topic of {data[1]} and {len(data[2])} following details, which are {data[2]}. The length has to be less than 250 words."}]
    return prompts

# -----------------------------------------------real---------------------------------------------------------------

def get_speech(file):

    df_speechs = pd.DataFrame(columns=['page', 'speech', 'usage', 'model'])

    prompts = file2prompt(file)

    for page in prompts:
        page_prompt = prompts[f"{page}"]

        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages= page_prompt
        )

        model = response["model"]
        speech = response["choices"][0]["message"]["content"]
        paragraphs = speech.split('\n\n')[1:-1]
        usage = response["usage"]

        data = [page, paragraphs, usage, model]
        df_speechs.loc[len(df_speechs)] = data

    return df_speechs

# -----------------------------------------------test---------------------------------------------------------------

def get_speech(file):
    data = [
        'page0',
        [
            "Let's dive right into it. The 5P analysis consists of five key factors: Plan, Pattern, Positioning, Perspective, and Deployment. These factors, when examined together, provide a comprehensive understanding of any situation or strategy.",
            'First up, we have Plan. This is all about developing a clear and well-thought-out roadmap for success. Without a solid plan, we are simply wandering aimlessly, hoping for the best. But with a strong plan, we can set ourselves up for victory.',
            'Next, we have Pattern. This involves looking at past trends and identifying recurring themes. By studying patterns, we can anticipate future outcomes and make informed decisions.',
            'Moving on to Positioning. This is all about finding our unique place in the market or industry. We need to differentiate ourselves from the competition and position ourselves as the go-to solution for our target audience.',
            "Now, let's talk about Perspective. This is about taking a step back and seeing the bigger picture. By analyzing different perspectives, we can gain valuable insights and unlock new possibilities.",
            'Lastly, we have Deployment. This is all about executing our plans effectively and efficiently. Without proper deployment, even the best strategies may fail to yield the desired results.'],
        "'prompt_tokens': 82, 'completion_tokens': 366, 'total_tokens': 448",
        "'prompt_tokens': 82, 'completion_tokens': 366, 'total_tokens': 448"
    ]

    page_id = data[0]
    paragraphs = data[1]
    usage_data = data[2]
    model_data = data[3]

    # 創建一個空的DataFrame
    df_speechs = pd.DataFrame(columns=['page', 'speech', 'usage', 'model'])

    # 將每個段落和相關數據作為新行添加到DataFrame
    new_row = pd.DataFrame({
        'page': page_id,
        'speech': [paragraphs],
        'usage': usage_data,
        'model': model_data
    })
    df_speechs = pd.concat([df_speechs, new_row], ignore_index=True)

    print(df_speechs)

    return df_speechs

# ------------------------------------------------------------------------------------------------------------------

#
# def score_speech(speech):
#
#     response = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo",
#       messages= [{
#             "role": "system",
#             "content": """Please conduct an analysis of the following speech, considering the reactions and expectations of three distinct audience groups:
#
#             Those who are interested in the subject: Individuals who actively follow the topic and are likely to engage with the content.
#             Those who are neutral about the subject: People who neither have a strong liking nor disliking for the subject and might need engagement to sustain interest.
#             Those who are not interested in the subject: Individuals who typically find the subject unappealing and may need compelling reasons to pay attention.
#             Evaluate the speech for each of these audience groups, providing a rating score on a scale of 1 to 100, with 100 being the most favorable response.
#
#             Following the ratings, please offer specific suggestions to improve the speech's appeal to each of these audience groups, considering their unique needs and preferences.
#
#             It's crucial that you adhere strictly to the format provided below in your response:
#             "
#             Interested Audience: [Insert Rating Here]
#             Neutral Audience: [Insert Rating Here]
#             Uninterested Audience: [Insert Rating Here]
#
#             Interested Audience Edit Recommendations: [Insert Edit Recommendations Here] \n\n
#
#             Neutral Audience Edit Recommendations: [Insert Edit Recommendations Here] \n\n
#
#             Uninterested Audience Edit Recommendations: [Insert Edit Recommendations Here] \n\n
#             "
#             Please ensure that your response follows this exact structure, containing only one rating and one recommendation for each audience type, do not make addition response,
#             Failure to follow this format will result in an incorrect analysis.
#             """
#       },
#     {
#             "role": "user",
#             "content": f"{speech}"
#     }]
#     )
#
#     whole_data = response["choices"][0]["message"]["content"]
#
#     # 分割個評審給的分數
#     scores = whole_data.split('\n\n')[0]
#     score = scores.split('\n')
#
#     Interested_re = whole_data.split('\n\n')[1]
#     neutral_re = whole_data.split('\n\n')[2]
#     uninterested_re = whole_data.split('\n\n')[3]
#
#     Interested = score[0]
#     neutral = score[1]
#     uninterested = score[2]
#
#     usage = response["usage"]
#     model = response["model"]
#
#     data = [speech, Interested, neutral, uninterested, Interested_re, neutral_re, uninterested_re, usage, model]
#
#     return data

def score_speech4test(speech):

    print(speech)
    testing_response = """Interested Audience: 85\nNeutral Audience: 65\nUninterested Audience: 45\n\nInterested Audience Edit Recommendations: The speech is informative and provides a comprehensive overview of the 5P analysis. However, to further engage the interested audience, it could be beneficial to include specific examples or case studies that demonstrate the effectiveness of using the 5P analysis in different contexts. This will help this audience group better understand the practical application and impact of the analysis.\n\nNeutral Audience Edit Recommendations: While the speech provides a clear explanation of the 5P analysis, it could be more engaging for the neutral audience by incorporating interactive elements. For example, the speaker could ask questions or invite the audience to share their own experiences or thoughts related to each factor of the analysis. This will help sustain their interest and encourage active participation throughout the speech.\n\nUninterested Audience Edit Recommendations: To capture the attention of the uninterested audience, the speech needs to highlight the benefits and relevance of the 5P analysis in a more compelling way. This can be achieved by starting with a powerful and attention-grabbing opening statement that clearly conveys the value and impact of using this analysis. Additionally, incorporating storytelling or real-life examples that resonate with this audience could help them connect with the subject matter."
                    """
    # 返回回答作為分數（可能需要進一步處理來得到一個具體的分數）

    # 分割個評審給的分數
    scores = testing_response.split('\n\n')[0]
    score = scores.split('\n')
    Interested = score[0]
    neutral = score[1]
    uninterested = score[2]

    Interested_re = testing_response.split('\n\n')[1]
    neutral_re = testing_response.split('\n\n')[2]
    uninterested_re = testing_response.split('\n\n')[3]

    data = [speech, Interested, neutral, uninterested, Interested_re, neutral_re, uninterested_re]

    return data




# ---------pygame---------
def render_text(text, font, color, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        if font.size(current_line + word)[0] <= max_width:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines

def set_input_box(w_width,w_height):
    # 計算輸入框的位置和大小

    input_box_width = w_width * 0.7  # 輸入框寬度為視窗寬度的70%
    input_box_height = 200  # 輸入框高度
    input_box_x = (window_width - input_box_width) * 0.5  # 橫向位置
    input_box_y = w_height * 0.1  # 縱向位置
    input_box_result = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)

    return input_box_result

#
# def change_line(input_box_text):
#     # --------換行--------
#     lines = render_text(input_box_text, font, color, window_width * 0.6)
#     y_offset = 0
#     for line in lines:
#         txt_surface = font.render(line, True, color)
#         screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5 + y_offset))
#         y_offset += font.get_linesize()  # 增加 Y 方向的偏移量以換行
#
#     # 更新輸入框的高度，基於行數
#     input_box.h = max(32, y_offset + 10)
#     # -------------------

# PPT按鈕
# load_ppt_button = pygame.Rect(50, 500, 200, 50)

# 初始化Pygame
pygame.init() # 初始化所有導入的pygame模塊

window_width, window_height = (800, 600)

screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE) # 創建800x600的可調整顯示窗口
pygame.display.set_caption("ChatBot") # 設置窗口標題為"ChatBot"
font = pygame.font.Font(None, 24) # 定義36點的字體
button_font = pygame.font.Font(None, 36)

# 定義分数框的位置和大小
load_ppt_width = 200
load_ppt_height = 50
load_ppt_x = 10
load_ppt_y = window_height - load_ppt_height - 10
load_ppt_button = pygame.Rect(load_ppt_x, load_ppt_y, load_ppt_width, load_ppt_height)

# 定義分数框的位置和大小
score_box_width = 200
score_box_height = 50
score_box_x = window_width - score_box_width - 10
score_box_y = window_height - score_box_height - 10
score_box = pygame.Rect(score_box_x, score_box_y, score_box_width, score_box_height)
score_text = ''  # 初始化分数文本

# 定義輸入框的位置和大小
input_box = set_input_box(window_width, window_height)

color_inactive = pygame.Color('lightskyblue3') # 定義非活動狀態的顏色
color_active = pygame.Color('dodgerblue2') # 定義活動狀態的顏色
color = color_inactive # 設置當前顏色為非活動狀態
active = False # 設置輸入框為非活動
input_box_text = '' # 初始化輸入文本
clock = pygame.time.Clock() # 用於控制遊戲迴圈的速度


game_state = "welcome"

while True:
    screen.fill((255, 255, 255)) # 將屏幕填充為白色

    # 輸入框
    txt_surface = font.render(input_box_text, True, color) # 以當前顏色渲染文本
    width = max(600, txt_surface.get_width() + 10)
    input_box.w = width # 設置輸入框的寬度
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5)) # 在螢幕上繪製文本
    pygame.draw.rect(screen, color, input_box, 2) # 繪製輸入框

    # 分數框
    pygame.draw.rect(screen, color_inactive, score_box, 2)  # 画分数框
    score_font = pygame.font.Font(None, 18)
    score_label = score_font.render(f"Score: {score_text}", True, (0, 0, 0))
    screen.blit(score_label, (score_box.x + 5, score_box.y + 15))  # 在屏幕上绘制分数文本

    # PPT按鈕
    pygame.draw.rect(screen, (0, 150, 100), load_ppt_button)  # 繪製加載PPT按鈕
    load_label = button_font.render('Load PPT', True, (255, 255, 255))
    screen.blit(load_label, (load_ppt_button.x + 40, load_ppt_button.y + 10))


    # --------換行--------
    lines = render_text(input_box_text, font, color, window_width * 0.6)
    y_offset = 0
    for line in lines:
        txt_surface = font.render(line, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5 + y_offset))
        y_offset += font.get_linesize()  # 增加 Y 方向的偏移量以換行

    # 更新輸入框的高度，基於行數
    input_box.h = max(32, y_offset + 10)
    # -------------------



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

                speech_scripts = get_speech(select_file()) #Dataframe
                print(speech_scripts)
                input_box_text = str(speech_scripts.iloc[0,1])[1:-1]
                active = not active

            else:
                active = False
            color = color_active if active else color_inactive # 更改顏色以反映活動狀態

        if event.type == pygame.KEYDOWN: # 如果按下鍵盤鍵

            if active: # 如果輸入框處於活動狀態

                if event.key == pygame.K_RETURN: # 如果按下回車，打印文本，得分，並清空文本
                    # score = score_speech(input_box_text)
                    score = score_speech4test(input_box_text)
                    score_text = f"{score[1]} \n {score[2]} \n {score[3]}" # 更新分数文本
                    print(f'Score：{score_text}')
                    input_box_text = ''

                elif event.key == pygame.K_BACKSPACE: # 如果按下退格，刪除一個字符
                    input_box_text = input_box_text[:-1]

                elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_META:
                    # 如果按下Ctrl+C，則複製當前文字到剪貼板
                    pyperclip.copy(input_box_text)

                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_META:
                    # 如果按下Ctrl+V，則從剪貼板粘貼文字
                    input_box_text += pyperclip.paste()

                else:
                    input_box_text += event.unicode  # 否則，將按鍵添加到文本

    pygame.display.flip() # 更新整個顯示窗口
    clock.tick(30) # 控制遊戲迴圈速度，使每秒不超過30次迴圈
