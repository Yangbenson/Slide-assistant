import pygame
import openai
import pyperclip
import pandas as pd
import pptx
from tkinter import filedialog
import tkinter as tk
from sys import platform as sys_pf
from Slide_data import slide_contents
import json
import time
import datetime

# 設置你的OpenAI API密鑰
openai.api_key = ''

# slide_contents('SummerProject/PP_samples/5p_sample.pptx')



# 初始化Pygame
pygame.init() # 初始化所有導入的pygame模塊

window_width, window_height = (800, 600)

screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE) # 創建800x600的可調整顯示窗口
pygame.display.set_caption("ChatBot") # 設置窗口標題為"ChatBot"
font = pygame.font.Font(None, 16) # 定義36點的字體
button_font = pygame.font.Font(None, 36)

def check_standards(insert_standards):

    # 1.simple
    # 2.unexpected
    # 3.concrete
    # 4.credible
    # 5.emotional
    # 6.has stories

    # Acedemic:001101
    # Business:011101
    # Educate:101111

    if insert_standards == [0,1,1,1,0,1]:
        return True
    else:
        return False



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
                 "content": f"Compose a succinct presentation for one slide, focusing on the topic of {data[1]}. It should incorporate {len(data[2])} specific details: {data[2]}. Please ensure that your description maintains a professional business tone, engages the audience, and does not exceed a limit of 250 words."}]
    return prompts

# -----------------------------------------------real---------------------------------------------------------------
#
# def get_speech(file):
#
#     if input_box_text == "":
#
#         df_speechs = pd.DataFrame(columns=['page', 'speech', 'usage', 'model'])
#
#         prompts = file2prompt(file)
#
#         for page in prompts:
#             page_prompt = prompts[f"{page}"]
#
#             response = openai.ChatCompletion.create(
#               model="gpt-3.5-turbo",
#               messages= page_prompt
#             )
#
#             model = response["model"]
#             speech = response["choices"][0]["message"]["content"]
#             paragraphs = speech.split('\n\n')[1:-1]
#             usage = response["usage"]
#
#             data = [page, paragraphs, usage, model]
#             df_speechs.loc[len(df_speechs)] = data
#
#         return df_speechs
#
#     else:
#
#         data = ["continue", input_box_text]
#
#         return data

# -----------------------------------------------test---------------------------------------------------------------

def get_speech(file):

    if input_box_text == "":
        data = [
            'page0',
            [
                "Welcome everyone! Today, we are going to dive into the world of strategic analysis with the 5Ps Analysis. By the end of this presentation, you'll be equipped with the knowledge to unlock your business's true potential. So, let's get started!",
                "First up, we have the 'Plan'. This crucial step involves setting clear objectives, determining the resources needed, and establishing a roadmap to achieve your goals. It's all about charting a course that maximizes efficiency and minimizes risks.",
                "Next is the 'Pattern'. By identifying trends and patterns within your industry, you gain insights into what works and what doesn't. Understanding these patterns allows you to make informed decisions and adapt your strategies accordingly.",
                "Then comes 'Positioning'. Knowing where you stand in relation to your competitors is vital. It involves analyzing your unique selling points, target audience, and market demands to develop a compelling value proposition. By positioning yourself effectively, you can carve out a niche and differentiate yourself from the competition.",
                "Moving on to 'Perspective', this step encourages you to look beyond your business and consider external factors such as economic, social, and technological changes. Keeping an eye on these broader perspectives allows you to anticipate opportunities and threats, ensuring your strategies remain relevant in a dynamic marketplace.",
                "Lastly, we have 'Deployment'. This phase is all about executing your plans effectively. It involves aligning resources, empowering your team, and monitoring progress to ensure timely and successful implementation of your strategies."
    ],
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

        data = [page_id,[paragraphs],usage_data,model_data]

        print(df_speechs)

        return data

    else:

        data = ["continue", input_box_text]

        return data


# ------------------------------------------------------------------------------------------------------------------


def score_speech(speech):

    try:
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages= [{
                "role": "system",
                "content": """Please conduct an analysis of the given speech, with particular attention to the reactions and expectations of the following four distinct audience groups:
    
                Those who value patience and thorough understanding
                Those who prefer a fast-paced and energetic delivery
                Those who pay close attention to detail and precision
                Those who focus on the overall concept and underlying themes
                Your task is to provide specific suggestions to enhance the speech's appeal to each of these audience types, considering their unique needs and inclinations.
                
                after suggestions, Is this speech simple, unexpected, concrete, credible, emotional, and has stories?
                Call back with the format:
                simple: yes or no
                unexpected: yes or no
                concrete: yes or no
                credible: yes or no
                emotional: yes or no
                has stories: yes or no.
    
                
                You must strictly adhere to the format provided below in your response:
                "
                {
                  "value_patience_and_thorough_understanding_audience": "Insert Edit Recommendations Here",
                  "fast_paced_and_energetic_delivery_audience": "Insert Edit Recommendations Here",
                  "pay_close_attention_to_detail_and_precision_audience": "Insert Edit Recommendations Here",
                  "focus_on_the_overall_concept_and_underlying_themes_audience": "Insert Edit Recommendations Here",
                  
                  "simple": "Insert yes or no",
                  "unexpected": "Insert yes or no",
                  "concrete": "Insert yes or no",
                  "credible": "Insert yes or no",
                  "emotional": "Insert yes or no",
                  "has_stories": "Insert yes or no"
                  
                }.
                "
                Please ensure that your response follows this exact structure, including only one recommendation for each audience type. Any deviation from this format will result in an incorrect analysis..
                """
          },
        {
                "role": "user",
                "content": f"{speech}"
        }]
        )

        data = response["choices"][0]["message"]["content"]
        print(data)
        whole_data = json.loads(data.strip())
        # 分割個評審給的分數
        patience_re = whole_data["value_patience_and_thorough_understanding_audience"]
        fast_paced_re = whole_data["fast_paced_and_energetic_delivery_audience"]
        detail_re = whole_data["pay_close_attention_to_detail_and_precision_audience"]
        concept_re = whole_data["focus_on_the_overall_concept_and_underlying_themes_audience"]

        simple_num = whole_data["simple"]
        unexpected_num = whole_data["unexpected"]
        concrete_num = whole_data["concrete"]
        credible_num = whole_data["credible"]
        emotional_num = whole_data["emotional"]
        has_stories_num = whole_data["has_stories"]

        usage = response["usage"]
        model = response["model"]

        result = [speech,
                patience_re,
                fast_paced_re,
                detail_re,
                concept_re,
                simple_num,
                unexpected_num,
                concrete_num,
                credible_num,
                emotional_num,
                has_stories_num,
                usage,
                model]

        return result

    except Exception:
        print(data.strip(), Exception)


def score_speech4test(speech):

    print(speech)
    testing_response = """value patience and thorough understanding Audience: For those who value patience and thorough understanding, it would be helpful to slow down the pace of the speech and provide more detailed explanations for each step of the 5Ps Analysis. This can be done by including specific examples or case studies that illustrate the concepts being discussed. Additionally, it would be beneficial to incorporate visual aids such as diagrams or charts to provide a visual representation of the ideas being presented.\n\nfast-paced and energetic delivery Audience: To cater to those who prefer a fast-paced and energetic delivery, it would be beneficial to maintain a quick tempo throughout the speech. The speaker can achieve this by using energetic and engaging language, incorporating dynamic body language and gestures, and injecting enthusiasm and excitement into their tone of voice. Including personal anecdotes or success stories can help captivate the attention of this audience group and keep them engaged.\n\npay close attention to detail and precision Audience: To appeal to the audience members who pay close attention to detail and precision, it would be helpful to provide more specific information and data to support the analysis being discussed. This can include statistics, market research findings, or real-world examples that demonstrate the effectiveness of each step of the 5Ps Analysis. Presenting the information in a structured and organized manner, such as using bullet points or subheadings, can also assist in ensuring clarity and precision.\n\nfocus on the overall concept and underlying themes Audience: For those who focus on the overall concept and underlying themes, it would be beneficial to highlight the interconnectedness between the steps of the 5Ps Analysis and emphasize the overarching purpose of strategic analysis. This can be achieved by summarizing the main points at the end of each section and emphasizing how they contribute to the overall success of a business. Additionally, tying in relevant industry trends or current events can help convey the broader implications of strategic analysis and its impact on business growth and sustainability."""
    # 返回回答作為分數（可能需要進一步處理來得到一個具體的分數）

    # 分割個評審給的分數
    patience_re = testing_response.split('\n\n')[0].split(":")[1]
    fast_paced_re = testing_response.split('\n\n')[1].split(":")[1]
    detail_re = testing_response.split('\n\n')[2].split(":")[1]
    concept_re = testing_response.split('\n\n')[3].split(":")[1]

    data = [speech, patience_re, fast_paced_re, detail_re, concept_re]

    return data

def get_edit(speech, advise, option):

    # 1 patient
    # 2 fast-pace
    # 3 detail
    # 4 concept

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"""The speech has been given a piece of advice by a judge: {advise[option - 1]}.
    
                          # Remaining content remains the same
                          Response Format:
                            \"
                            {{
                              \"the edited speech script\": \"insert the edited speech script here\",
                              \"simple\": \"yes or no\",
                              \"unexpected\": \"yes or no\",
                              \"concrete\": \"yes or no\",
                              \"credible\": \"yes or no\",
                              \"emotional\": \"yes or no\",
                              \"has stories\": \"yes or no\"
                            }}
                            \"
                            """
                },
                {
                    "role": "user",
                    "content": f"{speech}"
                }
            ]
        )
        raw_content = response["choices"][0]["message"]["content"].strip()
        print(raw_content)
        content = json.loads(raw_content)
        edit_speech = content["the edited speech script"]
        standards = [content["simple"],content["unexpected"],content["concrete"],content["credible"],content["emotional"],content["has stories"]]
        model = response["model"]
        usage = response["usage"]

        data = [edit_speech, standards, usage, model]

        print(data)

        return data

    except Exception as e:

        print(e)



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

# pygame 初設變數

game_state = "start"

process_record = pd.DataFrame(columns=['original_speech', 'original_standard', 'advise_choose', 'edit_speech', 'edit_standard'])

original_speech = ""
edit_speech = ""
advises = []
original_standards = []
edit_standard = []

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
        if game_state == "start":

            if event.type == pygame.MOUSEBUTTONDOWN: # 如果鼠標單擊
                if input_box.collidepoint(event.pos): # 如果在輸入框上單擊，切換活動狀態
                    active = not active

                elif load_ppt_button.collidepoint(event.pos):  # 如果在加載PPT按鈕上單擊
                    input_box_text = ""
                    score_text = ""
                    speech_scripts = get_speech(select_file()) #Dataframe
                    input_box_text = str(speech_scripts[1])[1:-1]
                    original_speech = input_box_text
                    active = True

                else:
                    active = False
                color = color_active if active else color_inactive # 更改顏色以反映活動狀態

            if event.type == pygame.KEYDOWN: # 如果按下鍵盤鍵

                if active: # 如果輸入框處於活動狀態

                    if event.key == pygame.K_RETURN: # 如果按下回車，打印文本，得分，並清空文本
                        reviews = score_speech(input_box_text)
                        # reviews = score_speech4test(input_box_text)

                        advises = reviews[1:5]
                        original_standards = [1 if review.lower() == "yes" else 0 for review in reviews[5:11]]
                        st2text = ', '.join([str(item) for item in original_standards]) # 'abc'
                        score_text = f"{st2text}" # 更新分数文本

                        if check_standards(original_standards) == True:
                            game_state = "finish"

                        game_state = "editing"

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

        elif game_state == "editing":

            if event.type == pygame.KEYDOWN:  # 如果按下鍵盤鍵

                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:

                    advise_choose = None
                    edit_response = None

                    if event.key == pygame.K_1:
                        edit_response = get_edit(original_speech, advises, 1)
                        advise_choose = 1

                    elif event.key == pygame.K_2:
                        edit_response = get_edit(original_speech, advises, 2)
                        advise_choose = 2

                    elif event.key == pygame.K_3:
                        edit_response = get_edit(original_speech, advises, 3)
                        advise_choose = 3

                    elif event.key == pygame.K_4:
                        edit_response = get_edit(original_speech, advises, 4)
                        advise_choose = 4

                    input_box_text = edit_response[0]
                    edit_speech = edit_response[0]
                    edit_standards = [1 if review.lower() == "yes" else 0 for review in edit_response[1]]
                    score_text = f"New Standard : {', '.join([str(item) for item in edit_standards])}"

                    new_row = pd.DataFrame({
                        'original_speech': original_speech,
                        'original_standard': [original_standards],
                        'advise_choose': f"advise_choose : {advise_choose} ,content:{advises[advise_choose-1]}",
                        'edit_speech': edit_speech,
                        'edit_standard': [edit_standards]
                    })

                    process_record = pd.concat([process_record, new_row], ignore_index=True)
                    print(process_record)

                    if check_standards(edit_standards) == True:
                        game_state = "finish"
                    else:
                        game_state = "start"

        elif game_state == "finish":
            now = datetime.datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H")
            path = 'Run_Record/'
            process_record.to_csv(f'record_{date_time_str}.csv', index=False)
            pygame.init()



    pygame.display.flip() # 更新整個顯示窗口
    clock.tick(30) # 控制遊戲迴圈速度，使每秒不超過30次迴圈