from bs4 import BeautifulSoup
import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_conversation(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    conversation = []
    
    questions = soup.find_all('div', {'data-testid': lambda x: x and x.startswith('youchat-question-turn-')})
    answers = soup.find_all('div', {'data-testid': lambda x: x and x.startswith('youchat-answer-turn-')})
    
    for q, a in zip(questions, answers):
        # Extract question
        question_text = q.find('span', class_='sc-7240024a-4')
        if question_text:
            conversation.append(f"**User**: {clean_text(question_text.text)}\n")
        
        # Extract answer
        answer_content = []
        
        # Process all elements in order
        for element in a.find_all(['span', 'h4', 'pre', 'ul', 'ol']):
            if element.name == 'span' and 'AnswerParser_TextContainer__z_Iiv' in element.get('class', []):
                answer_content.append(clean_text(element.text))
            
            elif element.name == 'h4':
                answer_content.append(f"\n### {clean_text(element.text)}\n")
            
            elif element.name == 'pre':
                lang = element.find_previous('div', class_='language-label')
                lang_text = lang.get_text().strip() if lang else ''
                code_content = element.get_text()
                answer_content.append(f"\n```{lang_text}\n{code_content}\n```\n")
            
            elif element.name in ['ul', 'ol']:
                for item in element.find_all('li'):
                    answer_content.append(f"- {clean_text(item.text)}")
        
        if answer_content:
            conversation.append("**Assistant**: " + "\n".join(answer_content) + "\n")
    
    return "\n".join(conversation)

if __name__ == "__main__":
    html_file = "your_conversation.html"
    markdown_output = extract_conversation(html_file)
    
    with open("conversation.md", "w", encoding="utf-8") as f:
        f.write(markdown_output)
