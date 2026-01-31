from typing import List

class ChunkingService:
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Simple recursive character splitting behavior.
        Splits text into chunks of roughly 'chunk_size' characters with 'overlap'.
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            
            # If we are not at the end of text, try to find a natural break header
            if end < text_len:
                # Try to split on newline first
                w_end = text.rfind('\n', start, end)
                if w_end == -1 or w_end < start + (chunk_size // 2): 
                    # If no newline, or newline is too far back, try space
                    w_end = text.rfind(' ', start, end)
                
                if w_end != -1 and w_end > start:
                    end = w_end + 1 # Include the delimiter
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = max(start + 1, end - overlap) 
            # Note: The logic above for 'start' is a simplified sliding window. 
            # A more robust one would strictly set start = end - overlap, 
            # but we need to ensure we don't get stuck if end did not advance much.
            # Simplified:
            start = end - overlap
            if start < 0: start = 0 # should not happen given loop condition
            
            # Break infinite loop if we aren't moving
            if end <= start:
                start = end
                
        return chunks
