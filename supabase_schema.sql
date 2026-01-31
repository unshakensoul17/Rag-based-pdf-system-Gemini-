-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store your documents
create table  if not exists documents (
  id uuid primary key default gen_random_uuid(),
  filename text not null,
  upload_hash text, -- useful for checking duplicates
  metadata jsonb,   -- for extra info like checking processing status, or original URL
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Create a table for chunks (the actual text parts + vectors)
create table if not exists document_chunks (
  id uuid primary key default gen_random_uuid(),
  document_id uuid references documents(id) on delete cascade,
  content text,
  embedding vector(768), -- Gemini Text Embedding 004 uses 768 dimensions
  chunk_index integer,
  metadata jsonb
);

-- Create a function to search for documents
create or replace function match_documents (
  query_embedding vector(768),
  match_threshold float,
  match_count int
)
returns table (
  id uuid,
  content text,
  similarity float,
  metadata jsonb
)
language plpgsql
as $$
begin
  return query
  select
    document_chunks.id,
    document_chunks.content,
    1 - (document_chunks.embedding <=> query_embedding) as similarity,
    document_chunks.metadata
  from document_chunks
  where 1 - (document_chunks.embedding <=> query_embedding) > match_threshold
  order by document_chunks.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- Create an index for faster queries (optional but recommended for scale)
create index on document_chunks using ivfflat (embedding vector_cosine_ops)
with (lists = 100);
