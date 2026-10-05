"""Code generation using AI."""
import logging
logger = logging.getLogger(__name__)
class CodeGenerator:
    def __init__(self, llm_router):
        self.llm = llm_router
    def generate_code(self, description, language='python'):
        prompt = f"Generate {language} code for: {description}"
        return self.llm.query(prompt)
    def generate_tests(self, function_signature):
        prompt = f"Generate unit tests for: {function_signature}"
        return self.llm.query(prompt)
    def optimize_code(self, code):
        prompt = f"Optimize this code: {code}"
        return self.llm.query(prompt)
    def refactor_code(self, code):
        prompt = f"Refactor this code: {code}"
        return self.llm.query(prompt)
    def format_code(self, code):
        prompt = f"Format this code: {code}"
        return self.llm.query(prompt)
    def lint_code(self, code):
        prompt = f"Lint this code: {code}"
        return self.llm.query(prompt)