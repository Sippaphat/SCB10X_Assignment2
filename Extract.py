from trafilatura import fetch_url, extract
import re
import jsonlines

def extract_exam(text):
    # Regular expressions for question, choices, and answer patterns
    question_pattern = r"(\d+\.)(.+)"
    choice_pattern = r"([ก-ฮ]\.)(.+)"
    answer_pattern = r"เฉลย(.+)"

    questions = []
    current_question = {}

    for line in text.splitlines():
        line = line.strip()  # Remove leading/trailing whitespace

        # Match questions
        question_match = re.match(question_pattern, line)
        if question_match:
            if current_question:  # Save previous question if any
                questions.append(current_question)
            current_question = {
                "question": question_match.group(2),
            }

        # Match choices
        choice_match = re.match(choice_pattern, line)
        if choice_match:
            current_question[choice_match.group(1)] = choice_match.group(2)

        # Match answer
        answer_match = re.match(answer_pattern, line)
        if answer_match:
            current_question["answer"] = answer_match.group(1).strip()

    # Add the last question
    if current_question:
        questions.append(current_question)

    
    return questions

if __name__ == "__main__":
    url = "https://krupaga.wordpress.com/category/แบบทดสอบรายวิชาการประก/"

    downloaded = fetch_url(url)
    result = extract(downloaded)
    text = result
    exam_data = extract_exam(text)
    with jsonlines.open("extract_data.jsonl", mode='w') as writer:
        for item in exam_data:  # exam_data คือ list ของ dictionaries ที่เก็บข้อมูลข้อสอบ
            writer.write(item)