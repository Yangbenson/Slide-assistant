import openai
import json
import datetime

openai.api_key = ''

def get_speech(messages):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
      # [
      #       {"role": "system", "content": "As a presenter who wants to present slides into an interesting tone speech that is less than 250 words."},
      #       {"role": "user", "content": f"Giving the information in one slide, with the topic of '5P analysis' and five following details, which are 'plan', 'pattern', 'positioning', 'perspective', and 'deployment'. The length has to be less than 250 words."},
      #   ]
    )


    print(response)

    # repsonse test
    # response = {
    #         "id": "chatcmpl-7ljmTHQWVhjD5djGe6WltQAR2toLg",
    #         "object": "chat.completion",
    #         "created": 1691611753,
    #         "model": "gpt-3.5-turbo-0613",
    #         "choices": [
    #             {
    #                 "index": 0,
    #                 "message": {
    #                     "role": "assistant",
    #                     "content": "Good afternoon, ladies and gentlemen! Today, I am delighted to present to you an intriguing topic in the world of business: the 5P analysis. In just a single slide, we will explore the essential elements that contribute to a successful business strategy.\n\nFirst up, we have \"plan.\" This is the foundation of any solid business strategy. It involves setting objectives, defining goals, and outlining the steps required to achieve them. Without a well-thought-out plan, success becomes a mere illusion.\n\nNext, we move on to \"pattern.\" This refers to the trends and patterns observed in the market. By understanding these patterns, businesses gain valuable insights into customer behavior, enabling them to make informed decisions and adapt their strategies accordingly.\n\nThe third element is \"positioning.\" It involves determining how your product or service stands out from the competition. Effective positioning ensures that your target market perceives your offering as unique and valuable, giving you a competitive edge.\n\nMoving on, we have \"perspective.\" This refers to the way your brand is perceived in the minds of consumers. By cultivating a positive and favorable perspective, businesses can establish trust, loyalty, and long-lasting relationships with their customers.\n\nLast but not least, we delve into \"deployment.\" This involves putting your plan into action and executing it effectively. Proper deployment ensures that all elements of your strategy work together seamlessly, maximizing your chances of achieving success.\n\nIn conclusion, the 5P analysis \u2013 plan, pattern, positioning, perspective, and deployment \u2013 forms the bedrock of a successful business strategy. By understanding and implementing these elements effectively, businesses can navigate the ever-changing landscape of the market, gaining a competitive advantage and reaching new heights of success. Thank you for your attention, and let's get ready to analyze our way to success!"
    #                 },
    #                 "finish_reason": "stop"
    #             }
    #         ],
    #         "usage": {
    #             "prompt_tokens": 84,
    #             "completion_tokens": 358,
    #             "total_tokens": 442
    #         }
    #     }

    speech = response["choices"][0]["message"]["content"]
    paragraphs = speech.split('\n\n')[1:-1]

    usage = response["usage"]

    record = {
        "promppt" : messages,
        "paragraphs" : paragraphs,
        "usage" : usage
    }

    return record

test = get_speech([
            {"role": "system", "content": "As a presenter who wants to present slides into an interesting tone speech that is less than 250 words."},
            {"role": "user", "content": "Giving the information in one slide, with the topic of '5P analysis' and five following details, which are 'plan', 'pattern', 'positioning', 'perspective', and 'deployment'. The length has to be less than 250 words."},
        ])
print(test)

