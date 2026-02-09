# Tasks: MCP Task Management Server

**Input**: Design documents from `/specs/1-mcp-task-management/`
**Prerequisites**: plan/impl-plan.md (required), spec.md (required for user stories), plan/data-model.md, plan/contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` at repository root
- **Database**: `backend/database.py`
- **Models**: `backend/models/`
- **Routes**: `backend/routes/`
- **Tools**: `backend/tools/`
- **Tests**: `backend/tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in backend/
- [X] T002 Initialize Python project with FastAPI, SQLModel, Official MCP SDK dependencies in backend/requirements.txt
- [X] T003 [P] Configure linting and formatting tools (Black, Flake8) in backend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Setup database schema and migrations framework in backend/database.py
- [X] T005 [P] Implement SQLModel Task entity in backend/models/task_model.py based on data-model.md
- [X] T006 [P] Setup FastAPI application structure in backend/main.py
- [X] T007 Create base MCP server configuration in backend/server_config.py
- [X] T008 Configure error handling and logging infrastructure in backend/utils/error_handlers.py
- [X] T009 Setup environment configuration management for Neon PostgreSQL in backend/config.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task via MCP Tool (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks through the MCP interface

**Independent Test**: Can be fully tested by calling the add_task MCP tool with valid parameters and verifying that a new task is persisted in the database with the correct attributes.

### Implementation for User Story 1

- [X] T010 [US1] Implement add_task MCP tool in backend/tools/task_operations.py
- [X] T011 [US1] Create database function to add task in backend/database.py
- [X] T012 [US1] Add validation for add_task input parameters
- [ ] T013 [US1] Test add_task functionality with valid parameters
- [ ] T014 [US1] Test add_task error handling for invalid input

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - List All Tasks via MCP Tool (Priority: P1)

**Goal**: Enable users to list all tasks through the MCP interface

**Independent Test**: Can be fully tested by calling the list_tasks MCP tool and verifying that all existing tasks in the database are returned correctly.

### Implementation for User Story 2

- [X] T015 [US2] Implement list_tasks MCP tool in backend/tools/task_operations.py
- [X] T016 [US2] Create database function to retrieve all tasks in backend/database.py
- [X] T017 [US2] Add validation for list_tasks input parameters
- [ ] T018 [US2] Test list_tasks functionality with multiple tasks
- [ ] T019 [US2] Test list_tasks functionality with no tasks (empty list)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task via MCP Tool (Priority: P2)

**Goal**: Enable users to update existing tasks through the MCP interface

**Independent Test**: Can be fully tested by calling the update_task MCP tool with valid parameters and verifying that the task is updated in the database.

### Implementation for User Story 3

- [X] T020 [US3] Implement update_task MCP tool in backend/tools/task_operations.py
- [X] T021 [US3] Create database function to update task in backend/database.py
- [X] T022 [US3] Add validation for update_task input parameters
- [ ] T023 [US3] Test update_task functionality with valid parameters
- [ ] T024 [US3] Test update_task error handling for non-existent task

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Complete Task via MCP Tool (Priority: P2)

**Goal**: Enable users to mark tasks as complete through the MCP interface

**Independent Test**: Can be fully tested by calling the complete_task MCP tool and verifying that the task's completion status is updated in the database.

### Implementation for User Story 4

- [X] T025 [US4] Implement complete_task MCP tool in backend/tools/task_operations.py
- [X] T026 [US4] Create database function to update task status to completed in backend/database.py
- [X] T027 [US4] Add validation for complete_task input parameters
- [ ] T028 [US4] Test complete_task functionality with valid task ID
- [ ] T029 [US4] Test complete_task error handling for non-existent task

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Task via MCP Tool (Priority: P3)

**Goal**: Enable users to delete tasks through the MCP interface

**Independent Test**: Can be fully tested by calling the delete_task MCP tool and verifying that the task is removed from the database.

### Implementation for User Story 5

- [X] T030 [US5] Implement delete_task MCP tool in backend/tools/task_operations.py
- [X] T031 [US5] Create database function to delete task in backend/database.py
- [X] T032 [US5] Add validation for delete_task input parameters
- [ ] T033 [US5] Test delete_task functionality with valid task ID
- [ ] T034 [US5] Test delete_task error handling for non-existent task

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T035 [P] Documentation updates in backend/docs/
- [ ] T036 Code cleanup and refactoring across all tools
- [ ] T037 Performance optimization across all tools
- [X] T038 [P] Additional unit tests in backend/tests/
- [ ] T039 Security hardening for MCP tools
- [ ] T040 Run quickstart.md validation to ensure all tools work as expected
- [ ] T041 Verify all tools return structured output as per spec
- [ ] T042 Confirm stateless behavior: server restart does not lose data

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence