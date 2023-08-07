import openai
import datetime
from Slide_data import slide_contents


openai.api_key = ''


df_slide = slide_contents("PP_samples/sample.pptx")
# print(df_slide)
df_p1 = df_slide.iloc[0]
df_p3 = df_slide.iloc[2]

print(df_p1)

# for index, row in df_slide.iterrows():
#     print(f"Slide {index} data: {row}")

prompt = f"Act as a As a professional presentation assistant.  " \
         f"give me a presentation script by Topic:{df_p1[1]} Title:{df_p3[1]}, Content:{df_p3[2]}." \
         f"make the script funnier "

for index, page in df_slide.iterrows():

    print(page)
    prompt = f"Act as a As a professional presentation assistant.  " \
             f"give me a presentation script by " \
             f"Presentation topic:{df_p1[1]},this page title:{page[1]}, Content:{page[2]}." \
             f"make the script funnier "


# connect to GPT
response = openai.Completion.create(
engine="gpt-3.5-turbo",
prompt=prompt,
max_tokens=1000
)
print(response.choices[0].text.strip())