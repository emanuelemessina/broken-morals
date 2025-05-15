import os
from dotenv import load_dotenv
from plurals.deliberation import Ensemble, Moderator
from plurals.agent import Agent
import pandas as pd

# row in the csv
row = 3

df = pd.read_csv("selected_dilemmas.csv")
dilemma = df.loc[row - 1, "Content"]

print(f"DILEMMA {row}\n")
print(dilemma)

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if api_key:
    os.environ["DEEPSEEK_API_KEY"] = api_key
else:
    raise ValueError("DEEPSEEK_API_KEY not found in .env file")

model = "deepseek/deepseek-chat"

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
}

tasks = {
    "ensemble": f"""Please read the $DILEMMA below and answer the proposed questions.
You are free to express your reasoning, thoughts and opinions doing so.
Please stick to roughly 200 words in your response.

$DILEMMA
<start>
{dilemma}
<end>
""",
}

combination_instructions = {
    "moderator": """Summarize the key points of agreement and disagreement from the discussion below. Do not make a final recommendation.

<start>
${previous_responses}
<end>

Identify:
- The core tension(s) in the debate
- Points of agreement
- Areas of disagreement
- Open questions or reflections

Keep the tone neutral and informative. Focus on helping a human reader understand the trade-offs at play so they can form their own judgment.
"""
}

# inherit the structure task
ceo = Agent(persona=personas["ceo"], persona_template="default", model=model)
engineer = Agent(persona=personas["engineer"], persona_template="default", model=model)

agents = [ceo, engineer]

moderator = Moderator(
    persona="default",
    combination_instructions=combination_instructions["moderator"],
    model=model,
)

ensemble = Ensemble(agents, moderator=moderator, task=tasks["ensemble"])
ensemble.process()

print("FINAL RESPONSE\n")
print(ensemble.final_response)

print("STRUCTURE INFO\n")
print(ensemble.info)
