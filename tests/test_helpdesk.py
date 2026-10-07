import sys
import unittest
from pathlib import Path
import httpx
from ollama import ResponseError
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from services.helpdesk_service import HelpdeskService, HelpdeskReply, EXAMPLES, build_messages, parse_reply
import json

GOOD = json.dumps(EXAMPLES[0][1], ensure_ascii=False)

class FakeLLM:
    def __init__(self, *results):
        self.results = iter(results)
        self.calls = 0

    def chat_json(self, model, messages, schema):
        self.calls += 1
        value = next(self.results)
        if isinstance(value, Exception):
            raise value
        return value

class HelpdeskTests(unittest.TestCase):
    def test_valid_and_fenced_json(self):
        for text in [GOOD, '```json\n' + GOOD + '\n```']:
            self.assertEqual(parse_reply(text).source, 'llm')

    def test_five_invalid_cases(self):
        valid = EXAMPLES[0][1]
        cases = ['not JSON', json.dumps({k:v for k,v in valid.items() if k != 'answer'}),
                 json.dumps(dict(valid, steps='wrong type')), json.dumps(dict(valid, category='unknown')),
                 json.dumps(dict(valid, unexpected='extra field'))]
        for raw in cases:
            with self.subTest(raw=raw), self.assertRaises((ValidationError, ValueError)):
                parse_reply(raw)

    def test_business_rule(self):
        with self.assertRaises(ValidationError):
            parse_reply(json.dumps(dict(EXAMPLES[1][1], follow_up='')))

    def test_repair_once(self):
        llm = FakeLLM('{}', GOOD)
        result = HelpdeskService(llm).ask('Giải thích F1', 'model')
        self.assertEqual(result.source, 'llm')
        self.assertEqual(llm.calls, 2)

    def test_fallback_validates(self):
        llm = FakeLLM('{}', '{}')
        result = HelpdeskService(llm).ask('Giải thích F1', 'model')
        self.assertEqual(result.status, 'fallback')
        HelpdeskReply.model_validate_json(result.model_dump_json())
        self.assertEqual(llm.calls, 2)

    def test_auth_error_no_retry_or_secret(self):
        llm = FakeLLM(ResponseError('secret-not-for-ui', status_code=401))
        result = HelpdeskService(llm).ask('Câu hỏi', 'model')
        self.assertEqual(llm.calls, 1)
        self.assertNotIn('secret-not-for-ui', result.model_dump_json())

    def test_timeout_and_rate_limit_retry(self):
        for error in [httpx.ReadTimeout('timeout'), ResponseError('rate', status_code=429)]:
            llm = FakeLLM(error, GOOD)
            self.assertEqual(HelpdeskService(llm).ask('Câu hỏi', 'model').source, 'llm')
            self.assertEqual(llm.calls, 2)

    def test_empty_and_long_input_no_api_call(self):
        llm = FakeLLM()
        for question in ['', ' ', 'x' * 4001]:
            self.assertEqual(HelpdeskService(llm).ask(question, 'model').source, 'fallback')
        self.assertEqual(llm.calls, 0)

    def test_few_shot_and_zero_shot(self):
        self.assertEqual(len(build_messages('New input')), 8)
        self.assertEqual(len(build_messages('New input', few_shot=False)), 2)
        for _, reply in EXAMPLES:
            HelpdeskReply.model_validate(reply)

if __name__ == '__main__':
    unittest.main()
