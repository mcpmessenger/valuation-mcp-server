create table if not exists processing_jobs (
    id uuid primary key default gen_random_uuid(),
    user_id uuid,
    file_name text not null,
    file_type text not null,
    file_size bigint not null,
    storage_path text,
    analysis_target text not null,
    status text not null default 'queued',
    metadata jsonb default '{}'::jsonb,
    created_at timestamptz not null default timezone('utc'::text, now()),
    updated_at timestamptz not null default timezone('utc'::text, now())
);

create index if not exists processing_jobs_user_id_idx on processing_jobs(user_id);
create index if not exists processing_jobs_status_idx on processing_jobs(status);

create or replace function handle_processing_jobs_updated_at()
returns trigger as $$
begin
  new.updated_at = timezone('utc'::text, now());
  return new;
end;
$$ language plpgsql;

drop trigger if exists trg_processing_jobs_updated_at on processing_jobs;
create trigger trg_processing_jobs_updated_at
before update on processing_jobs
for each row
execute procedure handle_processing_jobs_updated_at();

create table if not exists analysis_results (
    id uuid primary key default gen_random_uuid(),
    job_id uuid references processing_jobs(id) on delete cascade,
    ocr_text text,
    textract_response jsonb,
    summary jsonb,
    vision_summary text,
    vision_metadata jsonb,
    vision_provider text,
    vision_cost jsonb,
    created_at timestamptz not null default timezone('utc'::text, now())
);

create index if not exists analysis_results_job_id_idx on analysis_results(job_id);
create unique index if not exists analysis_results_job_id_unique on analysis_results(job_id);

