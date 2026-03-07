# Work Codex Roadmap

## Phase 1: Runtime foundation

Status: started

- Introduce a real code package
- Load and validate the workspace state
- Expose status and follow-up commands
- Add tests

## Phase 2: Safe state mutation

- Add commands to create and update tasks
- Add commands to update pipeline and funding records
- Add schema checks strong enough to prevent bad writes
- Add audit logging for every state change

## Phase 3: Agent orchestration

- Add scheduled routines for morning review and follow-up
- Add memory summarization and state compaction jobs
- Add adapters for external channels such as email and calendar
- Add policy guards for sensitive workstreams

## Phase 4: Service layer

- Add an API for multi-machine use
- Add background workers for 24/7 operations
- Separate sensitive evidence storage from Git-tracked metadata
- Add deployment configuration for a private runtime environment

## Product principle

The IP is not just prompts. The IP is:
- structured operating data
- repeatable workflows
- validation rules
- orchestration logic
- memory compression and retrieval strategy
