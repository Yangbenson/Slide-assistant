import pygame
import openai
import random

from Env import PresentationEnv # 匯入你的PresentationEnv環境

# 初始化OpenAI GPT-3.5，並使用你的API密鑰
openai_api_key = 'YOUR-OPENAI-API-KEY'
openai.api_key = openai_api_key

# 初始化pygame
pygame.init()

# 設定畫面尺寸
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
font = pygame.font.SysFont(None, 36)
input_box = pygame.Rect(50, 100, 700, 50)
# color_inactive = pygame.Color('lightskyblue3')
# color_active = pygame.Color('dodgerblue2')
# color = color_inactive

# 聊天機器人的邏輯
def chatbot():
    env = PresentationEnv()
    text = ''
    active = False
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive # 初始化color變量
    clock = pygame.time.Clock()
    while True:
        screen.fill((255, 255, 255))
        txt_surface = font.render(text, True, color)
        width = max(700, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        # 評分演講稿
                        action = random.choice([0, 1]) # 這裡你可以加入你的代理人邏輯
                        prompt = env.get_new_prompt(action)
                        prompt += f"\nUser's Speech: {text}"
                        # 使用OpenAI的GPT-3.5來評分
                        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=50)
                        score = env.get_score_from_judges(response.choices[0].text)
                        print(f"Speech Score: {score}")
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        clock.tick(30)

# 開始聊天機器人
chatbot()

# 退出pygame
pygame.quit()