from openai import OpenAI

class Agent:
    def __init__(self, model_con : str, api_key :str, menu : list[str],recipes : list[str], method : list[str]):
        self.api_key = api_key
        self.menu = menu
        self.recipes = recipes
        self.method = method
        self.model_con = model_con
    def select_model(self):
        if self.model_con == "typhoon":
            print("Using Typhoon model")
            self.client = OpenAI(api_key=self.api_key, base_url="https://api.opentyphoon.ai/v1")
        else:
            print("No model selected")
    def get_response(self, user_prompt : str, model = "typhoon-instruct", max_tokens = 1000, temperature = 1.0, top_p = 0.1):
        self.select_model()
        messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_prompt},
    ]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
        content = response.choices[0].message.content
        return content
    
    def gen_question(self):
        user_prompt = f"""
        You are a recipe assessment expert. Your task is to create insightful multiple-choice questions (MCQs) in Thai that assess a user's comprehension of a given recipe and the cooking techniques involved.

        Input:

        * Recipe Name: {self.menu}
        * Ingredients: {self.recipes}
        * Instructions/Method: {self.method}

        Output: 

        Generate 3-5 MCQs that cover these areas:

        1. Ingredient Knowledge: Questions about ingredient substitutions, their functions in the dish, or how to select high-quality ingredients.
        2. Technique Understanding: Questions about specific cooking methods used in the recipe, their purpose, or potential challenges/troubleshooting.
        3. Recipe Comprehension: Questions about the overall process, the order of steps, or the reasoning behind certain instructions.
        4. Food Safety: Questions (where applicable) about safe handling practices, temperature checks, or storage instructions.

        Each MCQ should have:

        * A clear and concise question stem.
        * 4 answer choices (a, b, c, d) with only ONE correct answer.
        * A brief explanation of the correct answer, highlighting key points from the recipe or general cooking knowledge.
        
        This is a sample format for the MCQs (dictionary format):
        * "question": "คำในข้อใดต่อไปนี้สะกดถูกต้องทุกคำ", "a": "ผู้เรียน กฎ บันได เที่ยวอนุญาต", "b": "ไล่เลี่ยง ซึมเซ่บ แกงบวช สถิต นกอินทรีย์", "c": "อัตราคัด โล่ห์ ขบถ นกพิราบ เส้นทแยง", "d": "สำปรางแช่ง โขมย อะไหล่ อุโมงก์ โอกาส", "e": "ไข่มุก ผักคะน้า มุกตลก กะเทยะ รสแซ่บ", "answer": "e", "subject": "Thai"
        """
        mcq = self.get_response(user_prompt)
        return mcq