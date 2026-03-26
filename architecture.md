# architecture.md file

## Stack
- Next.js 14 (App Router)
- Supabase (auth + db)
- Tailwind CSS
## Key Folders
- /app → routes and pages
- /components → shared UI
- /lib → Supabase client, helpers
- /hooks → custom React hooks
## Data Flow
User → Auth (Supabase) → Protected Routes → API calls via /lib/api.ts