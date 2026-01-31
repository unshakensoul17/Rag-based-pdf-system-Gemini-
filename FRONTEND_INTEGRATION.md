# Frontend Integration Guide

This guide explains how to connect your frontend (React, Next.js, or HTML/JS) to the RAG API.

## 1. API Client Setup
You will need the `API_URL` (e.g., `https://your-app.onrender.com/api/v1`) and the `API_KEY`.

### Integration Code (JavaScript/TypeScript)

Here is a ready-to-use utility file for your frontend project.

```typescript
// api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "your-secret-api-key-for-client-auth";

interface IngestResponse {
  document_id: string;
  filename: string;
  message: string;
}

interface QueryResponse {
  answer: string;
  sources: Array<{
    id: string;
    content: string;
    similarity: number;
    metadata: any;
  }>;
}

export const RagApi = {
  /**
   * Uploads a PDF for ingestion.
   */
  async ingestPDF(file: File): Promise<IngestResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_URL}/ingest`, {
      method: "POST",
      headers: {
        "X-API-Key": API_KEY,
      },
      body: formData,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Upload failed" }));
        throw new Error(error.detail || "Upload failed");
    }

    return response.json();
  },

  /**
   * Asks a question to the RAG system.
   */
  async query(question: string): Promise<QueryResponse> {
    const response = await fetch(`${API_URL}/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
      },
      body: JSON.stringify({ query: question, limit: 5 }),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Query failed" }));
        throw new Error(error.detail || "Query failed");
    }

    return response.json();
  }
};
```

## 2. Usage in a Component (React Example)

```tsx
import React, { useState } from 'react';
import { RagApi } from './api';

export default function ChatWithPDF() {
  const [file, setFile] = useState<File | null>(null);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  // Handle PDF Upload
  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      await RagApi.ingestPDF(file);
      alert("PDF uploaded successfully!");
    } catch (e) {
      alert("Error uploading PDF");
    } finally {
      setLoading(false);
    }
  };

  // Handle Chat Query
  const handleAsk = async (question: string) => {
    setLoading(true);
    try {
      const res = await RagApi.query(question);
      setAnswer(res.answer);
    } catch (e) {
      alert("Error getting answer");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button onClick={handleUpload} disabled={loading}>Upload</button>
      
      <div style={{ marginTop: 20 }}>
        <button onClick={() => handleAsk("Summarize this document")}>Summarize</button>
        {answer && <p>Answer: {answer}</p>}
      </div>
    </div>
  );
}
```

## 3. Environment Variables
Ensure your frontend has the correct environment variables set:
- `NEXT_PUBLIC_API_URL`: The URL of your deployed API (on Render).
- `NEXT_PUBLIC_API_KEY`: The same key configured in your backend `.env`.

