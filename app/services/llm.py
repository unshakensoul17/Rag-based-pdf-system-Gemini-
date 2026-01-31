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
        Use the following context to answer the student's question efficiently and accurately.
        If the exact answer is not explicitly stated in the context, try to infer it from the related information provided.
        If the context is completely irrelevant, politely state that the notes don't cover this topic.
        
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
