import os

import openai
from openai import AsyncOpenAI
import reflex as rx
from dotenv import load_dotenv
import anthropic
from tqdm import tqdm
from .embeddings_manager import EmbeddingGenerator as embeddings_manager
from .pinecone_manager import PineconeManager as pinecone_manager
import json
import requests
from bs4 import BeautifulSoup


class State(rx.State):
    question: str
    chat_history: list[tuple[str, str]] = []
    chat_open: bool = False
    faq_html: str = ""
    qa_pairs: list[dict] = []

    def init(self):
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
        #anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


    def fetch_page(self, url):
        """
        Fetch the HTML content of the given URL.
        """
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text

    def extract_qa_pairs(self, html):
        """
        Parse the HTML with BeautifulSoup, find all <h4> tags whose text begins with "Q ",
        then collect everything between that <h4> and the next <h4> as the answer.
        Returns a list of dicts: [{'question': ..., 'answer': ...}, ...].
        """
        soup = BeautifulSoup(html, 'html.parser')
        qa_list = []

        # Find all <h4> tags
        all_h4 = soup.find_all('h4')
        for h4 in all_h4:
            text = h4.get_text(strip=True)
            # Only consider headings that start with "Q " (e.g. "Q I.1 – …")
            if not text.startswith('Q '):
                continue

            question_text = text

            # Collect all sibling nodes until the next <h4>
            answer_parts = []
            for sibling in h4.next_siblings:
                if getattr(sibling, 'name', None) == 'h4':
                    # Reached the next question → stop collecting
                    break

                # We only care about non-empty text nodes and tags
                if isinstance(sibling, str):
                    s = sibling.strip()
                    if s:
                        answer_parts.append(s)
                else:
                    # If it's a tag, grab its text (stripping excess whitespace)
                    s = sibling.get_text(separator=" ", strip=True).replace('\xa0', ' ')
                    if s:
                        answer_parts.append(s)

            # Join all parts with two line breaks to preserve some structure
            answer_text = "\n".join(answer_parts).strip()
            # answer_text = " ".join(answer_parts).strip()

            qa_list.append({
                'question': question_text,
                'answer': answer_text
            })

        return qa_list

    def get_html_and_qa_pairs(self):
        url = "https://www.ecologie.gouv.fr/politiques-publiques/questions-reponses-dispositif-cee"
        html = self.fetch_page(url)
        qa_pairs = self.extract_qa_pairs(html)

        # Save to JSON file
        output_filename = "cee_questions_answers.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(qa_pairs, f, ensure_ascii=False, indent=2)

        return html, qa_pairs

    @rx.event
    def toggle_chat(self):
        self.chat_open = not(self.chat_open)

    @rx.event
    async def answer(self): #step1
        client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        session = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": self.question}],
            temperature=0.7,
            stream=True,
        )
        answer = ""
        self.chat_history.append((self.question, answer))
        self.question = ""
        yield
        async for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    break
                answer += item.choices[0].delta.content
                self.chat_history[-1] = (
                    self.chat_history[-1][0],
                    answer,
                )
                yield