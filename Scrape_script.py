# load necessary components
from trafilatura import fetch_url, extract
import re
import os
import jsonlines
from time import time
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from tqdm import tqdm
import json
import concurrent.futures
from Agent import Agent

load_dotenv()

api_key = os.getenv('Typhoon_API_KEY')

def get_wongnai_recipe(by_line):
    recipes = []
    collecting_ingredients = False

    for line in by_line:
        if line == 'วัตถุดิบ':
            collecting_ingredients = True
        elif line == 'วิธีทำ':
            break
        elif collecting_ingredients:
            recipes.append(line)

    return recipes

def get_wongnai_method(by_line):
    recipes = []
    collecting_ingredients = False

    for line in by_line:
        if line == 'วิธีทำ':
            collecting_ingredients = True
        elif collecting_ingredients:
            recipes.append(line)

    return recipes

def fetch_recipe_urls(base_url):
    """
    Fetch and extract recipe URLs from the given base URL.

    Args:
        base_url (str): The URL of the website to scrape.

    Returns:
        list: A list of recipe URLs extracted from the webpage.
    """
    # Fetch the HTML content of the webpage
    downloaded = fetch_url(base_url)
    
    # Extract URLs from the fetched content, including links
    result = extract(downloaded, include_links=True)
    
    # Define a regex pattern to find and filter URLs in one step
    pattern = re.compile(r'\((recipes/[^\)]+)\)')
    
    # Use the pattern to find all matching URLs in the result
    urls = pattern.findall(result)
    
    return urls

def process_url(url):
    try:
        print(f"Processing {url}")
        full_url = f"https://www.wongnai.com/{url}"
        downloaded = fetch_url(full_url)
        result = extract(downloaded)
        by_line = result.split('\n')
        by_line = [line for line in by_line if line.strip() != '-']
        menu = re.findall(r'“(.*?)”', by_line[0])
        recipes = get_wongnai_recipe(by_line)
        method = get_wongnai_method(by_line)
        
        # Optional: Adjust or remove sleep time as needed
        time.sleep(1)  
        
        agent = Agent(model_con="typhoon", api_key=api_key, menu=menu, recipes=recipes, method=method)
        mcq = agent.gen_question()
        return mcq
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def extract_valid_json(items):
    """Extracts valid JSON objects from a list of strings."""
    valid_json_objects = []
    for item in items:
        # Attempt to load the item as JSON
        try:
            loaded_json = json.loads(item)  # Attempt to load as full JSON first
            valid_json_objects.append(loaded_json)
        except json.JSONDecodeError:  #If not, try to create a JSON
            for i in range(len(item)):
                try:
                    loaded_json = json.loads("{" + str(item[i:]) + "}")
                    valid_json_objects.append(loaded_json)
                    break  # Stop if a valid JSON is found
                except json.JSONDecodeError:
                    continue  # Try the next substring if not valid
    return valid_json_objects

def extract_exam_items(texts):
    """Extracts exam items from a list of Thai texts in various formats and returns them as a list of dictionaries.

    Args:
        texts: A list of strings, each containing text with exam items.

    Returns:
        A list of dictionaries, each representing an exam item.
    """
    all_exam_items = []
    for text in texts:
        # Check if the text is in JSON format
        if text.startswith("*"):
            try:
                items = extract_valid_json(text.split("*"))
                for item in items:
                    # Extract the question, answer, and subject values
                    question = item.pop("คำถาม")
                    answer = item.pop("answer")
                    subject = item.pop("subject")
                    
                    # Create a new dictionary with the desired order
                    new_item = {
                        "question": question,
                        "a": item.pop("a"),
                        "b": item.pop("b"),
                        "c": item.pop("c"),
                        "d": item.pop("d"),
                        "answer": answer,
                        "subject": "Food"
                    }

                    # Update the original item with the new dictionary
                    item.clear()  # Clear the original dictionary
                    item.update(new_item)  # Update with the new dictionary
                all_exam_items.extend(items)
                continue  # Skip the rest of the loop if JSON parsing is successful
            except json.JSONDecodeError:
                pass  # If not valid JSON, continue to the next format

        # Regular expressions for extracting different parts of the exam items
        question_pattern = r"คำถาม:\s*(.+)"
        choice_pattern = r"([a-e])[.)]\s*(.+)"
        answer_pattern = r"(?:คำตอบ|answer):\s*([a-d])[\)]*" 

        # Find all questions in the current text
        question_matches = re.finditer(question_pattern, text)

        exam_items = []
        for question_match in question_matches:
            item = {
                "question": question_match.group(1).strip(),
                "a": "",
                "b": "",
                "c": "",
                "d": "",
                "answer": "",
                "subject": "Thai food"  # Default subject (can be updated from text)
            }

            # Find choices and answer for the current question
            start = question_match.end()
            end = text.find("คำถาม:", start) if text.find("คำถาม:", start) != -1 else len(text)
            question_text = text[start:end]

            for choice_match in re.finditer(choice_pattern, question_text):
                item[choice_match.group(1)] = choice_match.group(2).strip()

            answer_match = re.search(answer_pattern, question_text)
            if answer_match:
                item["answer"] = answer_match.group(1)

            # # Update subject if found in the question text
            # subject_match = re.search(r"subject:\s*(\w+)", question_text)
            # if subject_match:
            #     item["subject"] = subject_match.group(1)

            exam_items.append(item)
        all_exam_items.extend(exam_items)
    return all_exam_items


if __name__ == "__main__":
    # Extract exam items from the list of texts
    base_url = "https://www.wongnai.com/recipes"
    recipe_urls = fetch_recipe_urls(base_url)
    # List to store MCQs
    mcqs = []

    # Using ThreadPoolExecutor for parallel processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_url, url): url for url in recipe_urls}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(recipe_urls)):
            mcq = future.result()
            if mcq:
                mcqs.append(mcq)
            
    extracted_items = extract_exam_items(mcqs)
        
    with jsonlines.open("exam_gen_data_test.jsonl", mode='w') as writer:
        for item in extracted_items:  # exam_data คือ list ของ dictionaries ที่เก็บข้อมูลข้อสอบ
            writer.write(item)