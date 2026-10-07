import argparse
from core.config import settings
from services.helpdesk_service import HelpdeskService

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Student Helpdesk qua Ollama")
    parser.add_argument("question")
    parser.add_argument("--model", default=settings.ollama_model)
    parser.add_argument("--zero-shot", action="store_true")
    args = parser.parse_args()
    print(HelpdeskService().ask(args.question, args.model, few_shot=not args.zero_shot).model_dump_json(indent=2))
