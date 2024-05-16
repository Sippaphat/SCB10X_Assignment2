# SCB10X_Assignment2
# Thai Food Recipe MCQ Dataset Generation

## Table of Contents
- [Introduction](#introduction)
- [Objectives](#objectives)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithm Overview](#algorithm-overview)
- [Dataset](#dataset)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction
This project aims to develop a Thai food recipe multiple-choice question (MCQ) dataset for evaluating the knowledge of a large language model (LLM). The dataset is created by scraping Thai food recipes from selected websites and generating MCQs based on the extracted information. The project ensures that the entire dataset is in the Thai language and maintains a high level of accuracy and relevance.

## Objectives
- Conduct research to identify and select authentic Thai food recipe websites.
- Develop and implement an efficient web scraping algorithm to extract detailed recipe information.
- Formulate multiple-choice questions (MCQs) from the extracted recipe data, ensuring clarity and relevance.
- Translate and validate the MCQs in Thai to maintain linguistic accuracy and cultural relevance.
- Design a robust process for verifying the accuracy and quality of the generated MCQs.
- Ensure cost-effectiveness by avoiding the use of large LLMs for the extraction process.
- Provide a detailed justification for the selected websites based on authenticity, variety, and user engagement.

## Requirements
- Python 3.7+
- Libraries: `trafilatura`, `re`, `jsonlines`, `dotenv`, `tqdm`, `concurrent.futures`
- OpenAI API Key (for question generation)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/thai-food-recipe-mcq-dataset.git
    cd thai-food-recipe-mcq-dataset
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up your environment variables:
    - Create a `.env` file in the project root directory and add your OpenAI API Key:
      ```plaintext
      Typhoon_API_KEY=your_openai_api_key
      ```

## Usage
1. Run the main script to fetch recipe data and generate the MCQ dataset:
    ```bash
    python main.py
    ```
2. The generated MCQ dataset will be saved as `exam_gen_data_test.jsonl` in the project directory.

## Algorithm Overview
1. **Load Necessary Components**:
    - Import essential libraries: `trafilatura`, `re`, `jsonlines`, `dotenv`, `tqdm`, `concurrent.futures`.

2. **Fetch and Extract Web Content**:
    - Use `fetch_url` to download HTML content from the specified URL.
    - Use `extract` to parse HTML content into text.

3. **Extract Recipe and Method Sections**:
    - Define functions to extract ingredients and cooking methods from the parsed text.

4. **Generate MCQs**:
    - Use the `Agent` class to generate MCQs from the extracted data.

5. **Save MCQs**:
    - Save the generated MCQs to a JSONL file using `jsonlines`.

## Dataset
The dataset consists of multiple-choice questions (MCQs) derived from authentic Thai food recipes. Each MCQ includes a question, four choices, and the correct answer, all in Thai. The dataset is structured to facilitate easy evaluation of the LLM's knowledge of Thai cuisine.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with a descriptive message.
4. Push your changes to the branch.
5. Create a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Special thanks to the authors of `trafilatura` and `jsonlines` for their excellent libraries.
- Thanks to [wongnai](https://www.wongnai.com/) and [แบบทดสอบรายวิชาการประกอบอาหารไทย ง 30230 ม.4](https://krupaga.wordpress.com/category/แบบทดสอบรายวิชาการประก/) for providing authentic Thai recipes used in this project.
- Thanks to OpenAI for providing the API used in generating the MCQs.
