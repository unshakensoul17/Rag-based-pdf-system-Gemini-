import google.generativeai as genai
from app.core.config import settings

class LLMService:
    @staticmethod
    def generate_answer(query: str, context: str) -> str:
        """
        Generates an answer based on the query and retrieved context.
        """
        model = genai.GenerativeModel(settings.GENERATION_MODEL)
        
        prompt = f"""
        You are a helpful assistant for a student notes platform.
        Use the following context to answer the student's question.
        If the answer is not in the context, say "I don't have enough information in the notes to answer that."
        
        Context:
        {context}
        
        Question:
        {query}
        
        Answer:
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "Sorry, I encountered an error while generating the answer."
