"""Deterministic study assistant; standard library only, no model or API."""
import re
import unicodedata
from dataclasses import dataclass

@dataclass(frozen=True)
class Reply:
    text: str
    intent: str
    end: bool = False

class StudyBot:
    """One instance per session. respond is the future service integration seam."""
    def __init__(self):
        self.waiting_minutes = False

    def respond(self, message):
        if not isinstance(message, str):
            return Reply('Please enter text, such as help.', 'invalid')
        if len(message) > 500:
            return Reply('Please shorten your message to 500 characters or fewer.', 'invalid')
        text = ' '.join(unicodedata.normalize('NFKC', message).casefold().split())
        text = text.strip(' .!?')
        if not text or not any(c.isalnum() for c in text):
            return Reply('Please type a question or enter help.', 'invalid')
        if text in ('bye', 'quit', 'exit'):
            self.waiting_minutes = False
            return Reply('Goodbye. Good luck with your studies!', 'goodbye', True)
        if text in ('cancel', 'reset'):
            self.waiting_minutes = False
            return Reply('Study planning canceled. Enter help for topics.', 'cancel')
        if text in ('help', 'menu', 'capabilities', 'what can you do'):
            return Reply('I can explain HCI, explain a chatbot lifecycle, give testing tips, and plan a study session. Try: HCI, lifecycle, testing, or study plan. Use cancel to reset or bye to exit.', 'help')
        if self.waiting_minutes:
            if not re.fullmatch(r'[0-9]{1,3}', text) or not 10 <= int(text) <= 180:
                return Reply('Enter a whole number from 10 to 180 minutes, or cancel.', 'invalid_minutes')
            minutes = int(text)
            self.waiting_minutes = False
            review = minutes // 3
            return Reply(f'For {minutes} minutes: review for {review}, practice for {minutes - review - 5}, and recap for 5.', 'plan')
        if re.search(r'\b(study plan|plan a study session)\b', text):
            self.waiting_minutes = True
            return Reply('How many minutes do you have? Enter 10 to 180, or cancel.', 'ask_minutes')
        topics = [
            ('hci', r'\b(hci|human computer interaction|human-computer interaction)\b', 'HCI studies how people interact with computers. A clear interface gives feedback and helps users recover from errors.'),
            ('lifecycle', r'\b(lifecycle|life cycle)\b', 'A chatbot lifecycle includes requirements, conversation design, implementation, testing, deployment, and maintenance.'),
            ('testing', r'\b(testing|test|tests)\b', 'Test expected prompts, paraphrases, ambiguous requests, malformed input, and multi-turn state transitions.')
        ]
        hits = [(name, answer) for name, pattern, answer in topics if re.search(pattern, text)]
        if len(hits) > 1:
            return Reply('Please ask about one topic at a time: HCI, lifecycle, or testing.', 'clarify')
        if hits:
            return Reply(hits[0][1], hits[0][0])
        if text in ('hi', 'hello', 'hey'):
            return Reply('Hello! I am StudyBot, a rule-based study assistant. Enter help to see my capabilities.', 'greeting')
        return Reply('I do not recognize that request. Enter help for supported topics.', 'fallback')

def main():
    bot = StudyBot()
    print('StudyBot | Traditional rule-based chatbot | Enter help or bye')
    while True:
        try:
            message = input('You: ')
        except (EOFError, KeyboardInterrupt):
            print('\nStudyBot: Goodbye!')
            break
        reply = bot.respond(message)
        print('StudyBot:', reply.text)
        if reply.end:
            break

if __name__ == '__main__':
    main()
