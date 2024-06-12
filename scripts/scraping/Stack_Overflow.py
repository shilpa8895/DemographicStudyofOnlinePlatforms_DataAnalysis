from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = []
    def handle_data(self, d):
        self.text.append(d)
    def get_data(self):
        return ''.join(self.text)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def fetch_questions_and_answers(keywords, save_directory):
    try:
        all_data = []

        for keyword in keywords:
            params = {
                'site': 'stackoverflow',
                'q': keyword,
                'sort': 'votes',
                'order': 'desc',
                'pagesize': 100
            }

            page = 1

            while True:
                params['page'] = page
                response = requests.get('https://api.stackexchange.com/2.3/search/advanced', params=params)
                response.raise_for_status()
                data = response.json()

                if 'items' in data:
                    questions = data['items']

                    for question in questions:
                        question_id = question['question_id']
                        answers = fetch_answers(question_id)
                        answer_texts = "\n\n".join([strip_tags(answer.get('body', '')) for answer in answers])

                        all_data.append({
                            "Keyword": keyword,
                            "Question Title": question['title'],
                            "Question Body": strip_tags(question.get('body', '')),
                            "Question Score": question['score'],
                            "Question View Count": question['view_count'],
                            "Question Creation Date": format_date(question['creation_date']),
                            "Question Last Activity Date": format_date(question['last_activity_date']),
                            "Answers": answer_texts
                        })

                    if len(questions) < 100:
                        break
                    else:
                        page += 1
                else:
                    break

        if all_data:
            df = pd.DataFrame(all_data)
            file_name = f"StackOverflowKeywords.csv"
            df.to_csv(os.path.join(save_directory, file_name), index=False)
            print(f"Exported to {os.path.join(save_directory, file_name)}")
        else:
            print("No questions found.")

    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


keywords = ['AusPost API']  
current_directory = os.getcwd()
fetch_questions_and_answers(keywords, current_directory)

