import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_contract(text):

    res = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"You are a contract legal risk expert."},
            {"role":"user","content":f"Analyze contract risks:\n{text[:3000]}"}
        ]
    )

    return res.choices[0].message.content


def rewrite_clause(clause):

    res = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Rewrite clause safely and legally balanced."},
            {"role":"user","content":clause}
        ]
    )

    return res.choices[0].message.content
