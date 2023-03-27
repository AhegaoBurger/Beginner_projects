import spacy
import openai
import os

openai.api_key = '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'


# Open the text file in read mode
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


text = read_text_file('D:\\Python\\reports\\full_reports\\aapl20221231.txt')


# Split the text into chunks of 500 words each
chunk_size = 500
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


# Generate summaries for each chunk
summaries = []
for i, chunk in enumerate(chunks):
    summary = openai.Completion.create(
        engine="text-ada-001",
        prompt=f"Summarize the following text:\n\n{chunk}\n Tl;dr",
        max_tokens=15,
        n=1,
        stop=None,
        temperature=0.5
    ).choices[0].text.strip()
    summaries.append(summary)
    filename = os.path.join('D:', os.sep, 'Python', 'reports', 'chunks', f'summary_{i+1}.txt')
    print(summary, file=open(filename, 'w', encoding='utf-8'))


merged_text = ' '.join(summaries)
print(merged_text, file=open('D:\\Python\\reports\\chunks\\merged_text\\merged.txt', 'w', encoding='utf-8'))


new_summary = openai.Completion.create(
    engine="text-ada-001",
    prompt=f"Summarize the following text:\n\n{merged_text}\n Tl;dr",
    max_tokens=150,
    n=1,
    stop=None,
    temperature=0.5
).choices[0].text.strip()
print(new_summary, file=open('D:\\Python\\reports\\summaries\\summary.txt', 'w', encoding='utf-8'))


nlp = spacy.load("en_core_web_sm")
doc = nlp(new_summary)
print(doc, file=open('D:\\Python\\reports\\spacy_summary\\spacy.txt', 'w', encoding='utf-8'))

# Extract named entities from the summary
key_notes = [ent.text for ent in doc.ents]
print(key_notes, file=open('D:\\Python\\reports\\key_notes\\notes.txt', 'w', encoding='utf-8'))


step_by_step = ''
for i, note in enumerate(key_notes):
    step_by_step += f"\n{i+1}. {note}"


def summarize_bare_essentials(notes):
    model_engine = "text-ada-001"
    prompt = f"Summarize the bare essentials of the report based on the following notes:\n{notes}\n Tl;dr"
    response = openai.Completion.create(engine=model_engine, prompt=prompt, temperature=0.5, max_tokens=100)
    bare_essentials = response.choices[0].text.strip()
    print(bare_essentials, file=open('D:\\Python\\reports\\bare_essentials\\bare.txt', 'w', encoding='utf-8'))
    return bare_essentials


def generate_blog_post(notes):
    model_engine = "text-ada-001"
    prompt = f"Write a blog post discussing the following notes:\n{notes}\n Tl;dr"
    response = openai.Completion.create(engine=model_engine, prompt=prompt, temperature=0.5, max_tokens=1000)
    blog_post = response.choices[0].text.strip()
    print(blog_post, file=open('D:\\Python\\reports\\blog_posts\\blog.txt', 'w', encoding='utf-8'))
    return blog_post


# def generate_midjourney_prompts(notes):
#     model_engine = "text-ada-001"
#     prompt = f"Generate some mid-journey prompts based on the following notes:\n{notes}"
#     response = openai.Completion.create(engine=model_engine, prompt=prompt, temperature=0.5, max_tokens=1000)
#     midjourney_prompts = response.choices[0].text.strip()
#     return midjourney_prompts
