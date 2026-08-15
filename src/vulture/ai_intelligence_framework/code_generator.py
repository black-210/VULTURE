"""AI-powered code generation & optimization."""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CodeGenerator:
    """AI-assisted code generation."""

    def __init__(self, llm_router=None):
        """
        Args:
            llm_router: LLMRouter instance
        """
        self.llm = llm_router

    def generate_function(self, description: str, language: str = 'python',
                         params: Dict = None) -> str:
        """Generate function from description.
        
        Args:
            description: Function description
            language: Programming language
            params: Parameter hints
            
        Returns:
            Generated code
        """
        if self.llm is None:
            logger.warning("No LLM router. Returning template code.")
            return f"# {language} function for: {description}"
        
        system_prompt = f"You are a {language} code generator. Generate clean, efficient, well-documented code."
        
        param_str = ", ".join([f"{k}: {v}" for k, v in (params or {}).items()])
        prompt = f"Generate a {language} function for: {description}. Parameters: {param_str}"
        
        response = self.llm.route_request(prompt, system_prompt)
        return response.get('response', '')

    def optimize_code(self, code: str, language: str = 'python') -> str:
        """Optimize existing code.
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            Optimized code
        """
        if self.llm is None:
            return code
        
        system_prompt = f"You are a {language} code optimizer. Improve performance, readability, and efficiency."
        prompt = f"Optimize this {language} code:\n{code}"
        
        response = self.llm.route_request(prompt, system_prompt)
        return response.get('response', code)

    def generate_tests(self, function_code: str, language: str = 'python') -> str:
        """Generate unit tests.
        
        Args:
            function_code: Function source code
            language: Programming language
            
        Returns:
            Generated test code
        """
        if self.llm is None:
            return "# Test code placeholder"
        
        system_prompt = f"Generate comprehensive {language} unit tests."
        prompt = f"Generate tests for:\n{function_code}"
        
        response = self.llm.route_request(prompt, system_prompt)
        return response.get('response', '')
