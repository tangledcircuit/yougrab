from bs4 import BeautifulSoup
import re
import argparse

def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def format_code(code_text):
    lines = code_text.split('\n')
    if lines and not lines[0].strip().startswith('//'):
        lines[0] = f"// {lines[0].lstrip()}"
    return '\n'.join(lines)

def extract_conversation(html_file, agent_name="Born"):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    conversation = []
    
    questions = soup.find_all('div', {'data-testid': lambda x: x and x.startswith('youchat-question-turn-')})
    answers = soup.find_all('div', {'data-testid': lambda x: x and x.startswith('youchat-answer-turn-')})
    
    for q, a in zip(questions, answers):
        question_text = q.find('span', class_='sc-7240024a-4')
        if question_text:
            conversation.append(f"**TangledCircuit**: {clean_text(question_text.text)}\n")
        
        answer_content = []
        
        for element in a.find_all(['span', 'h4', 'pre', 'ul', 'ol']):
            if element.name == 'span' and 'AnswerParser_TextContainer__z_Iiv' in element.get('class', []):
                answer_content.append(clean_text(element.text))
            
            elif element.name == 'h4':
                answer_content.append(f"\n### {clean_text(element.text)}\n")
            
            elif element.name == 'pre':
                lang = element.find_previous('div', class_='language-label')
                lang_text = lang.get_text().strip() if lang else ''
                code_content = format_code(element.get_text())
                proper_lang = get_language(lang_text)
                answer_content.append(f"\n```{proper_lang}\n{code_content}\n```\n")
            
            elif element.name in ['ul', 'ol']:
                for item in element.find_all('li'):
                    answer_content.append(f"- {clean_text(item.text)}")
        
        if answer_content:
            conversation.append(f"**{agent_name}**: " + "\n".join(answer_content) + "\n")
    
    return "\n".join(conversation)

def get_language(lang_text):
    lang_map = {
        'typescript': 'typescript',
        'javascript': 'javascript',
        'python': 'python',
        'solidity': 'solidity',
        'sol': 'solidity',
        'bash': 'bash',
        'shell': 'bash',
        'json': 'json',
        'html': 'html',
        'css': 'css',
        'text': 'text',
        '': 'text'
    }
    lang = lang_text.lower().strip()
    return lang_map.get(lang, lang)

def main():
    parser = argparse.ArgumentParser(description='Convert You.com chat HTML to markdown')
    parser.add_argument('-i', '--input', required=True, help='Input HTML file path')
    parser.add_argument('-o', '--output', required=True, help='Output markdown file path')
    parser.add_argument('-n', '--name', default='Born', help='Agent name (default: Born)')
    
    args = parser.parse_args()
    
    try:
        markdown_output = extract_conversation(args.input, args.name)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown_output)
        print(f"Successfully converted {args.input} to {args.output} with agent name: {args.name}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
