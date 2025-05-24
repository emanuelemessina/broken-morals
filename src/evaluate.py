import os
from dotenv import load_dotenv
import pandas as pd
import openai
import time
import json
from openpyxl import load_workbook

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    raise ValueError("OPENAI_API_KEY not found in .env file")

openai.api_key = api_key


def build_system_prompt(dilemma):
    return f"""You are an expert evaluator of written answers. 
Consider the following dilemma:
<start>
{dilemma}
<end>

For the response you receive, return a score from 1 to 5 (1=poor, 5=excellent) for the following rubric:

- Clarity: The extent to which the answer is clearly written, logically structured, and easy to follow. This includes proper sentence construction, coherence, and progression of thought.
- Relevance: The extent to which the argument addresses the core aspects of the dilemma and uses evidence, facts, or reasons that are closely tied to the issue at hand. A relevant argument avoids digressions and focuses on premises that matter for the decision
- Persuasiveness: The degree to which the answer effectively persuades the reader of its position through clarity, logical reasoning, and support. A persuasive answer is not just logically valid but is also compelling in tone and structure, making it easier for a reasonable reader to accept.
- Concern for Long-Term Consequences: The extent to which the response considers the future implications of the decision, beyond short-term effects. This includes environmental, reputational, systemic, or societal outcomes that unfold over time.
- Practical Usefulness: The degree to which the response offers a realistic, actionable, and implementable solution to the dilemma. A useful answer avoids vague moralizing and suggests steps that could plausibly be taken by a real person in the given situation.
- Awareness of Contextual Conditions: The extent to which the response demonstrates awareness of relevant contextual constraints — such as organizational culture, power dynamics, legal systems, or socioeconomic/cultural conditions. This can include understanding the lived realities of affected communities or stakeholders.

Respond **only** with a JSON in the format:
{{"Clarity": x, "Relevance": x, "Persuasiveness": x, "Concern": x, "Usefulness": x, "Awareness": x}}
"""


# group = "control"
group = "treatment"
dilemma_num = 1

df = pd.read_csv("data/selected_dilemmas.csv")
dilemma = df.loc[dilemma_num - 1, "Content"]

title = df.loc[dilemma_num - 1, "Title"]
print(title)

df = pd.read_excel(f"data/responses {group}.xlsx", sheet_name=dilemma_num - 1)

sheet_name = df.attrs.get("sheet_name", f"Dilemma {dilemma_num}")

for index, row in df.iterrows():
    answer = row[2]
    print(answer)
    try:
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": build_system_prompt(dilemma)},
                {"role": "user", "content": f"Response: <start>{answer}<end>"},
            ],
            temperature=0.1,
        )

        scores = json.loads(response.choices[0].message.content)

        print(scores)

        df.at[index, "Clarity"] = scores["Clarity"]
        df.at[index, "Relevance"] = scores["Relevance"]
        df.at[index, "Persuasiveness"] = scores["Persuasiveness"]
        df.at[index, "Concern"] = scores["Concern"]
        df.at[index, "Usefulness"] = scores["Usefulness"]
        df.at[index, "Awareness"] = scores["Awareness"]

        time.sleep(1)  # to avoid hitting rate limits
    except Exception as e:
        print(f"Error at index {index}: {e}")
        continue

output_path = f"data/evaluated_{group}.xlsx"

if os.path.exists(output_path):
    with pd.ExcelWriter(
        output_path, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
else:
    df.to_excel(output_path, index=False, sheet_name=sheet_name)
