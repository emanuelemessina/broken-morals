# Broken Morals

Moral copilot for high-stakes ethical decisions in business contexts

## Resources

- [Paper](paper/broken-morals-2025.pdf)
- [Video pitch](https://www.youtube.com/watch?v=7_pmrzyQGHE) presenting the tool with product name "_Ensemble_"
- [Business Feasibility Study](handins/business-feasibility-study.pdf)
- [Responsible AI Report](handins/rai-cards.pdf) made with https://social-dynamics.net/ai-design/tool

## Release

A snapshot of this repo for the paper submission @ Crafting Tech 2025 is available [here](https://github.com/emanuelemessina/broken-morals/releases/tag/crafting-tech-2025)

## Documentation

Here we provide instructions to use the Broken Morals tool
and to replicate the findings we reported in the paper, explaining the function of each file.

Every script requires Python 3 to run.

### Use the tool

Install the requirements with

```bash
pip install -r tool/requirements.txt
```

Create a `.env` file in this directory with your OpenAI API key inside:

```ini
OPENAI_API_KEY=...
```

Choose a row number in [selected_dilemmas.csv](data/dilemmas/selected_dilemmas.csv) corresponding to the dilemma you want to run the tool on (the first dilemma is row `2`).

Launch the tool with the selected row number as argument:

```bash
python3 tool/main.py <row>
```

### Replicate findings

The [data](data) folder contains evey file needed to replicate the findings reported in the paper, including dilemma selection and statistical analysis on the evaluation ratings.

#### Moral classification of dilemmas

The [moral classification notebook](data/dilemmas/moral_classification.ipynb) scores the [original dilemma dataset](data/dilemmas/crafting_tech_8_business_ethics.csv) with the [MoralFoundationsClassifier](https://huggingface.co/MMADS/MoralFoundationsClassifier): it computes the classification score for each moral foundation, and it highlights the best scoring one, producing [a final xlsx file](data/dilemmas/moral_classification_scored.xlsx) containing the associations.

[selected_dilemmas.csv](data/dilemmas/selected_dilemmas.csv) contains our choices after manual selection, the ones we used in the user study.

#### Statistical analysis of ratings

The [responses](data/responses/) folder contains the participants' responses and the analysis files.

The two files under [questionnaire](data/responses/questionnarie/) contain the answers for [common likert questions](data/responses/questionnarie/ResponsesQuestionarie.csv) and [treatment only likert questions](data/responses/questionnarie/ToolQuestionarie.csv). The answers to the dilemmas are present in both files.

The [ratings](data/responses/ratings/) folder contains the three rubric rating tables (`RatingTableX.csv`, one for each evaluator), a [map](data/responses/ratings/AnswerID_Group.csv) from each answer ID to the group identifier (Control or Treatment) to perform blind evaluation, and the [final evaluation sheet](data/responses/ratings/FinalDataset.csv) with the rubric scores averaged along raters and dimensions.

The [stats notebook](data/responses/stats.ipynb) provides a step by step guide to perform the statistical tests and obtaining the [results](data/responses/statistical_analysis_results.csv) we reported in the paper.
