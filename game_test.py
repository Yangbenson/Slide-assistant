import pygame
import openai

# 設置你的OpenAI API密鑰
openai.api_key = ''

def score_speech(speech):
    # 使用GPT-3.5來評分講稿（這部分可能需要自定義）
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=speech,
        max_tokens=50
    )

    # 返回回答作為分數（可能需要進一步處理來得到一個具體的分數）
    return response.choices[0].text

# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("聊天機器人")
font = pygame.font.Font(None, 36)
input_box = pygame.Rect(100, 100, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
clock = pygame.time.Clock()

while True:
    screen.fill((255, 255, 255))
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)
                    score = score_speech(text)
                    print(f'分數：{score}')
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    pygame.display.flip()
    clock.tick(30)
