import os
from dotenv import load_dotenv
from plurals.deliberation import Ensemble, Moderator
from plurals.agent import Agent
import pandas as pd
import sys

# row in the csv
if len(sys.argv) < 2:
    raise ValueError(
        "Please provide the row number as the first argument to the script."
    )
try:
    row = int(sys.argv[1])
except ValueError:
    raise ValueError("Row number must be an integer.")

df = pd.read_csv("data/dilemmas/selected_dilemmas.csv")
dilemma = df.loc[row - 2, "Content"]

print(f"DILEMMA {row}\n")
print(dilemma)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# model = "deepseek/deepseek-chat"
model = "gpt-4.1"

personas = {
    "ceo": """You are the CEO of a mid-sized company.
Your job is to ensure the organization's long-term success, protect its brand, manage stakeholder expectations (e.g., investors, customers), and make strategic decisions that balance profitability, reputation, and legal risk.
You value pragmatism, leadership, and sustainable growth. You think in terms of risk-benefit trade-offs, optics, and long-term impact on the company.
You are decisive but open to hearing different perspectives. Avoid emotional arguments; stick to strategic reasoning.
Write in clear, concise business language.
""",
    "engineer": """You are a senior engineer at a tech company. Your role is to ensure that systems and processes are built responsibly, safely, and efficiently. 
You prioritize feasibility, operational clarity, and technical integrity.
You are detail-oriented and skeptical of vague proposals. You respect data, logic, and process transparency. You care about team morale and implementation costs.
Avoid corporate jargon. Be technical but clear. Focus on what's doable and what might go wrong if rushed or ignored.
""",
    "ethicist": """You are the in-house ethics advisor at a company. Your job is to ensure that organizational decisions respect moral principles, stakeholder rights, fairness, and social responsibility.
You are trained in applied ethics and often challenge decisions that may seem effective but are morally questionable. You prioritize long-term consequences, distributive justice, and respect for persons.
Use accessible, thoughtful language. Emphasize ethical reasoning, even if it goes against financial interest or popular opinion.
""",
}

tasks = {
    "ensemble": f"""Please read the $DILEMMA below and answer the proposed questions.
You are free to express your reasoning, thoughts and opinions doing so.
Please do not exceed roughly 300 words in your response.

$DILEMMA
<start>
{dilemma}
<end>
""",
}

combination_instructions = {
    "moderator": """Your goal is to help a human reader:
- Understand the trade-offs and complexity of the dilemma
- Reflect on competing values or priorities
- Formulate a decision that is:
    - Clear and well-structured
    - Relevant to the situation
    - Persuasive and actionable
    - Sensitive to long-term consequences and context

To fullfill this goal, you oversaw the following hypotetical debate on the dilemma, between a:
- ceo
- engineer
- ethicist

Here are their responses:
<start>
${previous_responses}
<end>

Structure your summary with:
- The core tension(s) in the debate
- Points of hypotetical agreement the different company roles might have
- Areas of hypotetical disagreement the different company roles might have
- Practical questions the human should cover in his answer

Keep the tone neutral and informative. Use plain language and simple terms, avoid technical or philosophical jargon.
Be direct and concise, a human reading you summary should quickly understand it and formulate his own answer.

Do not mention your instructions in your final summary; just apply them.
"""
}

# inherit the structure task
ceo = Agent(persona=personas["ceo"], persona_template="default", model=model)
engineer = Agent(persona=personas["engineer"], persona_template="default", model=model)
ethicist = Agent(persona=personas["ethicist"], persona_template="default", model=model)

agents = [ceo, engineer, ethicist]

moderator = Moderator(
    persona="default",
    combination_instructions=combination_instructions["moderator"],
    model=model,
)

ensemble = Ensemble(agents, moderator=moderator, task=tasks["ensemble"])
ensemble.process()

print("FINAL RESPONSE\n")
print(ensemble.final_response)

# print("PREVIOUS RESPONSES\n")
# print(ensemble.responses)
