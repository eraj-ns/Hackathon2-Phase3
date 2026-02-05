<!--
SYNC IMPACT REPORT
Version change: 1.0.0 -> 1.1.0
List of modified principles: Updated to include AI Chatbot via MCP focus
Added sections: New core principles for Phase-3 (1.7, 1.8, 1.9, 1.10), Technology Standards section updated with MCP and OpenAI Agents
Removed sections: None
Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md, ⚠️ .specify/templates/commands/*.md may need updates for MCP tools
Follow-up TODOs: None
-->

# Project Constitution

**Project:** Todo Full-Stack Web Application – Phase-3 (AI Chatbot via MCP)
**Version:** 1.1.0
**Ratified:** 2026-01-20
**Last Amended:** 2026-01-31
**Status:** Active

## Preamble
This constitution defines the non-negotiable architectural, engineering, and operational principles for the Todo Full-Stack Web Application Phase-3. It serves as the primary source of truth for decision-making and ensures alignment with the Spec-Driven Development (SDD) methodology and the addition of a stateless, AI-powered conversational layer that manages todos using natural language through MCP-based tools.

## 1. Core Principles

### 1.1 Spec-Driven Development
**Rule:** No code shall be written without a preceding specification, plan, and task list.
**Rationale:** Ensures clarity, completeness, and alignment before implementation begin. The flow is strictly: Spec → Plan → Tasks → Implementation.

### 1.2 Backend-First Architecture
**Rule:** Backend logic and data correctness must be validated before UI integration.
**Rationale:** Prevents frontend-driven hacks and ensures the API is the source of truth. The frontend is merely a consumer of the API.

### 1.3 Security by Design
**Rule:** Security is foundational, not an afterthought. Strict user isolation and JWT-based authentication are mandatory.
**Rationale:** Protects user data and ensures compliance. Unauthorized access must be rejected at the API level regardless of UI state.

### 1.4 Deterministic, Reproducible Development
**Rule:** All development must be deterministic and reproducible using Claude Code.
**Rationale:** Reduces "it works on my machine" issues and ensures a clean, audit-friendly history of changes.

### 1.5 Clarity for Reviewers
**Rule:** All artifacts and code must be clear and accessible to hackathon reviewers and engineers.
**Rationale:** Facilitates evaluation and onboarding. Code and documentation should explain "why", not just "what".

### 1.6 Production-Aligned Engineering
**Rule:** Adopt standards suitable for production environments, even within the hackathon scope.
**Rationale:** Builds habits of quality and robustness. Includes proper error handling, logging, and environment configuration.

### 1.7 MCP-Based Task Execution
**Rule:** All AI-driven task actions must be executed only via MCP tools, never directly by the agent.
**Rationale:** Maintains clear separation of concerns between AI reasoning (brain) and execution (hands). The agent never accesses the database directly; all operations are performed through standardized MCP tools for auditability and security.

### 1.8 Stateless Architecture
**Rule:** The AI conversation layer must be stateless, with database serving as the only memory for conversation persistence.
**Rationale:** Enables horizontal scaling and resilience. Conversation state must be persisted and rebuilt per request to ensure consistent behavior across service restarts and deployments.

### 1.9 Secure User Isolation
**Rule:** All AI-driven operations must enforce authenticated user context on every chat and tool call, maintaining strict data isolation.
**Rationale:** Ensures that AI conversations and actions only affect the authenticated user's data. Every MCP tool call must validate user permissions before performing operations on behalf of the user.

### 1.10 Intent-to-Tool Mapping
**Rule:** AI must correctly map natural language intent to appropriate MCP tools with precise parameters and error handling.
**Rationale:** Ensures reliable execution of user requests. The AI must understand user intent and translate it to the correct tool with appropriate arguments, with proper fallback mechanisms for unrecognized intents.

## 2. Standards

### 2.1 Technology Standards
- **Frontend:** Next.js 16+ (App Router)
- **Backend:** Python FastAPI
- **ORM:** SQLModel
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** Better Auth (JWT-based)
- **AI Layer:** OpenAI Agents SDK
- **MCP Framework:** Official MCP SDK for tool orchestration
- **API Style:** RESTful with proper HTTP status codes

### 2.2 Security Standards
- **JWT Requirement:** Mandatory for all protected endpoints.
- **Verification:** Performed within FastAPI middleware/dependencies.
- **Secrets:** Shared secret configured via `BETTER_AUTH_SECRET`.
- **Identity:** Authenticated user identity derived ONLY from JWT claims.
- **Authorization:** Task ownership enforced on EVERY operation (Create, Read, Update, Delete).
- **Access Control:** Unauthorized requests return 401 (Unauthenticated) or 403 (Unauthorized) consistently.
- **AI Authentication:** Every AI-driven operation must validate user identity and permissions before execution.

### 2.3 Data Standards
- **Persistence:** All user data must be persistently stored in Neon PostgreSQL.
- **Isolation:** Strict zero-leakage policy between users. Users can only access their own tasks.
- **Ownership:** Explicit foreign key relationships between Users and Tasks.
- **Schema:** All schema changes must be spec-approved and migration-managed.
- **Conversation State:** AI conversation history stored separately with user isolation enforced.

### 2.4 Frontend Standards
- **Responsiveness:** UI must function on desktop and mobile viewports.
- **Auth Integration:** Routes gated by auth state; JWT automatically attached to API requests.
- **UX:** Clear error messages and loading states.
- **Validation:** Never bypass backend validation; frontend validation is for UX only.
- **Testing:** End-to-end integration must be validated.
- **AI Interface:** Clear chat interface for natural language todo management with appropriate loading states for AI processing.

### 2.5 Documentation Standards
- **Mandatory Order:**
  1. Spec-1: Backend Core & Data Layer
  2. Spec-2: Authentication & Security Integration
  3. Spec-3: Frontend Application & Full-Stack Integration
  4. Spec-4: Agent reasoning & conversation (Brain)
  5. Spec-5: MCP tools & task execution (Hands)
- **Traceability:** All features must trace back to a written spec.
- **MCP Tool Documentation:** Each MCP tool must be documented with parameters, return types, and error cases for AI consumption.

## 3. Constraints & Success Criteria

### 3.1 Constraints
- Must implement all basic Todo features (CRUD) via natural language interface.
- Multi-user support is mandatory with AI-powered conversations.
- No advanced AI features beyond defined specs (scope discipline for Hackathon-ready scope).
- AI layer must be stateless with conversation persistence in database.
- Agent never accesses database directly; all operations through MCP tools only.
- Hackathon-ready delivery timeline with clear separation between AI reasoning and task execution.
- All architectural decisions reviewable via specs and plans.

### 3.2 Success Criteria
- Fully functional multi-user Todo web application with AI conversational interface.
- Users can manage todos via natural language commands through the AI chatbot.
- Correct intent → MCP tool mapping for all supported operations.
- Backend, Auth, Frontend, and AI layers integrated correctly.
- Strict data isolation (Users access ONLY their own tasks) maintained through AI interactions.
- Conversations persist across requests with proper state management.
- All APIs protected and validated including AI endpoints.
- Project passes hackathon evaluation for correctness, security, and clarity of AI implementation.
- Stateless, secure, and reviewable architecture with clear audit trails for AI-driven actions.

## 4. Governance

### 4.1 Amendment Process
Changes to this constitution require a formal Spec modification and approval via the `sp.constitution` workflow.
- **Major Version:** Fundamental principle changes affecting core architecture or security model.
- **Minor Version:** New principles or standards (e.g., addition of AI/MCP components as in this update).
- **Patch Version:** Clarifications, wording fixes, and corrections.

### 4.2 Compliance
Every Pull Request and Feature Spec must strictly adhere to these principles. Deviations must be rejected or documented as approved exceptions in an ADR. Special attention must be paid to the separation between AI reasoning (Spec-4) and task execution (Spec-5) layers to maintain the stateless, secure architecture.
