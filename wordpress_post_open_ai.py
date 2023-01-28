import requests
import base64

#wordpress login
wp_user = 'parvez'
wp_pass = 'nDXs WtqQ ARdJ ykOJ nUjF mzAT'
wp_credential = f'{wp_user}:{wp_pass}'
wp_token = base64.b64encode(wp_credential.encode())
wp_headers = {'Authorization': f'Basic {wp_token.decode("utf-8")}'}

def capitalize_first_letter(string):
    return ' '.join([word.capitalize() for word in string.split()])

def wph2(text):
    return f'<!-- wp:heading --><h2>{text}</h2><!-- /wp:heading -->'

def wph3(text):
    return f'<!-- wp:heading --><h3>{text}</h3><!-- /wp:heading -->'

def paragraph(text):
    return f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'

#Open Ai Access
def openai_text(prompt):
    import openai
    openai.api_key = 'SET YOUR API KEY'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    data = response.get('choices')[0].get('text').strip()
    return data

#file read from local disk
filename = "keywords.txt"
with open(filename, "r") as file:
    for line in file:
        post_title = capitalize_first_letter(f"{line} buying guide")
        intro = paragraph(openai_text(f"write down 150 words about {line}"))
        first_heading = wph2(f"Why get a {line}?")
        first_heading_paragraph = paragraph(openai_text(f"Why get a {line}?"))
        second_heading = wph2(f"Are {line} safe?")
        second_heading_paragraph = paragraph(openai_text(f"Are {line} safe?"))
        third_heading = wph3(f"What size {line} should I purchase?")
        third_heading_paragraph = paragraph(openai_text(f"What size {line} should I purchase?"))
        fourth_heading = wph3(f"What features should be considered while buying {line}?")
        fourth_heading_paragraph = paragraph(openai_text(f"What features should be considered while buying {line}?"))
        conclusion = paragraph(openai_text(f"Write down 200 words about {line} as conclusion"))

        content = f'{intro}{first_heading}{first_heading_paragraph}{second_heading}{second_heading_paragraph}{third_heading}{third_heading_paragraph}{fourth_heading}{fourth_heading_paragraph}{conclusion}'

        #wordpress post items
        post_data = {
            'title': post_title,
            'content': content,
            'categories': '3',
            'status': 'publish'
        }

        api_end_point = 'https://localhost/wp/wp-json/wp/v2/posts'
        r = requests.post(api_end_point, data=post_data, headers=wp_headers, verify=False)

        #wordpress post status
        if (r.status_code == 201):
            print("Post :", post_title, "successfully published")
        else:
            print(r.status_code)
