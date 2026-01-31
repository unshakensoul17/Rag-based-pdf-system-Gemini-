-- Drop the old function first to ensure we replace it cleanly with new signature
drop function if exists match_documents;

-- Create the new function with filter_document_id support
create or replace function match_documents (
  query_embedding vector(768),
  match_threshold float,
  match_count int,
  filter_document_id uuid default null
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
  and (filter_document_id is null or document_chunks.document_id = filter_document_id)
  order by document_chunks.embedding <=> query_embedding
  limit match_count;
end;
$$;
