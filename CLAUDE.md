# Makir's AI Chief of Staff — Workspace

## Directory Map
```
~/Work/
├── nrg-bloom/      — NRG Bloom Inc. (modular data centers, emerging markets)
├── coldstorm/      — Coldstorm AI (AI consulting)
├── personal/       — Personal items
├── shared/         — Cross-company shared resources
│   ├── contacts/   — Contact profiles (JSON files)
│   ├── templates/  — Document templates
│   ├── goals.yaml  — Quarterly OKRs
│   ├── tasks.yaml  — Active task list
│   └── schedules.yaml — Weekly routines
└── knowledge/      — Persistent knowledge store
```

## Shared Resources
@shared/goals.yaml
@shared/tasks.yaml
@shared/schedules.yaml

## Session Start Protocol
On every new conversation, BEFORE responding to Makir's first message:
1. Read ~/Work/shared/tasks.yaml — flag overdue or due-today items
2. Check Gmail (makir@nrgbloom.com) for unread emails from key contacts: Dayo Adu, Julie Peeters, Oando contacts (Chioma, Eleas Eduga), TCS, Futurpreneur, Leyton/Ayming, accountant
3. Check today's calendar for meetings
4. If anything is urgent or time-sensitive, surface it at the top of your first response — even if Makir asked about something else
5. Within an active session, proactively check for updates when relevant topics come up — don't wait to be asked

## Available Skills
- **morning-review** — Daily briefing (calendar + emails + tasks + priorities)
- **email-triage** — Categorize and process inbox
- **meeting-prep** — Pre-meeting research and talking points
- **contact-enrichment** — Create/update contact records

## Available Commands
- `/gm` — Morning briefing
- `/triage` — Email triage
- `/weekly-review` — Weekly review and planning

## Available Agents
- **researcher** — Deep research specialist (web + files, read-only)
- **email-drafter** — Communication specialist (drafts only, never sends)
- **analyst** — Financial and data analysis

## Working Conventions
- Save NRG Bloom work to ~/Work/nrg-bloom/
- Save Coldstorm work to ~/Work/coldstorm/
- Save cross-company items to ~/Work/shared/
- Contact files go in ~/Work/shared/contacts/ as JSON
- Research outputs go in ~/Work/knowledge/
- Always check goals.yaml for quarterly context before prioritizing work
