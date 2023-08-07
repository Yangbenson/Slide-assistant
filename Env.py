import gym
from gym import spaces

class PresentationEnv(gym.Env):
    def __init__(self):
        super(PresentationEnv, self).__init__()
        self.score = 0
        self.judges = ["interested", "uninterested", "neutral"]
        self.goal_score = 0.8

        # 這個到時候看要不要直接放一個固定的 prompt 先去做測試
        self.current_prompt = ""

        # Define action and observation space
        # They must be gym.spaces objects

        # 這邊必須想出有幾個文本上的選項可以改，然後去決定數字
        self.action_space = spaces.Discrete(2)  # For simplicity, let's assume the actions are binary: 0-change format, 1-maintain format

        self.observation_space = spaces.Box(low=0, high=1, shape=(1,1)) # For simplicity, assume the observation is the score

    # 這邊需要設定這環境可以選擇的方案（改prompt）
    def step(self, action):
        # Execute one time step within the environment
        self.current_prompt = self.get_new_prompt(action)
        self.score = self.get_score_from_judges(self.current_prompt)

        done = self.score >= self.goal_score
        reward = self.score  # You may want to adjust this

        # for debugging
        # 這邊得紀錄
        # 1.當前prompt
        # 2.當前score？
        # 3.修改後prompt
        # 4.修改後score？
        # 5.修改後是否變高分
        info = {}

        return self.current_prompt, reward, done, info

    def reset(self):
        # Reset the state of the environment to an initial state
        self.score = 0
        self.current_prompt = self.get_initial_prompt()
        return self.current_prompt

    def render(self, mode='human'):
        # Render the environment to the screen (optional)
        print(f"Current prompt: {self.current_prompt}")
        print(f"Current score: {self.score}")

    def close(self):
        pass

    def get_new_prompt(self, action):
        # TODO: Implement logic for changing the prompt based on action
        pass

    def get_score_from_judges(self, prompt):
        # TODO: Implement logic for getting scores from simulated judges
        pass

    def get_initial_prompt(self):
        # TODO: Implement logic for getting the initial prompt
        pass
