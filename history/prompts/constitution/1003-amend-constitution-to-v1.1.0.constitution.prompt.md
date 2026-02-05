---
id: 1003
title: Amend Constitution to v1.1.0
stage: constitution
date_iso: 2026-01-31
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 003-frontend-integration
user: claude
command: /sp.constitution
labels: ["constitution", "spec-driven-development", "ai-chatbot", "mcp"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - .specify/memory/constitution.md
tests_yaml: |
  - none
---

# Amend Constitution to v1.1.0

## User Command
```
/sp.constitution

Project: Todo Full-Stack Web Application – Phase-3 (AI Chatbot via MCP)

Purpose:
Add a stateless, AI-powered conversational layer that manages todos using natural language through MCP-based tools.

Core principles:
- Spec-driven, agentic development (no manual coding)
- Clear separation of concerns:
  - Spec-4 = Agent reasoning & conversation (Brain)
  - Spec-5 = MCP tools & task execution (Hands)
- Stateless server; database is the only memory
- Secure, user-isolated operations

Key standards:
- All AI behavior defined in specs
- Agent never accesses database directly
- All task actions executed only via MCP tools
- Conversation state persisted and rebuilt per request
- MCP tools are stateless and schema-driven
- Authenticated user enforced on every chat and tool call

Technology:
- OpenAI Agents SDK
- Official MCP SDK
- FastAPI + SQLModel
- Neon PostgreSQL
- Better Auth (JWT)

Constraints:
- Builds on existing backend and auth
- No advanced AI features beyond specs
- Hackathon-ready scope

Success criteria:
- Users manage todos via natural language
- Correct intent → MCP tool mapping
- Conversations persist across requests
- Stateless, secure, and reviewable architecture
```

## Response Summary
Updated the project constitution to version 1.1.0 to reflect the new Phase-3 focus on adding an AI-powered conversational layer using MCP-based tools. The update includes new core principles for MCP-based task execution, stateless architecture, secure user isolation, and intent-to-tool mapping. Technology standards were updated to include OpenAI Agents SDK and MCP SDK. Documentation standards now include Spec-4 for agent reasoning and Spec-5 for MCP tools. Success criteria were expanded to include natural language management of todos and proper AI integration.

## Outcome
The constitution has been successfully updated to guide the development of the AI Chatbot via MCP while maintaining the existing project principles and architecture.

## Evaluation
The updated constitution maintains backward compatibility while adding new principles specific to the AI/MCP implementation. All placeholders have been properly filled and the document follows the required format.