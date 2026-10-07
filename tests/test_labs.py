import sys
import json
import unittest
from pathlib import Path
from pydantic import ValidationError
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from services.lab_service import Flashcards, Grade, LabService, EXAMPLES

class Fake:
    def __init__(self, *responses):
        self.responses = iter(responses)
        self.calls = 0
    def chat_json(self, *args):
        self.calls += 1
        value = next(self.responses)
        if isinstance(value, Exception):
            raise value
        return value

class LabTests(unittest.TestCase):
    def test_five_invalid_flashcard_cases(self):
        good = EXAMPLES['flashcards'][0][1]
        missing = json.loads(json.dumps(good))
        del missing['flashcards'][0]['answer']
        wrong_type = json.loads(json.dumps(good))
        wrong_type['flashcards'][0]['question'] = 42
        bad_difficulty = json.loads(json.dumps(good))
        bad_difficulty['flashcards'][0]['difficulty'] = 'expert'
        cases = ['not JSON', json.dumps(missing), json.dumps(wrong_type),
                 json.dumps(bad_difficulty), json.dumps({'flashcards': good['flashcards'][:2]})]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValidationError):
                Flashcards.model_validate_json(case)

    def test_grade_total_and_bounds(self):
        good = EXAMPLES['grade'][0][1]
        Grade.model_validate(good)
        for wrong in [dict(good, total=9), dict(good, functionality=5), dict(good, explanation=True)]:
            with self.assertRaises(ValidationError):
                Grade.model_validate(wrong)

    def test_repair_and_fallback(self):
        good = json.dumps(EXAMPLES['flashcards'][0][1])
        payload = {'topic': 'Python', 'difficulty': 'easy'}
        fake = Fake('{}', good)
        self.assertTrue(LabService(fake).run('flashcards', payload, 'model')['ok'])
        self.assertEqual(fake.calls, 2)
        result = LabService(Fake('{}', '{}')).run('flashcards', payload, 'model')
        self.assertFalse(result['ok'])
        self.assertIsNone(result['data'])

    def test_empty_input_does_not_call_api(self):
        fake = Fake()
        result = LabService(fake).run('feedback', {'assignment': '', 'code': 'x'}, 'model')
        self.assertFalse(result['ok'])
        self.assertEqual(fake.calls, 0)

    def test_missing_explanation_zero(self):
        sample, good = EXAMPLES['grade'][0]
        sample = dict(sample, explanation='')
        result = LabService(Fake(json.dumps(good), json.dumps(good))).run('grade', sample, 'model')
        self.assertFalse(result['ok'])

    def test_requested_difficulty(self):
        good = json.dumps(EXAMPLES['flashcards'][0][1])
        result = LabService(Fake(good, good)).run('flashcards', {'topic':'Python', 'difficulty':'hard'}, 'model')
        self.assertFalse(result['ok'])

    def test_api_error_no_exception_details(self):
        result = LabService(Fake(RuntimeError('secret'))).run('feedback', {'assignment':'Test','code':'x'}, 'model')
        self.assertFalse(result['ok'])
        self.assertNotIn('secret', result['message'])

if __name__ == '__main__':
    unittest.main()
