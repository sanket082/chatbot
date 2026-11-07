# Traditional StudyBot
A deterministic Python chatbot for MSAI 631. No LLM, training, network calls, API keys, or third-party runtime dependencies.

## Run locally
Use Python 3.10 or newer. From this folder:
```
python chatbot.py
python -m unittest -v
```
Try `help`, `HCI`, `lifecycle`, `testing`, `study plan`, `30`, `cancel`, and `bye`.
The study plan is a simple demonstration heuristic, not personalized educational advice.

## Notebook / Google Colab
Upload StudyBot.ipynb to Colab and run the cells in order. It contains the exact chatbot and tests, writes them into the notebook working directory, demonstrates interactions, and provides an optional interactive loop. Cloud execution has not been verified; the notebook was executed locally.

## Design and lifecycle
Requirements: multiple prompts, capabilities, malformed input recovery, extensibility.
Design: normalization -> global commands -> pending study-plan slot -> topic rules -> fallback.
Implementation: `StudyBot.respond(message)` returns a `Reply(text, intent, end)`.
Validation: 14 unittest methods cover intents, validation, boundaries, ambiguity, state transitions, and session isolation. See evidence/test_results.txt.
Deployment: CLI and self-contained notebook. No hosted service has been deployed.
Maintenance: add examples and counterexamples with each new rule; run regression tests.
Future service adapter: preserve Reply and session isolation; put an optional provider behind the response boundary, with timeouts, error handling and consent before sending text externally. No cloud AI integration is implemented.

## Limitations
English only; spelling errors and unseen paraphrases can fall back. Keyword rules do not interpret negation. Multiple recognized educational topics cause clarification. A study-plan request has priority over educational topic matches. State is held in memory until process exit. No conversation logging.

## GitHub submission
Repository URL: https://github.com/sanket082/chatbot
The repository is public, allowing the instructor to read it without a collaborator invitation. Submit the repository URL and ZIP with the report.

## Attribution
Created with assistance from OpenAI ChatGPT for code, tests, report drafting, and formatting. The chatbot itself does not call ChatGPT or any language model. Review and personalize the report before submission; lecture/readings were not supplied.
References: https://docs.python.org/3/library/re.html ; https://docs.python.org/3/library/unittest.html ; https://www.nltk.org/api/nltk.chat.html
