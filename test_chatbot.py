import unittest
from chatbot import StudyBot

class StudyBotTests(unittest.TestCase):
    def setUp(self):
        self.bot = StudyBot()
    def test_supported_prompts(self):
        for text, intent in [('hi','greeting'),('help','help'),('What is HCI?','hci'),('Explain the life cycle','lifecycle'),('testing tips','testing'),('bye','goodbye')]:
            with self.subTest(text=text): self.assertEqual(self.bot.respond(text).intent,intent)
    def test_normalization(self):
        self.assertEqual(self.bot.respond('  ＨＣＩ  !!! ').intent, 'hci')
    def test_word_boundaries(self):
        self.assertEqual(self.bot.respond('contest').intent,'fallback')
    def test_ambiguous_topics(self):
        self.assertEqual(self.bot.respond('HCI and testing').intent,'clarify')
    def test_malformed(self):
        for value in ['', '  ', '?!', None, 42, 'x'*501]:
            with self.subTest(value=str(value)[:20]): self.assertEqual(self.bot.respond(value).intent,'invalid')
    def test_unknown(self):
        self.assertEqual(self.bot.respond('weather tomorrow').intent,'fallback')
    def test_plan(self):
        self.assertEqual(self.bot.respond('study plan').intent,'ask_minutes')
        self.assertIn('review for 10, practice for 15, and recap for 5', self.bot.respond('30').text)
        self.assertFalse(self.bot.waiting_minutes)
    def test_bad_minutes_keep_state(self):
        self.bot.respond('study plan')
        for value in ['9','181','20.5','-10','ten']:
            self.assertEqual(self.bot.respond(value).intent,'invalid_minutes')
            self.assertTrue(self.bot.waiting_minutes)
    def test_plan_boundaries(self):
        for value in ['10','180']:
            self.bot.respond('study plan')
            self.assertEqual(self.bot.respond(value).intent,'plan')
    def test_help_keeps_state(self):
        self.bot.respond('study plan')
        self.assertEqual(self.bot.respond('help').intent,'help')
        self.assertTrue(self.bot.waiting_minutes)
    def test_cancel(self):
        self.bot.respond('study plan')
        self.bot.respond('cancel')
        self.assertEqual(self.bot.respond('HCI').intent,'hci')
    def test_exit(self):
        self.bot.respond('study plan')
        self.assertTrue(self.bot.respond('bye').end)
        self.assertFalse(self.bot.waiting_minutes)
    def test_session_isolation(self):
        self.bot.respond('study plan')
        self.assertEqual(StudyBot().respond('30').intent,'fallback')
    def test_determinism(self):
        self.assertEqual(self.bot.respond('HCI'),self.bot.respond('HCI'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
