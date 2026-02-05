# Data Model: AI Chat Agent & Conversation System

## Entity Models

### Conversation
Represents a logical conversation thread between a user and the AI agent

```python
class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)  # Links to existing User model
    title: str = Field(max_length=255, nullable=False)  # Auto-generated from first message or user-provided
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_active: bool = Field(default=True, nullable=False)  # Whether conversation is ongoing

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")
```

**Validation Rules:**
- User ID must correspond to an existing user
- Title length must be between 1 and 255 characters
- Created and updated timestamps automatically managed
- Only active conversations are shown to users by default

### Message
Represents individual exchanges within a conversation

```python
class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id", nullable=False)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)  # Denormalized for query efficiency
    role: str = Field(max_length=20, nullable=False)  # "user", "assistant", "system", "tool"
    content: str = Field(nullable=False)  # The actual message content
    message_metadata: Optional[dict] = Field(default=None)  # Additional metadata (intent, tool_calls, etc.)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
    user: "User" = Relationship(back_populates="messages")
```

**Validation Rules:**
- Role must be one of: "user", "assistant", "system", "tool"
- Content length must be reasonable (not empty, not excessively long)
- Message must belong to a valid conversation
- User must be the owner of the conversation

### Intent (as part of Message metadata)
Classification of user input intent for task operations

```python
class IntentType(str, Enum):
    CREATE_TASK = "create_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    VIEW_TASKS = "view_tasks"
    SEARCH_TASKS = "search_tasks"
    MARK_COMPLETE = "mark_complete"
    MARK_INCOMPLETE = "mark_incomplete"
    UNKNOWN = "unknown"

class Intent:
    type: IntentType
    confidence: float  # 0.0 to 1.0
    parameters: dict   # Specific parameters for the intent
    extracted_entities: List[str]  # Named entities extracted from the message
```

## Database Schema Considerations

### Indexes
- `conversation.user_id`: For efficient user-specific queries
- `message.conversation_id`: For conversation history retrieval
- `message.created_at`: For chronological ordering
- `message.role`: For filtering message types

### Foreign Key Constraints
- `conversation.user_id` → `user.id`
- `message.conversation_id` → `conversation.id`
- `message.user_id` → `user.id` (denormalized for security checks)

## State Transitions

### Conversation States
- `active`: New conversation created, accepting messages
- `archived`: User has archived the conversation (via metadata flag)
- `deleted`: Soft deletion marker (via is_active flag)

### Message Immutability
- Messages are immutable once created
- Updates create new messages rather than modifying existing ones
- This preserves conversation history integrity

## Relationship Mapping

### User ↔ Conversation
- One-to-many: One user can have multiple conversations
- Foreign key: `conversation.user_id` references `user.id`
- Cascading: Deleting user archives all conversations (soft delete)

### Conversation ↔ Message
- One-to-many: One conversation contains multiple messages
- Foreign key: `message.conversation_id` references `conversation.id`
- Ordering: Messages ordered by `created_at` timestamp

## Security & Access Patterns

### Data Isolation
- All queries must filter by `user_id` to prevent cross-user access
- Middleware ensures user owns the conversation before access
- API endpoints validate user identity against resource ownership

### Query Patterns
- Retrieve user's conversations: `SELECT * FROM conversation WHERE user_id = ?`
- Retrieve conversation history: `SELECT * FROM message WHERE conversation_id = ? ORDER BY created_at ASC`
- Get recent conversations: `SELECT * FROM conversation WHERE user_id = ? AND is_active = TRUE ORDER BY updated_at DESC LIMIT 10`

## Migration Strategy

### New Tables
1. `conversation` table with indexes on `user_id` and `updated_at`
2. `message` table with indexes on `conversation_id` and `created_at`

### Permissions
- Only authenticated users can access their own conversations
- Read-only access to assistant/system messages
- Write access only to user messages