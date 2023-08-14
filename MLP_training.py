import gym
from gym import spaces


class SpeechEnv(gym.Env):
    def __init__(self):
        super(SpeechEnv, self).__init__()

        # 動作空間：修改的單詞的索引
        self.action_space = spaces.Discrete(100)  # 假設有100個可替換的單詞

        # 觀察空間：當前的提示
        self.observation_space = spaces.Discrete(100)  # 假設有100個不同的格式

        self.total_score = 10  # 80%的總分數
        self.score = 0
        self.score_threshold = 1
        self.prompt = "Your initial prompt here."

    def step(self, action):
        # 用動作替換提示中的單詞
        self.prompt = self.modify_prompt(self.prompt, action)

        # 計算分數（這個部分需要根據你的具體需求來實現）
        new_score = self.calculate_score(self.prompt)

        # 計算獎勵
        reward = new_score - self.score
        self.score = new_score

        # 檢查是否完成
        done = self.score >= self.total_score

        # 更新觀察
        observation = self.update_prompt(self.prompt, reward > 0)

        return observation, reward, done, {}

    def reset(self):
        self.score = 0
        self.prompt = "Your initial prompt here."
        return self.prompt

    def modify_prompt(self, prompt, action):
        # 替換prompt中的單詞（根據action的索引）
        # 需要根據你的具體需求來實現
        return prompt

    def calculate_score(self, prompt):
        # 根據prompt計算分數
        # 需要根據你的具體需求來實現
        return 0

    def update_prompt(self, prompt, score_increasing):
        # 根據分數的變化更新prompt
        # 需要根據你的具體需求來實現
        return prompt