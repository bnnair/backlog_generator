import json


backlog = '''
  {"product_backlog": {
    "acceptance_criteria_handling": {
      "external_standards_links": [
        {
          "link": "/docs/accessibility-crm-wcag-v1.5.6",
          "standard": "WCAG 2.1 AA",
          "summary": "Key inline criteria: All interactive elements keyboard accessible; color contrast ratio at least 4.5:1; text alternatives for non-text content; adaptable layouts; logical tab order; touch targets >= 44x44px; font resizing; no color-only info. Accessibility for error messages, custom widgets, and third-party integrations must be verified in English, German, and French. Testers must verify these explicitly in each relevant story. All user-facing epics/stories must reference and verify these requirements in their acceptance criteria. Critical test cases include: screen reader support, keyboard navigation, color contrast, focus states, and touch target size. For third-party or legacy integrations, accessibility is targeted as 'best effort' and must be phased according to risk/feasibility documented in the technical spike."
        },
        {
          "link": "/docs/audit-log-format-crm-v1.5.6",
          "standard": "Audit Log Format",
          "summary": "Audit entries must be JSON, containing: timestamp, user_id, role, operation, object_type, object_id, result, details (field changes, error info), ip_address, tenant_id. Entries are immutable, access-restricted, and all access is logged. Retention/rotation per compliance."
        },
        {
          "link": "/docs/notification-format-crm-v1.5.6",
          "standard": "Notification Format",
          "summary": "Notifications include: timestamp, recipient_user_id, channel, subject, body, language, priority, action_link. Must be actionable and localized; in-app supports HTML, email is plain text."
        }
      ],
      "po_update_instructions": "Product Owner (PO) must document and communicate interim targets or documentation updates in the team's Confluence planning board within 1 business day of spike outcome or identification of incomplete acceptance criteria. Updates must be tagged to the relevant user story and announced in the next daily scrum and sprint review. If only fallback/minimum criteria are met, the PO must document the reason, notify affected stakeholders, and ensure backlog is updated in the next sprint review. When technical spikes require a backlog update, documentation is mandatory; re-estimation of affected stories is required only if scope/timing changes result. For stories blocked by technical spikes, acceptance criteria must specify the impact of spike failure and guidance for partial delivery or holding stories."
    },
    "audit_logging_requirements": {
      "critical_behaviors_summary": "Entries must be immutable and stored securely. All access is audit-logged. Performance tested for 1,000 events/minute normal load, 2,000 events/minute peak load. Archiving/rotation at 1GB or 90 days, with admin notification at 90% capacity. Long-term storage must support scalable solutions for compliance retention periods.",
      "format_reference": "/docs/audit-log-format-crm-v1.5.6",
      "performance_note": "Audit logging must not introduce system bottlenecks. High-volume actions may cause log growth; see Reporting and Audit Logs epic for storage/rotation requirements. Infrastructure for high-throughput, tamper-proof logging must be validated with a technical spike and proof-of-concept implementation (see US-RAL-6), not just a document review, and tracked in architectural risk logs. System must handle peak loads of 2,000 events/minute with 99.9% availability.",
      "required_fields": ["timestamp", "user_id", "role", "operation", "object_type", "object_id", "result (success/error)", "details (field changes, error info, affected records)", "ip_address", "tenant_id"],
      "spike_unblock_criteria": "Spike US-RAL-6 is considered sufficient to unblock downstream stories if a working POC demonstrates append-only, immutable storage at required scale and documented in Confluence. If only partial feasibility is achieved, affected stories must be split for partial delivery and risk mitigation.",
      "technical_spike_dependency": "Downstream stories are blocked by the outcome of the technical spike US-RAL-6 and must be re-estimated and updated per POC findings. If technical feasibility is not achieved, backlog must be updated with mitigation stories."
    },
    "background_jobs_glossary": {
      "default_sla": "Background jobs (e.g., archiving, reporting, notifications) are expected to complete within 5 minutes under normal load conditions. If delayed or failed, user-facing notifications must indicate the status, estimated time, and offer next steps. For persistent failures (>3 retries or 15 minutes delay), escalate to system administrators with detailed error reports. Acceptance criteria for jobs must link to this glossary and explicitly define user-facing behaviors for delays/failures. Example: 'Export is taking longer than expected (ERR-JOB-002). Estimated completion: 10 minutes. You may close this window and will be notified when ready. If not received, please retry or contact support.'",
      "reference": "/docs/glossary-background-jobs-v1.5.7"
    },
    "created_date": "2024-07-04",
    "epic_prioritization_rationale": [
      {
        "epic_name": "Role-Based Access Control",
        "priority": 1,
        "rationale": "Protects sensitive data and enforces least-privilege access. RBAC is foundational for securing all entities before data onboarding."
      },
      {
        "epic_name": "User Profile & Account Settings",
        "priority": 2,
        "rationale": "Core for user context and onboarding; must precede any workflow or personalized feature."
      },
      {
        "epic_name": "Customer Profile Management",
        "priority": 3,
        "rationale": "Core to CRM value—enables all subsequent CRM workflows and data management. Positioned here as foundational for onboarding and value realization, but preceded by system setup and data compliance to ensure secure, compliant onboarding."
      },
      {
        "epic_name": "Contact Management",
        "priority": 4,
        "rationale": "Core CRM workflow for managing individual contacts and their interactions."
      },
      {
        "epic_name": "Opportunity Management",
        "priority": 5,
        "rationale": "Key CRM flow for managing and tracking sales opportunities."
      },
      {
        "epic_name": "Compliance, Data Retention & Privacy",
        "priority": 6,
        "rationale": "Regulatory and contractual obligations, including GDPR/DSR, must be met before bulk data onboarding. Reporting and Audit Logs are interdependent and must be completed for compliance go-live."
      },
      {
        "epic_name": "Reporting and Audit Logs",
        "priority": 7,
        "rationale": "Operational insight, monitoring, and compliance evidence. Prioritized with Compliance and Multi-Tenant Administration to support regulatory go-live."
      },
      {
        "epic_name": "Multi-Tenant Administration & Data Segregation",
        "priority": 8,
        "rationale": "Ensures strict separation and management of tenant data—critical before bulk operations or user onboarding."
      },
      {
        "epic_name": "Notifications",
        "priority": 9,
        "rationale": "System notification infrastructure is critical for compliance, workflow awareness, and is a dependency for core workflows and automation."
      },
      {
        "epic_name": "System Administration & Maintenance",
        "priority": 10,
        "rationale": "Operational continuity and resilience (backup/restore/DR) are critical ahead of reporting and tickets."
      },
      {
        "epic_name": "Bulk Operations & Imports",
        "priority": 11,
        "rationale": "Efficient onboarding and mass-updates are gating needs for any go-live, but must follow RBAC, Compliance, and Tenant structures."
      },
      {
        "epic_name": "Ticketing System",
        "priority": 12,
        "rationale": "Core for customer support, dependent on foundational CRM data."
      },
      {
        "epic_name": "Dashboard & Custom Reporting",
        "priority": 13,
        "rationale": "Empowers end users (sales, CS) to make data-driven decisions with actionable dashboards and custom reports."
      },
      {
        "epic_name": "Workflow Automation & Rules",
        "priority": 14,
        "rationale": "Automates repetitive actions for efficiency and compliance, often a key differentiator in CRM."
      },
      {
        "epic_name": "Usability and Guidance",
        "priority": 15,
        "rationale": "Enhances adoption and reduces onboarding friction."
      },
      {
        "epic_name": "Mobile Support",
        "priority": 16,
        "rationale": "Key for field and external access; core mobile flows prioritized. If mobile is a primary channel, core workflows must be delivered with web parity. Priority may be raised if customer confirms mobile as business-critical."
      },
      {
        "epic_name": "Integrations & API Requirements",
        "priority": 17,
        "rationale": "Extends system value to partners; minimal API contract definition and security now prioritized earlier for extensibility."
      },
      {
        "epic_name": "Backlog Transparency & Scope",
        "priority": 18,
        "rationale": "Ensures shared understanding and quality of delivery."
      },
      {
        "epic_name": "Out-of-Scope and Deferred",
        "priority": 19,
        "rationale": "To prevent scope creep and clarify release boundaries."
      }
    ],
    "epics": [
      {
        "epic_name": "Role-Based Access Control",
        "rationale": "Protects sensitive data and enforces least-privilege access. RBAC is foundational for securing all entities before data onboarding.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API allows admin to view, assign, and change roles for users; all role changes logged to audit log with user, admin, timestamp, and operation.", "Role changes trigger user notification with sample: 'Your role has been updated to Manager. For questions, contact your administrator. (USR-RBAC-002)'", "If an admin attempts to assign a role they themselves do not hold, the system denies with localized message: 'You do not have permission to assign this role. (USR-RBAC-003)'", "All UI and messages are localized; fallback to English with standardized error code.", "Accessibility: Role management UI meets WCAG 2.1 AA (keyboard navigation, color contrast ratio at least 4.5:1, screen reader support, logical tab order, touch targets >= 44x44px). Explicit test instructions: tab order: search > user list > role dropdown > save > cancel."],
            "definition_of_done": ["Role assignment, audit, notification, localization, error code, and accessibility verified."],
            "depends_on": [],
            "description": "Allow admins to assign, change, and revoke user roles (admin, manager, user, read-only) with audit logging, localization, and accessible UI.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-RBAC-1",
            "test_cases": ["TC-RBAC-1-01: Change user roles, check audit log.", "TC-RBAC-1-02: Attempt unauthorized role change, verify error and code.", "TC-RBAC-1-03: Check language fallback and notification.", "TC-RBAC-1-04: Accessibility—tab order and color contrast tested."],
            "title": "User Role Management",
            "user_story": "As an admin, I want to assign, change, or revoke user roles so that users have appropriate permissions."
          },
          {
            "acceptance_criteria": ["UI/API allows admin to invite user (email sent with activation link, sample: 'Click here to activate your CRM account (USR-INV-001)').", "Deactivation/reactivation triggers notification: 'Your account has been deactivated; contact your admin for assistance. (USR-ACC-004)'", "Admin can trigger password reset; user receives secure, localized instructions.", "Edge cases: Invitation to existing email returns error: 'User already exists (USR-INV-002)'.", "All actions audited; audit log includes admin, target user, IP, time, and action.", "Accessibility: All flows meet WCAG 2.1 AA. Sample: Focus moves automatically to first input field; error states have sufficient contrast (>=4.5:1)."],
            "definition_of_done": ["Invite, deactivate/reactivate, password reset, notification, audit, localization, error handling, accessibility complete."],
            "depends_on": [{"blocking": true, "story_id": "US-RBAC-1"}],
            "description": "Admins can invite new users, deactivate/reactivate accounts, and initiate password resets, with audit, localization, notification, and accessible UI.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 2,
            "story_id": "US-RBAC-2",
            "test_cases": ["TC-RBAC-2-01: Invite user, check email and audit log.", "TC-RBAC-2-02: Deactivate/reactivate, verify notification and logging.", "TC-RBAC-2-03: Duplicate invite; verify error and code.", "TC-RBAC-2-04: Accessibility—test input focus and error contrast."],
            "title": "User Invitation and Account Lifecycle",
            "user_story": "As an admin, I want to invite new users, manage their activation status, and reset passwords securely."
          }
        ]
      },
      {
        "epic_name": "User Profile & Account Settings",
        "rationale": "Core for user context and onboarding; must precede any workflow or personalized feature.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API allows users to view and edit their profile information with proper validation.", "All profile data supports Unicode/RTL scripts and multi-language display.", "Changes to profile information are audit-logged with timestamp and user context.", "All UI and error messages are localized; fallback to English with standardized error code.", "Accessibility: Profile management UI meets WCAG 2.1 AA with explicit test cases for keyboard navigation, screen reader support, color contrast (>=4.5:1), and touch targets (>=44x44px).", "Time zone and language preferences are saved and applied consistently across the application."],
            "definition_of_done": ["Profile management, Unicode/RTL support, audit logging, localization, accessibility, and preference handling verified."],
            "depends_on": [{"blocking": true, "story_id": "US-RBAC-1"}],
            "description": "Allow users to view and edit their own profile information with localization, accessibility, and audit logging.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-UP-1",
            "test_cases": ["TC-UP-1-01: Edit profile with multi-language input, verify saving and display.", "TC-UP-1-02: Change time zone/language preferences, verify application-wide consistency.", "TC-UP-1-03: Accessibility testing for keyboard navigation and screen reader.", "TC-UP-1-04: Audit log verification for profile changes.", "TC-UP-1-05: Localization fallback testing."],
            "title": "User Profile Management",
            "user_story": "As a user, I want to view and edit my profile information including name, email, time zone, and language preferences."
          },
          {
            "acceptance_criteria": ["UI/API allows users to configure notification preferences, display options, and accessibility settings.", "All preference changes are saved per user and applied consistently across sessions.", "Settings UI meets WCAG 2.1 AA with proper keyboard navigation, screen reader support, color contrast (>=4.5:1), and touch targets (>=44x44px).", "All labels and messages are localized; fallback to English with standardized error code.", "Preference changes are audit-logged for security-sensitive settings.", "Accessibility settings (high contrast, font size) are immediately applied in the UI."],
            "definition_of_done": ["Preference management, accessibility features, localization, audit logging, and consistency verified."],
            "depends_on": [{"blocking": true, "story_id": "US-UP-1"}],
            "description": "Allow users to configure application preferences including notification settings, display options, and accessibility features.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 2,
            "story_id": "US-UP-2",
            "test_cases": ["TC-UP-2-01: Configure various user preferences, verify persistence.", "TC-UP-2-02: Test accessibility settings application in real-time.", "TC-UP-2-03: Accessibility testing for settings UI.", "TC-UP-2-04: Localization fallback verification.", "TC-UP-2-05: Audit log review for sensitive setting changes."],
            "title": "User Preferences and Settings",
            "user_story": "As a user, I want to configure my application preferences to personalize my experience and meet my accessibility needs."
          },
          {
            "acceptance_criteria": ["UI/API allows users to initiate self-service password reset with email verification.", "Password reset emails include secure, time-limited links with clear instructions.", "All password reset operations are audit-logged with timestamp and user context.", "Error handling for invalid or expired reset links with localized messages and standardized error codes.", "Accessibility: Password reset UI meets WCAG 2.1 AA with proper keyboard navigation, screen reader support, and color contrast (>=4.5:1).", "Rate limiting implemented to prevent abuse of password reset functionality."],
            "definition_of_done": ["Self-service password reset, email verification, audit logging, error handling, localization, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-UP-1"}],
            "description": "Allow users to reset their own passwords securely through self-service functionality with proper audit trails and security controls.",
            "estimate": "S",
            "priority": "must have",
            "priority_within_epic": 3,
            "story_id": "US-UP-3",
            "test_cases": ["TC-UP-3-01: Initiate password reset, verify email delivery and link functionality.", "TC-UP-3-02: Test error handling for invalid/expired reset links.", "TC-UP-3-03: Accessibility testing for password reset UI.", "TC-UP-3-04: Audit log verification for reset operations.", "TC-UP-3-05: Rate limiting testing to prevent abuse."],
            "title": "Self-Service Password Reset",
            "user_story": "As a user, I want to reset my password securely through self-service functionality when I forget my credentials."
          }
        ]
      },
      {
        "epic_name": "Customer Profile Management",
        "rationale": "Core to CRM value—enables all subsequent CRM workflows and data management.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API supports add/edit/view/delete of customer profiles with validations for required fields (sample: 'Customer name is required (CUST-VAL-001)').", "All profile data supports Unicode/RTL scripts and multi-language search; test with Arabic and French names.", "Error messages localized; fallback to English with code if missing.", "All changes and deletions logged in audit log (user, action, before/after, timestamp).", "Accessibility: WCAG 2.1 AA. Explicit test: Tab order: search > add > customer fields > save > cancel. Color contrast >= 4.5:1, touch targets >=44x44px.", "If deletion blocked by referential integrity, show: 'Cannot delete customer with active opportunities (CUST-DEL-002)'."],
            "definition_of_done": ["CRUD, Unicode/RTL, error handling, audit, localization, accessibility, and referential integrity verified."],
            "depends_on": [{"blocking": true, "story_id": "US-RBAC-1"}],
            "description": "Allow users to create, view, edit, and delete customer profiles with full localization, audit, and accessibility.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-CPM-1",
            "test_cases": ["TC-CPM-1-01: Create/edit/delete with multi-language input.", "TC-CPM-1-02: Attempt delete with dependencies.", "TC-CPM-1-03: Accessibility—tab and contrast check.", "TC-CPM-1-04: Audit log review."],
            "title": "Customer CRUD Operations",
            "user_story": "As a CRM user, I want to manage customer profiles (create, update, view, delete) with all supported fields and validations."
          }
        ]
      },
      {
        "epic_name": "Contact Management",
        "rationale": "Core CRM workflow for managing individual contacts and their interactions.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API allows add/edit/view/delete of contacts; required fields validated (sample: 'Email is required (CONT-VAL-002)').", "Contacts are linked to customers; error on orphaned contact: 'Contact must be linked to a customer (CONT-VAL-005)'.", "Unicode/RTL supported for names, notes; multi-language search available where feasible.", "All changes and deletions audited.", "Localized error and success messages; fallback to English and display code.", "Accessibility: WCAG 2.1 AA, with test: Logical tab order, minimum touch target 44x44px, color contrast test for labels and errors (>=4.5:1)."],
            "definition_of_done": ["CRUD, linkage, localization, audit, accessibility, and error coverage complete."],
            "depends_on": [{"blocking": true, "story_id": "US-CPM-1"}],
            "description": "Enable users to create, edit, view, and delete contacts linked to customers, with localization, audit, and accessibility.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-CONT-1",
            "test_cases": ["TC-CONT-1-01: Add/edit/delete with multi-language data.", "TC-CONT-1-02: Attempt to save orphaned contact.", "TC-CONT-1-03: Accessibility—focus order and touch target.", "TC-CONT-1-04: Audit log entries."],
            "title": "Contact CRUD Operations",
            "user_story": "As a CRM user, I want to manage contacts (add, edit, delete) linked to customer profiles with validations and audit trails."
          }
        ]
      },
      {
        "epic_name": "Opportunity Management",
        "rationale": "Key CRM flow for managing and tracking sales opportunities.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API for add/edit/view/close of opportunities; required fields: customer, stage, amount (sample: 'Amount must be a positive number (OPP-VAL-003)').", "Opportunities must be linked to customer; error if not: 'Link a customer before saving (OPP-VAL-004)'.", "Audit log records all stage/owner/amount changes.", "All messages and field labels localized; fallback to English with code.", "Accessibility: WCAG 2.1 AA. Test: Screen reader reads field labels and error messages; keyboard access to each field and save/cancel; color contrast >=4.5:1.", "Edge case: Opportunity cannot be closed if mandatory fields missing; UI feedback: 'Complete all required fields before closing (OPP-CLOSE-002)'."],
            "definition_of_done": ["CRUD, linkage, localization, audit, accessibility, and required field error handling complete."],
            "depends_on": [{"blocking": true, "story_id": "US-CPM-1"}, {"blocking": true, "story_id": "US-CONT-1"}],
            "description": "Enable users to create, edit, view, and close/delete opportunities with customer/contact linkage, localization, audit, and accessibility.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-OPP-1",
            "test_cases": ["TC-OPP-1-01: CRUD with multi-language and Unicode data.", "TC-OPP-1-02: Attempt to save without customer.", "TC-OPP-1-03: Accessibility—screen reader and keyboard.", "TC-OPP-1-04: Audit verification."],
            "title": "Opportunity CRUD Operations",
            "user_story": "As a sales user, I want to manage sales opportunities linked to customers and contacts, set amounts and stages, and track changes."
          }
        ]
      },
      {
        "epic_name": "Compliance, Data Retention & Privacy",
        "rationale": "Regulatory and contractual obligations, including GDPR/DSR, must be met before bulk data onboarding.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API allows configuration of retention periods (in days) for each entity type.", "Policy changes are audit-logged with admin details and timestamp.", "All UI and messages are localized; fallback to English with standardized error code.", "Accessibility: Policy configuration UI meets WCAG 2.1 AA with keyboard navigation, screen reader support, color contrast (>=4.5:1), and touch targets (>=44x44px).", "Validation prevents conflicting or non-compliant retention periods with appropriate error messages."],
            "definition_of_done": ["Retention policy configuration, audit logging, localization, accessibility, and validation verified."],
            "depends_on": [{"blocking": true, "story_id": "US-RBAC-1"}],
            "description": "Allow admins to configure data retention policies for different entity types with audit logging and localization.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-COMP-1",
            "test_cases": ["TC-COMP-1-01: Configure retention policies for different entities.", "TC-COMP-1-02: Attempt invalid configuration, verify error handling.", "TC-COMP-1-03: Accessibility testing for policy UI.", "TC-COMP-1-04: Audit log verification for policy changes.", "TC-COMP-1-05: Localization fallback testing."],
            "title": "Data Retention Policy Configuration",
            "user_story": "As a compliance admin, I want to configure data retention policies for customers, contacts, opportunities, and tickets to meet regulatory requirements."
          },
          {
            "acceptance_criteria": ["Background job runs daily to identify and process data exceeding retention periods.", "Deletion/anonymization operations are fully audit-logged with system user context.", "Admin notifications sent for bulk deletion operations with summary reports.", "Process handles partial failures gracefully with retry logic and error reporting.", "All notification messages are localized; fallback to English with standardized error code.", "Performance tested to handle large data volumes without system impact."],
            "definition_of_done": ["Automated data deletion, audit logging, notification, error handling, and performance verified."],
            "depends_on": [{"blocking": true, "story_id": "US-COMP-1"}],
            "description": "Implement automated data deletion and anonymization based on configured retention policies with proper audit trails.",
            "estimate": "L",
            "priority": "must have",
            "priority_within_epic": 2,
            "story_id": "US-COMP-2",
            "test_cases": ["TC-COMP-2-01: Verify automated deletion based on retention policies.", "TC-COMP-2-02: Test partial failure handling and retry logic.", "TC-COMP-2-03: Audit log verification for deletion operations.", "TC-COMP-2-04: Notification testing for admin alerts.", "TC-COMP-2-05: Performance testing with large data sets."],
            "title": "Data Deletion and Anonymization",
            "user_story": "As a system, I want to automatically delete or anonymize data based on retention policies to maintain compliance."
          },
          {
            "acceptance_criteria": ["UI/API allows users to submit data access requests with authentication verification.", "System generates comprehensive data export including: profile data, activity logs, connected entities, and system interactions.", "Exports provided in standardized formats (JSON, CSV) with proper data structure and metadata.", "All access requests are audit-logged with timestamp and user context.", "Background job handles export generation with SLA compliance (within 30 days per GDPR).", "Localized notifications for request submission, processing status, and completion.", "Accessibility: Request UI meets WCAG 2.1 AA with proper navigation and screen reader support."],
            "definition_of_done": ["Data access requests, export generation, audit logging, notification, localization, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-UP-1"}],
            "description": "Implement GDPR Right to Access functionality allowing users to request and receive their personal data in portable format.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 3,
            "story_id": "US-COMP-3",
            "test_cases": ["TC-COMP-3-01: Submit data access request, verify export completeness.", "TC-COMP-3-02: Test export format validity and machine-readability.", "TC-COMP-3-03: Verify audit logging for access requests.", "TC-COMP-3-04: Test notification localization and timing.", "TC-COMP-3-05: Accessibility testing for request interface."],
            "title": "GDPR Right to Access and Data Portability",
            "user_story": "As a user, I want to request and receive a copy of my personal data in a machine-readable format to exercise my GDPR Right to Access."
          },
          {
            "acceptance_criteria": ["UI/API allows authenticated users to submit erasure requests with proper verification.", "System performs complete data deletion across all entities: profile data, activity logs, connected records, and system interactions.", "Erasure process includes verification steps and confirmation of completion.", "All erasure requests are audit-logged with comprehensive before/after records.", "Background job handles erasure operations with proper error handling and retry logic.", "Localized notifications for request submission, processing status, and completion.", "Accessibility: Erasure request UI meets WCAG 2.1 AA requirements."],
            "definition_of_done": ["Data erasure functionality, audit logging, notification, error handling, localization, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-COMP-2"}],
            "description": "Implement GDPR Right to Be Forgotten functionality allowing users to request complete erasure of their personal data.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 4,
            "story_id": "US-COMP-4",
            "test_cases": ["TC-COMP-4-01: Submit erasure request, verify complete data removal.", "TC-COMP-4-02: Test audit logging completeness for erasure operations.", "TC-COMP-4-03: Verify notification localization and delivery.", "TC-COMP-4-04: Test error handling for partial erasure failures.", "TC-COMP-4-05: Accessibility testing for erasure interface."],
            "title": "GDPR Right to Be Forgotten",
            "user_story": "As a user, I want to request complete erasure of my personal data to exercise my GDPR Right to Be Forgotten."
          },
          {
            "acceptance_criteria": ["UI/API allows users to export their personal data in multiple formats (JSON, CSV, PDF) from the data access interface.", "Export functionality includes selection of specific data categories and date ranges.", "All export operations are audit-logged with user context and export parameters.", "Background job handles large export operations with proper SLA compliance.", "Localized notifications for export completion with download links.", "Accessibility: Export interface meets WCAG 2.1 AA with proper navigation and screen reader support."],
            "definition_of_done": ["Data export functionality, format options, audit logging, notification, localization, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-COMP-3"}],
            "description": "Implement data export functionality for GDPR Right to Access allowing users to download their personal data in multiple formats.",
            "estimate": "S",
            "priority": "must have",
            "priority_within_epic": 3.1,
            "story_id": "US-COMP-3a",
            "test_cases": ["TC-COMP-3a-01: Export personal data in multiple formats, verify content completeness.", "TC-COMP-3a-02: Test export with specific category and date range selections.", "TC-COMP-3a-03: Verify audit logging for export operations.", "TC-COMP-3a-04: Test notification delivery for export completion.", "TC-COMP-3a-05: Accessibility testing for export interface."],
            "title": "GDPR Data Export Functionality",
            "user_story": "As a user, I want to export my personal data in multiple formats (JSON, CSV, PDF) to facilitate data portability and analysis."
          }
        ]
      },
      {
        "epic_name": "Reporting and Audit Logs",
        "rationale": "Operational insight, monitoring, and compliance evidence.",
        "user_stories": [
          {
            "acceptance_criteria": ["POC implementation demonstrates append-only, immutable storage using recommended technology stack (e.g., Kafka with immutable storage backend or blockchain-based logging) at scale of 2,000 events/minute peak load with latency <100ms average, <500ms p95.", "Performance testing results documented including throughput, latency, and resource utilization under various load conditions with specific technology recommendations.", "Feasibility assessment for tamper-proof storage, high-availability requirements, and scalable long-term retention solutions with implementation approach documentation.", "Evaluation of storage scalability options for compliance retention periods (3-7 years) with cost analysis.", "Risk assessment completed for partial feasibility scenarios including mitigation strategies with specific technology constraints documented.", "Infrastructure validation plan documented including production deployment requirements, monitoring needs, and specific measurable outcomes with technology stack specifications.", "Recommendations documented for implementation approach and required infrastructure with cost analysis and technology selection criteria.", "Spike outcome documented in Confluence with clear go/no-go criteria: POC must demonstrate 2,000 events/minute throughput with <500ms p95 latency and immutable storage to unblock downstream stories using validated technology approach."],
            "definition_of_done": ["POC implemented with specific technology validation, performance validated under peak loads with latency metrics, feasibility assessed with implementation approach, storage scalability evaluated, infrastructure validation plan documented, documentation complete, and recommendations provided."],
            "depends_on": [],
            "description": "Technical spike to validate high-throughput, immutable audit log infrastructure capable of handling 2,000 events/minute peak load with scalable storage and performance metrics, including specific technology stack evaluation and implementation recommendations.",
            "estimate": "L",
            "priority": "must have",
            "priority_within_epic": 0,
            "story_id": "US-RAL-6",
            "test_cases": ["TC-RAL-6-01: Performance testing at required scale including peak loads with latency measurements using recommended technology stack.", "TC-RAL-6-02: Immutability validation testing under various attack scenarios with specific technology implementation.", "TC-RAL-6-03: High-availability and disaster recovery scenario testing with technology recommendations.", "TC-RAL-6-04: Storage scalability assessment for long-term retention with technology evaluation.", "TC-RAL-6-05: Infrastructure validation plan review for production readiness with technology specifications.", "TC-RAL-6-06: Documentation review for completeness and actionable recommendations including technology selection."],
            "title": "Audit Log Infrastructure Technical Spike",
            "user_story": "As an architect, I want to validate the technical feasibility of high-performance audit log infrastructure to support compliance requirements including peak loads and long-term storage, with specific technology stack evaluation and implementation recommendations."
          },
          {
            "acceptance_criteria": ["UI/API supports filters for user, date range, action, entity.", "Exports available in CSV and JSON; all fields per audit log spec.", "Access restricted to authorized roles; unauthorized access denied with localized error: 'You do not have permission to access audit logs (AUDIT-VAL-003)'.", "Localization: All UI and error messages localized; fallback to English with code if missing.", "Audit log includes export/search events.", "Accessibility: WCAG 2.1 AA. Test: Tab order, color contrast (>=4.5:1), screen reader reads filter labels."],
            "definition_of_done": ["Search/export, access control, localization, audit, accessibility coverage complete."],
            "depends_on": [{"blocking": true, "story_id": "US-RAL-6"}],
            "description": "Allow authorized users to search and export audit logs by entity, date, user, and action, with localization and accessibility.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-RAL-1",
            "test_cases": ["TC-RAL-1-01: Filter/export by date/user/action.", "TC-RAL-1-02: Attempt unauthorized access.", "TC-RAL-1-03: Accessibility—filter controls.", "TC-RAL-1-04: Audit log of export/search events."],
            "title": "Audit Log Search and Export",
            "user_story": "As a compliance or admin user, I want to search and export audit logs for specific users, dates, and actions in CSV/JSON format."
          },
          {
            "acceptance_criteria": ["UI/API supports audit log storage configuration for archiving at 1GB or 90 days thresholds.", "Admin notifications sent when storage reaches 90% capacity with detailed usage reports.", "Rotation policies implemented with secure archival procedures.", "Long-term storage solutions validated for compliance retention periods (3-7 years).", "All configuration changes audit-logged with admin details.", "Localized notifications and error messages; fallback to English with standardized error code.", "Accessibility: Storage management UI meets WCAG 2.1 AA with keyboard navigation and screen reader support."],
            "definition_of_done": ["Storage configuration, archiving/rotation, notification, audit logging, localization, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-RAL-6"}],
            "description": "Implement audit log storage management with archiving, rotation, and capacity notifications as specified in critical behaviors summary.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1.5,
            "story_id": "US-RAL-1b",
            "test_cases": ["TC-RAL-1b-01: Configure storage thresholds and verify archiving triggers.", "TC-RAL-1b-02: Test admin notifications at 90% capacity.", "TC-RAL-1b-03: Verify rotation policies and secure archival.", "TC-RAL-1b-04: Accessibility testing for storage management UI.", "TC-RAL-1b-05: Audit log verification for configuration changes."],
            "title": "Audit Log Storage Management and Rotation",
            "user_story": "As a system administrator, I want to configure audit log storage policies with archiving, rotation, and capacity notifications to maintain system performance."
          },
          {
            "acceptance_criteria": ["Reports available by entity with filters (e.g., date, status, owner); export to CSV, XLSX, PDF, JSON.", "Reports show Unicode/RTL and data formatted per locale.", "All labels/messages localized; fallback to English with code.", "Accessibility: All filters and tables meet WCAG 2.1 AA (test: focus moves logically through filters > table > export; color contrast >=4.5:1).", "Audit log captures report views/exports."],
            "definition_of_done": ["Standard report, filters, export including JSON format, localization, audit, accessibility tested."],
            "depends_on": [{"blocking": true, "story_id": "US-CPM-1"}],
            "description": "Provide standard reports for customer, contact, opportunity, and ticket data with filtering, export including JSON format, localization, and accessibility.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 2,
            "story_id": "US-RAL-2",
            "test_cases": ["TC-RAL-2-01: Generate/export report for each entity including JSON format.", "TC-RAL-2-02: Filter, check locale/date/currency.", "TC-RAL-2-03: Accessibility—focus and contrast.", "TC-RAL-2-04: Audit log check."],
            "title": "Standard CRM Reporting (Entities)",
            "user_story": "As a CRM user, I want pre-built reports for customers, contacts, opportunities, and tickets, filterable and exportable in multiple formats including JSON."
          },
          {
            "acceptance_criteria": ["UI/API supports field selection, filter definition, and grouping.", "Exports available in CSV, XLSX, PDF, JSON; all data retains Unicode/RTL and locale formatting.", "All UI and error messages localized; fallback to English with code.", "Audit logs capture custom report definitions and exports.", "Accessibility: WCAG 2.1 AA (test: keyboard access to field selection, logical tab order, color contrast >=4.5:1 for dynamic fields)."],
            "definition_of_done": ["Custom report builder, export including JSON format, localization, audit, accessibility coverage complete."],
            "depends_on": [{"blocking": true, "story_id": "US-RAL-2"}],
            "description": "Enable users to build custom reports with fields, filters, and grouping, supporting localization, accessibility, export including JSON format, and audit.",
            "estimate": "L",
            "priority": "should have",
            "priority_within_epic": 3,
            "story_id": "US-RAL-3",
            "test_cases": ["TC-RAL-3-01: Build/export custom report with multi-language fields including JSON format.", "TC-RAL-3-02: Accessibility—dynamic field controls.", "TC-RAL-3-03: Localization fallback.", "TC-RAL-3-04: Audit log entries."],
            "title": "Custom Report Builder",
            "user_story": "As a power user, I want to build custom reports with selected fields, filters, and groups, and export results in multiple formats including JSON."
          },
          {
            "acceptance_criteria": ["Chart types: bar, line, pie available; user selects format.", "Charts use accessible color palettes (colorblind-safe, contrast >= 4.5:1).", "All labels and tooltips localized.", "Screen reader announces chart type, title, and summary data.", "Export charts to PDF, PNG.", "Audit logs capture chart views/exports."],
            "definition_of_done": ["Charts, localization, accessible color, export, audit, screen reader tested."],
            "depends_on": [{"blocking": true, "story_id": "US-RAL-3"}],
            "description": "Support charting and data visualization within custom reports, with accessible color schemes and localization.",
            "estimate": "M",
            "priority": "should have",
            "priority_within_epic": 3.1,
            "story_id": "US-RAL-3a",
            "test_cases": ["TC-RAL-3a-01: Generate each chart type with multi-language labels.", "TC-RAL-3a-02: Accessibility—color contrast and screen reader.", "TC-RAL-3a-03: Export chart to image/PDF.", "TC-RAL-3a-04: Audit log review."],
            "title": "Split: Custom Report Visualization",
            "user_story": "As a CRM user, I want to visualize report results as charts (bar, line, pie) with accessible color schemes and labels."
          }
        ]
      },
      {
        "epic_name": "Multi-Tenant Administration & Data Segregation",
        "rationale": "Ensures strict separation and management of tenant data—critical before bulk operations or user onboarding.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API for creating, configuring, and managing tenants with proper validation.", "All tenant data is strictly segregated with no cross-tenant data leakage.", "Tenant management operations are audit-logged with admin details and timestamp.", "All UI and error messages are localized; fallback to English with standardized error code.", "Accessibility: Tenant management UI meets WCAG 2.1 AA with keyboard navigation, screen reader support, color contrast (>=4.5:1), and touch targets (>=44x44px).", "Validation prevents conflicting tenant configurations with appropriate error messages."],
            "definition_of_done": ["Tenant management, data segregation, audit logging, localization, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-RBAC-1"}],
            "description": "Allow system admins to create, configure, and manage tenants with proper data segregation, audit logging, and localization.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-MT-1",
            "test_cases": ["TC-MT-1-01: Create and configure tenants with various settings.", "TC-MT-1-02: Verify data segregation between tenants.", "TC-MT-1-03: Accessibility testing for tenant management UI.", "TC-MT-1-04: Audit log verification for tenant operations.", "TC-MT-1-05: Localization fallback testing."],
            "title": "Tenant Management and Configuration",
            "user_story": "As a system administrator, I want to manage tenant configurations and ensure strict data segregation between tenants."
          },
          {
            "acceptance_criteria": ["UI/API allows tenant admins to configure overrides for allowed settings.", "Access controls prevent tenant admins from modifying restricted system settings.", "Configuration changes are audit-logged with tenant admin details and timestamp.", "All UI and error messages are localized; fallback to English with standardized error code.", "Accessibility: Configuration UI meets WCAG 2.1 AA with proper navigation and screen reader support.", "Validation ensures tenant configurations don't violate system constraints."],
            "definition_of_done": ["Tenant configuration overrides, access controls, audit logging, localization, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-MT-1"}],
            "description": "Allow tenant admins to override system-wide configurations for their specific tenant with proper access controls.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 2,
            "story_id": "US-MT-2",
            "test_cases": ["TC-MT-2-01: Configure tenant-specific overrides for allowed settings.", "TC-MT-2-02: Attempt to modify restricted settings, verify access denial.", "TC-MT-2-03: Accessibility testing for configuration UI.", "TC-MT-2-04: Audit log verification for configuration changes.", "TC-MT-2-05: Localization fallback testing."],
            "title": "Tenant-Specific Configuration Overrides",
            "user_story": "As a tenant administrator, I want to configure tenant-specific settings that override system defaults where allowed."
          }
        ]
      },
      {
        "epic_name": "Notifications",
        "rationale": "System notification infrastructure is critical for compliance, workflow awareness, and is a dependency for core workflows and automation.",
        "user_stories": [
          {
            "acceptance_criteria": ["Background job infrastructure implemented for notification delivery with SLA: 95% of notifications delivered within 30 seconds, 99% within 5 minutes.", "Support for email, in-app, and push notification channels implemented with proper error handling and retry logic.", "Notification delivery status tracked and available for monitoring.", "All notification operations are audit-logged with appropriate details including delivery status and timestamps.", "Performance tested to handle expected notification volumes (1,000 notifications/minute) without system impact.", "Localization fallback handling implemented with standardized error codes for delivery failures."],
            "definition_of_done": ["Notification delivery infrastructure, multi-channel support, SLA compliance, performance, audit logging, and error handling verified."],
            "depends_on": [],
            "description": "Implement core notification delivery infrastructure with background job processing, multi-channel support, and performance requirements.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-NOT-1a",
            "test_cases": ["TC-NOT-1a-01: Test notification delivery performance under load (1,000 notifications/minute).", "TC-NOT-1a-02: Verify SLA compliance for delivery timing.", "TC-NOT-1a-03: Test error handling and retry logic for failed deliveries.", "TC-NOT-1a-04: Audit log verification for notification operations.", "TC-NOT-1a-05: Performance testing with peak notification volumes."],
            "title": "Notification Delivery Infrastructure",
            "user_story": "As a system, I want to reliably deliver notifications through multiple channels with performance SLAs and proper error handling."
          },
          {
            "acceptance_criteria": ["Support for email, in-app, and push notification channels implemented.", "All notifications are localized per user preference; fallback to English with standardized error code.", "Notification failures are handled gracefully with retry logic and error reporting.", "All notification operations are audit-logged with appropriate details.", "Accessibility: Notification UI meets WCAG 2.1 AA across all channels.", "Performance tested to handle expected notification volumes without system impact."],
            "definition_of_done": ["Notification infrastructure, multi-channel support, localization, error handling, audit logging, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-NOT-1a"}],
            "description": "Implement core notification infrastructure with support for multiple channels, localization, and fallback handling.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-NOT-1",
            "test_cases": ["TC-NOT-1-01: Send notifications through all supported channels.", "TC-NOT-1-02: Test localization fallback for missing translations.", "TC-NOT-1-03: Simulate notification failures, verify retry logic.", "TC-NOT-1-04: Accessibility testing for notification UI.", "TC-NOT-1-05: Performance testing with high notification volumes."],
            "title": "Notification System Foundation",
            "user_story": "As a system, I want to send notifications through multiple channels (email, in-app, push) with proper localization and error handling."
          },
          {
            "acceptance_criteria": ["UI/API for creating, editing, and previewing notification templates.", "Support for template variables and conditional logic in notifications.", "All template management operations are audit-logged with admin details.", "Template UI supports localization for all supported languages.", "Accessibility: Template management UI meets WCAG 2.1 AA with keyboard navigation and screen reader support.", "Preview functionality shows exactly how notifications will appear to users."],
            "definition_of_done": ["Notification template management, variable support, preview functionality, audit logging, localization, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-NOT-1"}],
            "description": "Allow admins to manage notification templates with support for variables, localization, and preview functionality.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 2,
            "story_id": "US-NOT-2",
            "test_cases": ["TC-NOT-2-01: Create and edit notification templates with variables.", "TC-NOT-2-02: Test template preview functionality accuracy.", "TC-NOT-2-03: Accessibility testing for template management UI.", "TC-NOT-2-04: Audit log verification for template changes.", "TC-NOT-2-05: Localization testing for template management."],
            "title": "Notification Templates and Management",
            "user_story": "As an admin, I want to manage notification templates with variables and preview functionality to ensure consistent messaging."
          }
        ]
      },
      {
        "epic_name": "System Administration & Maintenance",
        "rationale": "Operational continuity and resilience (backup/restore/DR) are critical ahead of reporting and tickets.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API for configuring backup schedules, retention policies, and storage locations.", "Backup operations include verification and integrity checking with checksum validation.", "Restore operations with proper validation, confirmation steps, and post-restore verification procedures.", "All backup/restore operations are audit-logged with admin details and verification results.", "Notifications sent for backup completion, failures, and restore operations with detailed status reports.", "Accessibility: Backup/restore UI meets WCAG 2.1 AA with proper navigation and screen reader support.", "Disaster recovery procedures documented and tested including full system restoration scenarios."],
            "definition_of_done": ["Backup/restore functionality, scheduling, verification, notification, audit logging, accessibility, and disaster recovery procedures verified."],
            "depends_on": [],
            "description": "Implement system backup and restore functionality with proper scheduling, verification, and notification.",
            "estimate": "L",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-SYS-1",
            "test_cases": ["TC-SYS-1-01: Configure and execute backup operations with verification.", "TC-SYS-1-02: Perform restore operations with post-restore validation.", "TC-SYS-1-03: Test backup failure notifications and handling.", "TC-SYS-1-04: Accessibility testing for backup/restore UI.", "TC-SYS-1-05: Audit log verification for all operations.", "TC-SYS-1-06: Disaster recovery scenario testing with full system restoration."],
            "title": "Backup and Restore Operations",
            "user_story": "As a system administrator, I want to configure and execute backup and restore operations to ensure data protection and business continuity."
          },
          {
            "acceptance_criteria": ["Dashboard showing system health metrics, performance indicators, and status.", "Configurable alert thresholds for critical system parameters.", "Notifications for system alerts with appropriate severity levels.", "All health data is audit-logged for historical analysis.", "Accessibility: Monitoring dashboard meets WCAG 2.1 AA with proper navigation and screen reader support.", "Performance metrics include response times, error rates, and resource utilization."],
            "definition_of_done": ["System health monitoring, alerting, dashboard, notification, audit logging, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-SYS-1"}],
            "description": "Implement system health monitoring with dashboard, alerts, and performance metrics.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 2,
            "story_id": "US-SYS-2",
            "test_cases": ["TC-SYS-2-01: Monitor system health through dashboard.", "TC-SYS-2-02: Test alert triggering and notification delivery.", "TC-SYS-2-03: Accessibility testing for monitoring dashboard.", "TC-SYS-2-04: Audit log verification for health metrics.", "TC-SYS-2-05: Performance metric accuracy testing."],
            "title": "System Health Monitoring and Alerts",
            "user_story": "As a system administrator, I want to monitor system health and receive alerts for critical issues to maintain system reliability."
          },
          {
            "acceptance_criteria": ["UI/API for configuring system-wide settings including company information, default configurations, and global preferences.", "All configuration changes are audit-logged with admin details and timestamp.", "Validation prevents conflicting or invalid system configurations with appropriate error messages.", "All UI and error messages are localized; fallback to English with standardized error code.", "Accessibility: System configuration UI meets WCAG 2.1 AA with keyboard navigation, screen reader support, and color contrast (>=4.5:1).", "Settings are tenant-aware where applicable with proper access controls."],
            "definition_of_done": ["System-wide configuration management, audit logging, validation, localization, and accessibility verified."],
            "depends_on": [{"blocking": true, "story_id": "US-RBAC-1"}],
            "description": "Allow system administrators to configure global system settings including company information and default configurations.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 3,
            "story_id": "US-SYS-3",
            "test_cases": ["TC-SYS-3-01: Configure system-wide settings with various options.", "TC-SYS-3-02: Test validation for invalid configuration attempts.", "TC-SYS-3-03: Accessibility testing for configuration UI.", "TC-SYS-3-04: Audit log verification for configuration changes.", "TC-SYS-3-05: Localization fallback testing."],
            "title": "System-Wide Configuration Management",
            "user_story": "As a system administrator, I want to configure global system settings including company information and default configurations to customize the CRM environment."
          }
        ]
      },
      {
        "epic_name": "Bulk Operations & Imports",
        "rationale": "Efficient onboarding and mass-updates are gating needs for any go-live, but must follow RBAC, Compliance, and Tenant structures.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API allows upload of standard CSV/XLSX; supports field mapping and preview with full localization.", "Explicit data mapping step required before import, with validation for Unicode/RTL, multi-language support, and field matching.", "If import job is delayed (>5 minutes) or fails, user is notified with estimated time, error code, and guidance as per /docs/glossary-background-jobs-v1.5.7. Sample: 'Bulk import is taking longer than expected (BO-IMP-001). Estimated time: 8 minutes. You will be notified when complete.'", "Partial import errors trigger rollback of affected records and display a localized summary; fallback to English with standardized error code if localization fails.", "Audit log entry for import attempts/results, including user role and tenant context.", "Accessibility: Import UI meets WCAG 2.1 AA; test cases for screen reader, keyboard, color contrast (>=4.5:1). Tab order: upload > mapping > preview > import > error dialog.", "If import fails for technical reasons (e.g., timeout), user is shown guidance to retry, contact support, and receives incident reference."],
            "definition_of_done": ["Bulk import, mapping, validation, rollback, localization, audit, accessibility, error code, and background job handling tested."],
            "depends_on": [{"blocking": true, "story_id": "US-UP-1"}, {"blocking": true, "story_id": "US-MT-1"}],
            "description": "Admins can import bulk data for contacts and customers from CSV/XLSX with validation, localization, and rollback on error.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-BO-1",
            "test_cases": ["TC-BO-1-01: Import multi-script/RTL data, verify display and search.", "TC-BO-1-02: Simulate file format/validation errors, check error reporting and rollback with error code.", "TC-BO-1-03: Localization fallback and audit log review.", "TC-BO-1-04: Accessibility checks (screen reader, keyboard, color contrast).", "TC-BO-1-05: Import job delay/failure—check notification and fallback."],
            "title": "Bulk Import of Contacts and Customers",
            "user_story": "As an admin or onboarding specialist, I want to bulk import contacts/customers, with error handling and rollback, to support rapid onboarding."
          },
          {
            "acceptance_criteria": ["System detects and reports duplicate or conflicting records with row-level error code and guidance.", "Missing fields are flagged and require user resolution before import continues.", "Legacy scripts or encodings (non-UTF-8) are detected and either converted or rejected with explicit error message and standardized error code.", "On partial processing, successful records are committed, failed records are logged and rollback is available.", "Audit log captures all migration anomalies.", "Accessibility: All error states and dialogs tested for screen reader, keyboard nav, color contrast (>=4.5:1)."],
            "definition_of_done": ["Edge case handling, error code coverage, rollback, audit, accessibility tested."],
            "depends_on": [{"blocking": true, "story_id": "US-BO-1"}],
            "description": "Handle edge cases for data migration (duplicates, missing fields, legacy script handling); define mapping and rollback logic.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1.1,
            "story_id": "US-BO-1a",
            "test_cases": ["TC-BO-1a-01: Import file with duplicates; verify error codes and rollback.", "TC-BO-1a-02: Import file with missing/legacy encoded fields; verify error handling.", "TC-BO-1a-03: Partial migration; verify rollback and audit log.", "TC-BO-1a-04: Accessibility for error dialogs."],
            "title": "Data Migration Validation and Edge Cases",
            "user_story": "As a migration specialist, I want to handle edge cases for legacy customer/contact imports so data quality and system stability are not compromised."
          },
          {
            "acceptance_criteria": ["Export supports filters by entity, fields, date range, and language.", "Exported files include all Unicode/RTL data, correctly formatted per locale (dates, times, currency).", "If export job is delayed or fails, user is notified with error code and guidance per /docs/glossary-background-jobs-v1.5.7.", "If export fails, admin receives localized error/notification and guidance.", "Audit log entry for each export, including user and filters.", "Accessibility: Export UI meets WCAG 2.1 AA (screen reader, keyboard, contrast >=4.5:1)."],
            "definition_of_done": ["Bulk export, filters, localization, audit, accessibility, error code, background job handling tested."],
            "depends_on": [{"blocking": true, "story_id": "US-UP-1"}, {"blocking": true, "story_id": "US-MT-1"}],
            "description": "Admins can export contacts, customers, tickets, and opportunities with filters, localization, and audit trails.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 2,
            "story_id": "US-BO-2",
            "test_cases": ["TC-BO-2-01: Export data with multi-language/RTL content, verify output.", "TC-BO-2-02: Simulate export delay/failure, check fallback and guidance.", "TC-BO-2-03: Localization, error code, and audit checks.", "TC-BO-2-04: Accessibility on export screen."],
            "title": "Bulk Export of CRM Data",
            "user_story": "As an admin, I want to export CRM data (contacts, tickets, etc.) using filters and have results in CSV/XLSX/PDF for offline analysis."
          }
        ]
      },
      {
        "epic_name": "Ticketing System",
        "rationale": "Core for customer support, dependent on foundational CRM data.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API supports ticket add, edit, assign, resolve/close. Required fields: customer/contact, subject, status.", "Assignment notifies assignee: 'You have been assigned a new ticket (TICK-ASSIGN-001)'.", "Tickets must be linked to a customer or contact; orphan prevention: 'Ticket must have an associated customer or contact (TICK-VAL-004)'.", "Ticket changes/notes are audit-logged (user, action, time, before/after).", "Edge case: Cannot close ticket if required fields missing or unresolved dependencies; error shown.", "All error and success messages localized; fallback to English and display code.", "Accessibility: WCAG 2.1 AA. Test: Focus order—subject > description > contact > assign > status. Screen reader must announce ticket status and assignment; color contrast >=4.5:1."],
            "definition_of_done": ["CRUD, assignment, notification, localization, audit, accessibility, orphan/dependency error coverage complete."],
            "depends_on": [{"blocking": true, "story_id": "US-CPM-1"}, {"blocking": true, "story_id": "US-CONT-1"}],
            "description": "Enable users to create, update, assign, and resolve customer tickets, with localization, notification, audit, and accessibility.",
            "estimate": "L",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-TICK-1",
            "test_cases": ["TC-TICK-1-01: Create/assign/close ticket with Unicode notes.", "TC-TICK-1-02: Assign to user, check notification and audit.", "TC-TICK-1-03: Attempt to close incomplete ticket.", "TC-TICK-1-04: Accessibility—focus order and screen reader.", "TC-TICK-1-05: Localization fallback."],
            "title": "Ticket CRUD and Assignment",
            "user_story": "As a support user, I want to manage tickets linked to customers/contacts, assign ownership, update status, and add notes."
          },
          {
            "acceptance_criteria": ["UI/API for note/attachment add, edit, remove; supports Unicode/RTL scripts.", "All changes logged; deletion of attachment confirmed by user.", "Localized error: 'Attachment upload failed (TICK-ATT-002)'.", "Accessibility: Attachments and notes support keyboard navigation and screen reader announcements.", "Search supports multi-language content in notes/attachments where feasible."],
            "definition_of_done": ["Note/attachment add/edit/delete, Unicode/RTL, audit, localization, accessibility tested."],
            "depends_on": [{"blocking": true, "story_id": "US-TICK-1"}],
            "description": "Allow users to add, edit, and remove notes and attachments on tickets, with Unicode/RTL support, audit, and accessibility.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1.1,
            "story_id": "US-TICK-1a",
            "test_cases": ["TC-TICK-1a-01: Add/edit/remove notes and attachments with multi-language content.", "TC-TICK-1a-02: Simulate upload failure.", "TC-TICK-1a-03: Accessibility—keyboard and screen reader.", "TC-TICK-1a-04: Audit log review."],
            "title": "Split: Ticket Note and Attachment Management",
            "user_story": "As a support user, I want to add notes and attachments to tickets, supporting all languages and accessibility requirements."
          }
        ]
      },
      {
        "epic_name": "Workflow Automation & Rules",
        "rationale": "Automates repetitive actions for efficiency and compliance, often a key differentiator in CRM.",
        "user_stories": [
          {
            "acceptance_criteria": ["UI/API for defining triggers (create/update/delete of entity) and actions (send notification, update field, assign owner).", "All rule names/descriptions localized; error messages fallback to English (sample: 'Invalid workflow action (WAR-VAL-002)').", "Changes logged in audit with who, when, what.", "Accessibility: WCAG 2.1 AA, explicit checks: Tab order through trigger/action selection; screen reader reads rule summary; color contrast >=4.5:1.", "Invalid or incomplete rules not saved (error: 'Complete all required fields before saving (WAR-VAL-003)')."],
            "definition_of_done": ["Rule creation UI/API, validation, localization, audit, accessibility, fallback error coverage complete."],
            "depends_on": [{"blocking": true, "story_id": "US-RBAC-1"}],
            "description": "Allow admins to define workflows: when [event], then [action], with accessible, localized UI and audit.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-WAR-1",
            "test_cases": ["TC-WAR-1-01: Define valid rule, verify audit and localization.", "TC-WAR-1-02: Attempt to save incomplete rule.", "TC-WAR-1-03: Accessibility—tab and screen reader.", "TC-WAR-1-04: Localization fallback."],
            "title": "Workflow Rule Definition",
            "user_story": "As an admin, I want to define rules (e.g., 'When opportunity closes, send notification') with clear UI and audit."
          },
          {
            "acceptance_criteria": ["Rule execution handled as background job; status visible to admin (sample: 'Rule executed successfully (WAR-EXEC-001)').", "Failures/delays notify admin with guidance (sample: 'Workflow failed to execute (WAR-EXEC-002). Retry or check rule configuration').", "Audit logs all rule executions and failures.", "Localized notifications/messages; fallback to English with error code.", "Accessibility: Monitoring UI meets WCAG 2.1 AA (screen reader reads status, color contrast >=4.5:1 for success/failure)."],
            "definition_of_done": ["Rule execution, monitoring, notification, audit, localization, accessibility tested."],
            "depends_on": [{"blocking": true, "story_id": "US-WAR-1"}],
            "description": "Support execution of workflow rules as defined, background job handling, notification, audit, and monitoring.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 2,
            "story_id": "US-WAR-2",
            "test_cases": ["TC-WAR-2-01: Trigger rule, verify execution and notification.", "TC-WAR-2-02: Simulate rule failure.", "TC-WAR-2-03: Audit and localization fallback.", "TC-WAR-2-04: Accessibility—status indicators."],
            "title": "Workflow Rule Execution and Monitoring",
            "user_story": "As an admin, I want to be notified when a rule executes, monitor success/failure, and see audit/logs."
          }
        ]
      },
      {
        "epic_name": "Mobile Support",
        "rationale": "Key for field and external access; core mobile flows prioritized. If mobile is a primary channel, core workflows must be delivered with web parity.",
        "user_stories": [
          {
            "acceptance_criteria": ["Technical spike to validate Unicode/RTL search feasibility at mobile scale with performance constraints.", "Performance testing for multi-language search across customer names, contact names, opportunity titles with various data volumes and specific benchmarks: <500ms response time for 10,000 records, <2s for 100,000 records.", "Assessment of technical constraints for large text fields (>10KB) and complex linguistic processing.", "Documentation of search scope limitations for user-facing help including specific scalability limits.", "Recommendations for implementation approach balancing functionality and performance with measurable outcomes."],
            "definition_of_done": ["Search feasibility validated with specific performance benchmarks, constraints documented, recommendations provided."],
            "depends_on": [],
            "description": "Technical spike to validate multi-language search feasibility for mobile with performance constraints and Unicode/RTL support.",
            "estimate": "S",
            "priority": "must have",
            "priority_within_epic": 0.5,
            "story_id": "US-MOB-0",
            "test_cases": ["TC-MOB-0-01: Performance testing with multi-language search data at specified volume benchmarks.", "TC-MOB-0-02: Unicode/RTL search capability validation.", "TC-MOB-0-03: Large text field constraint assessment.", "TC-MOB-0-04: Documentation review for user-facing limitations including scalability boundaries."],
            "title": "Mobile Search Feasibility Technical Spike",
            "user_story": "As a mobile architect, I want to validate the feasibility of multi-language Unicode/RTL search on mobile devices with performance constraints."
          },
          {
            "acceptance_criteria": ["Mobile UI provides feature parity for core flows: create/edit/view contacts, opportunities, tickets.", "All UI, error, and notification messages are localized; fallback to English with standardized error code if localization resource missing.", "Date/time/currency are formatted per device locale and user preference; edge cases (24h/12h, week start, RTL) are covered.", "If an operation fails (offline, API error, missing data), user receives clear fallback message with standardized error code, guidance, and resolution steps (retry, contact support).", "Accessibility: Mobile UI meets WCAG 2.1 AA, with explicit test cases for touch targets (>=44x44px), voiceover/screen reader, keyboard nav (where relevant), and high-contrast mode. For iOS/Android, verify focus order: navigation > primary action > fields."],
            "definition_of_done": ["Mobile UI parity, localization, error code coverage, accessibility, and edge case coverage verified."],
            "depends_on": [{"blocking": true, "story_id": "US-UP-1"}, {"blocking": true, "story_id": "US-NOT-1"}, {"blocking": true, "story_id": "US-MOB-0"}],
            "description": "Deliver mobile UI and interactions for core workflows (contacts, opportunities, tickets) with localization, accessibility, and error handling.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-MOB-1",
            "test_cases": ["TC-MOB-1-01: Perform all core flows in mobile app with multiple locales and scripts.", "TC-MOB-1-02: Simulate network/API failures, verify fallback, error code, and guidance.", "TC-MOB-1-03: Check date/time/currency in US/EU/AR settings.", "TC-MOB-1-04: Accessibility testing for voiceover, touch targets, color contrast.", "TC-MOB-1-05: Verify error code consistency in all fallback messages."],
            "title": "Mobile UI Parity for Core Flows",
            "user_story": "As a mobile user (sales, support, admin), I want the same workflows and data on mobile as on web, with proper error handling and localization."
          },
          {
            "acceptance_criteria": ["POC implementation demonstrates offline data storage and synchronization capabilities for CRM entity relationships.", "Conflict resolution strategies evaluated and documented for complex data scenarios including customer-contact-opportunity relationships with specific resolution patterns: last-write-wins, manual merge, and field-level conflict resolution.", "Performance testing for sync operations with various data volumes and relationship complexity including sync time benchmarks for different data sizes.", "Battery impact assessment for mobile devices during sync operations with specific energy consumption metrics.", "Data consistency requirements defined for offline operations including referential integrity maintenance with validation rules.", "Feasibility assessment for complex data relationships in offline mode with risk mitigation strategies and measurable success criteria.", "Architecture documentation for data consistency patterns including entity relationship handling in offline mode with specific implementation patterns.", "Recommendations documented for implementation approach, data consistency patterns, and performance optimization with clear go/no-go criteria based on POC results."],
            "definition_of_done": ["POC implemented, conflict resolution strategies validated for complex relationships, performance assessed with benchmarks, data consistency requirements defined, architecture documentation complete, and recommendations provided."],
            "depends_on": [{"blocking": true, "story_id": "US-MOB-1"}],
            "description": "Technical spike to validate data consistency patterns for mobile offline support including conflict resolution for complex CRM relationships and sync mechanisms.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1.5,
            "story_id": "US-MOB-2",
            "test_cases": ["TC-MOB-2-SP01: Offline data storage performance testing with complex relationships.", "TC-MOB-2-SP02: Conflict resolution scenario testing for related entity updates.", "TC-MOB-2-SP03: Battery impact measurement during sync operations.", "TC-MOB-2-SP04: Data relationship complexity assessment and consistency validation.", "TC-MOB-2-SP05: Referential integrity maintenance in offline mode testing.", "TC-MOB-2-SP06: Architecture review for data consistency patterns."],
            "title": "Mobile Offline Support Technical Spike",
            "user_story": "As a mobile architect, I want to validate the technical feasibility of offline data synchronization and conflict resolution mechanisms for complex CRM data relationships."
          },
          {
            "acceptance_criteria": ["Mobile app caches recent data for offline access; local changes stored and sync when online.", "Conflicts detected and user notified with detailed resolution options: 'Sync conflict detected (MOB-SYNC-002). Your changes: X, Server changes: Y. Choose which to keep or merge manually.'", "Sync status visible; offline edits show sync icon/status.", "All offline errors have fallback guidance (sample: 'Unable to sync, please retry or contact support.').", "Accessibility: Offline indicators and sync status read by screen readers; color contrast for status icons.", "Implementation follows technical spike recommendations for data consistency and complex relationship handling.", "Data consistency maintained for customer-contact-opportunity relationships during offline operations."],
            "definition_of_done": ["Offline cache/edit, sync, conflict/error handling with detailed resolution options, localization, accessibility, and data consistency for complex relationships verified."],
            "depends_on": [{"blocking": true, "story_id": "US-MOB-2"}],
            "description": "Allow mobile users to access and edit CRM data offline, with conflict handling and sync notification based on spike findings.",
            "estimate": "M",
            "priority": "should have",
            "priority_within_epic": 2,
            "story_id": "US-MOB-2a",
            "test_cases": ["TC-MOB-2a-01: Make changes offline, verify sync and conflict resolution with detailed options.", "TC-MOB-2a-02: Accessibility—screen reader for status.", "TC-MOB-2a-03: Error and fallback messaging.", "TC-MOB-2a-04: Data consistency verification after sync for complex relationships.", "TC-MOB-2a-05: Referential integrity validation during offline operations.", "TC-MOB-2a-06: Conflict resolution UI testing for multiple scenario types."],
            "title": "Mobile Offline Support Implementation",
            "user_story": "As a mobile user, I want to view and edit CRM data offline and sync changes when reconnected with proper conflict resolution for complex relationships."
          },
          {
            "acceptance_criteria": ["Push notifications sent for assignment/updates on tickets/opportunities.", "Notifications localized per user/device language; fallback to English with code.", "Notifications have action buttons (sample: 'Open Ticket', 'Mark as Read').", "Accessibility: iOS/Android notification voiceover, readable titles, minimum font size, and device vibration for high-priority alerts.", "Test device-specific behaviors (Android notification grouping, iOS badge count)."],
            "definition_of_done": ["Push notification, device accessibility, localization, actionable UI, fallback error handling tested."],
            "depends_on": [{"blocking": true, "story_id": "US-NOT-1"}],
            "description": "Support push notifications for tickets/opportunities and test device-specific accessibility scenarios.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 3,
            "story_id": "US-MOB-3",
            "test_cases": ["TC-MOB-3-01: Receive push on multiple devices/languages.", "TC-MOB-3-02: Accessibility—voiceover, vibration, font size.", "TC-MOB-3-03: Device-specific grouping/badge tests.", "TC-MOB-3-04: Fallback error for failed delivery."],
            "title": "Mobile Push Notifications and Device Accessibility",
            "user_story": "As a mobile user, I want to receive push notifications for key events with accessible notification UI across devices."
          }
        ]
      },
      {
        "epic_name": "Dashboard & Custom Reporting",
        "rationale": "Empowers end users (sales, CS) to make data-driven decisions with actionable dashboards and custom reports.",
        "user_stories": [
          {
            "description": "See Reporting and Audit Logs epic for details.",
            "priority_within_epic": 1,
            "story_id": "US-RAL-2",
            "title": "Standard CRM Reporting (Entities)"
          },
          {
            "description": "See Reporting and Audit Logs epic for details.",
            "priority_within_epic": 2,
            "story_id": "US-RAL-3",
            "title": "Custom Report Builder"
          },
          {
            "description": "See Reporting and Audit Logs epic for details.",
            "priority_within_epic": 3,
            "story_id": "US-RAL-3a",
            "title": "Custom Report Visualization"
          }
        ]
      },
      {
        "epic_name": "Integrations & API Requirements",
        "rationale": "Extends system value to partners and enables internal/external extensibility.",
        "user_stories": [
          {
            "acceptance_criteria": ["Evaluate existing tooling for OpenAPI/Swagger documentation localization.", "Assess process requirements for maintaining localized documentation across releases.", "Test localization accuracy and consistency across supported languages.", "Document recommended approach and tooling requirements.", "Identify any platform constraints or limitations for documentation localization.", "Provide feasibility assessment and risk mitigation strategies with measurable success criteria."],
            "definition_of_done": ["Tooling evaluated, processes validated, feasibility assessed, documentation complete, and recommendations provided."],
            "depends_on": [],
            "description": "Technical spike to validate tooling and processes for localized API documentation across supported languages.",
            "estimate": "S",
            "priority": "must have",
            "priority_within_epic": 0.5,
            "story_id": "US-INT-1-TS",
            "test_cases": ["TC-INT-1-TS01: Tooling evaluation for documentation localization.", "TC-INT-1-TS02: Process workflow validation.", "TC-INT-1-TS03: Localization accuracy testing sample content.", "TC-INT-1-TS04: Platform constraint assessment."],
            "title": "API Documentation Localization Technical Spike",
            "user_story": "As a technical lead, I want to validate the feasibility of localized API documentation tooling and processes before implementation."
          },
          {
            "acceptance_criteria": ["API contract published using OpenAPI/Swagger for contacts, opportunities, tickets (CRUD, search).", "Contract includes all required/optional fields, error codes (per standardized /docs/glossary-error-codes-v1.5.7), and sample requests/responses.", "API documentation is localized for all supported UI languages; localized Swagger/OpenAPI docs are reviewed for language accuracy and accessibility. Implementation follows technical spike recommendations.", "Versioning strategy defined (e.g., /v1/) with backward compatibility guidelines.", "All error messages and field-level validation returned by API must be localized where user context is available (Accept-Language); fallback to English if missing. For asynchronous/batch operations, localization fallback logic is defined and tested; guidance provided if user context is lost.", "API authentication and RBAC scope requirements documented and enforced; platform constraints reviewed before implementation. Example: 'API access denied: insufficient scope (API-SEC-004)'.", "If API call fails due to validation or permission, client receives a localized error message, standardized error code, and actionable guidance.", "Accessibility: API documentation meets WCAG 2.1 AA (explicit checks for keyboard navigation, screen reader markup, color contrast >=4.5:1)."],
            "definition_of_done": ["API contract, docs (localized), versioning, localization fallback/Accept-Language, error handling, standardized codes, accessibility complete and tested. Technical spike recommendations implemented."],
            "depends_on": [{"blocking": true, "story_id": "US-INT-1-TS"}],
            "description": "Define and publish minimal REST API contracts for core CRM entities (contacts, opportunities, tickets) with localization, fallback, and accessibility.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-INT-1",
            "test_cases": ["TC-INT-1-01: Generate OpenAPI docs, validate fields and error messages.", "TC-INT-1-02: Verify all localized Swagger/OpenAPI docs for English, German, French.", "TC-INT-1-03: API call with unsupported locale and in async/batch context, verify fallback to English and error code.", "TC-INT-1-04: Invalid input/permission failure, verify localized error, code, and guidance.", "TC-INT-1-05: Accessibility testing for API docs (keyboard, screen reader, contrast).", "TC-INT-1-06: Technical spike outcome implemented and validated."],
            "title": "Public REST API Contract Definition",
            "user_story": "As a developer (partner or internal), I want a documented, versioned REST API contract for core CRM entities to enable integration and development."
          },
          {
            "acceptance_criteria": ["All API endpoints require OAuth2 or similar token; no anonymous access. Platform-level constraints and security frameworks reviewed before implementation.", "Rate limits enforced per client/tenant; configurable threshold.", "Authorization errors return localized error messages, standardized error codes, and actionable guidance. Fallback to English if resource missing.", "Security audit log entry for failed access attempts.", "If rate limit exceeded, API returns 429 with localized message/fallback and error code.", "Third-party integration error handling includes detailed error codes and retry guidance.", "Accessibility: API error responses and docs meet WCAG 2.1 AA (screen reader, keyboard, color contrast >=4.5:1)."],
            "definition_of_done": ["API security, rate limiting, error handling including third-party integration scenarios, localization, fallback, standardized error code, audit, accessibility tested."],
            "depends_on": [{"blocking": true, "story_id": "US-INT-1"}],
            "description": "Implement authentication, authorization, and basic rate limits for all public APIs with localization, fallback, and audit logging.",
            "estimate": "S",
            "priority": "must have",
            "priority_within_epic": 2,
            "story_id": "US-INT-2",
            "test_cases": ["TC-INT-2-01: API call without token, verify access denied, localization/fallback, error code.", "TC-INT-2-02: Exceed rate limit, check error message/fallback and error code.", "TC-INT-2-03: Review audit log for failed attempts.", "TC-INT-2-04: Third-party integration error scenario testing.", "TC-INT-2-05: Accessibility and guidance checks."],
            "title": "API Security and Rate Limiting",
            "user_story": "As a security officer, I want all API endpoints secured with access tokens, RBAC, and rate limiting to protect CRM data."
          }
        ]
      },
      {
        "epic_name": "Usability and Guidance",
        "rationale": "Enhances adoption and reduces onboarding friction.",
        "user_stories": [
          {
            "acceptance_criteria": ["Unified search interface supporting customers, contacts, opportunities, and tickets.", "Search supports Unicode/RTL scripts and multi-language content within feasibility constraints.", "Results are ranked by relevance with clear entity type indicators.", "Search interface meets WCAG 2.1 AA accessibility standards.", "Performance optimized for response times under 2 seconds for typical queries.", "Search queries are audit-logged for security monitoring.", "Localized error messages and fallback handling for search failures."],
            "definition_of_done": ["Unified search functionality, multi-language support, accessibility, performance, audit logging, and error handling verified."],
            "depends_on": [{"blocking": true, "story_id": "US-CPM-1"}, {"blocking": true, "story_id": "US-CONT-1"}, {"blocking": true, "story_id": "US-OPP-1"}, {"blocking": true, "story_id": "US-TICK-1"}, {"blocking": true, "story_id": "US-MOB-0"}],
            "description": "Implement unified search across customers, contacts, opportunities, and tickets with multi-language support and accessibility.",
            "estimate": "M",
            "priority": "must have",
            "priority_within_epic": 1,
            "story_id": "US-SEARCH-1",
            "test_cases": ["TC-SEARCH-1-01: Search across multiple entity types with various query types.", "TC-SEARCH-1-02: Test multi-language and RTL search functionality.", "TC-SEARCH-1-03: Verify accessibility compliance for search interface.", "TC-SEARCH-1-04: Performance testing with concurrent search requests.", "TC-SEARCH-1-05: Audit log verification for search activities.", "TC-SEARCH-1-06: Localization fallback testing for error messages."],
            "title": "System-Wide Search Functionality",
            "user_story": "As a CRM user, I want to search across all major entities (customers, contacts, opportunities, tickets) with a single interface to quickly find relevant information."
          }
        ]
      },
      {
        "epic_name": "Backlog Transparency & Scope",
        "rationale": "Ensures shared understanding and quality of delivery.",
        "user_stories": []
      },
      {
        "epic_name": "Out-of-Scope and Deferred",
        "rationale": "To prevent scope creep and clarify release boundaries.",
        "user_stories": []
      }
    ],
    "error_code_handling": {
      "error_code_format_summary": "Standardized error code format: [ENTITY]-[CONTEXT]-[NUMBER] (e.g., 'USR-VAL-001'). All UI and API fallback messages must display these codes. Error codes are centrally managed and cross-entity standardized.",
      "management_reference": "/docs/glossary-error-codes-v1.5.7",
      "standardization": "All error codes referenced in fallback messages across stories must use the centrally managed, cross-entity standardized error code format defined in /docs/glossary-error-codes-v1.5.7. The code format is [ENTITY]-[CONTEXT]-[NUMBER], e.g., 'USR-VAL-001'. All UI and API fallback messages must display these codes and acceptance criteria must confirm correct mapping."
    },
    "language_requirements_glossary": "Whenever 'supported languages' is referenced, this refers explicitly to English, German, and French for both UI and notifications unless otherwise stated (see /docs/glossary-languages-v1.5.6). All error messages, custom widgets, third-party integration UI, and edge cases must have localization and test coverage for each language. Data entry (e.g., customer names, notes, attachments) must support Unicode and right-to-left scripts for internationalization. All non-UI data (notes, attachments, custom fields) must retain original input, display correctly, and support multi-language search where feasible. All stories must include test cases and acceptance criteria covering edge cases for Unicode/RTL, date/time/currency localization, and fallback to English if localization is missing.",
    "notification_requirements": {
      "critical_behaviors_summary": "Localized notifications per user preference; actionable links; in-app supports HTML, email is plain text. System notifies on critical events, fallback paths for delivery failures documented. All notification-related error messages and notification content must be localized and tested in all supported languages. If localization resources fail, fallback to English with standardized error code. Fallback messages must provide actionable guidance (e.g., 'Retry', 'Contact Support with Code XYZ'). Example for failed notification: 'Unable to deliver notification (NOTIFY-DEL-003). Please check your email settings or contact support.'",
      "format_reference": "/docs/notification-format-crm-v1.5.6",
      "required_fields": ["timestamp", "recipient_user_id", "channel (email, in-app, push)", "subject", "body", "language (English, German, French)", "priority", "action_link"]
    },
    "project_name": "CRM System",
    "search_requirements": {
      "feasibility_criteria": "Search implementation must balance performance and functionality. Full-text search capabilities are prioritized for core business entities with reasonable performance expectations documented per entity type.",
      "multi_language_scope": "Multi-language search is feasible for: customer names, contact names, opportunity titles, ticket subjects, and notes fields. Search supports Unicode/RTL scripts with basic stemming and diacritic-insensitive matching. Technical constraints may limit search performance for large text fields (>10KB) or complex linguistic processing. Search scope limitations must be documented in user-facing help."
    },
    "supported_languages": ["English", "German", "French"],
    "time_zone_handling": "All user-facing timestamps and time zones are handled according to the user's preference. Tenant defaults apply for new users. Supported time zones include UTC and all IANA time zones (e.g., America/New_York, Europe/Berlin, Asia/Tokyo) with automatic daylight saving time adjustments.",
    "version": "1.5.22"
  }
}
'''

feedback = '''
{
  "feedback": {
    "completeness": {
      "suggestions": [
        "Missing user stories for Multi-Tenant Administration epic - stories US-MT-1 and US-MT-2 reference tenant management but no stories exist for actual data segregation implementation",
        "No stories address audit log retention/archiving implementation despite requirements in audit_logging_requirements section",
        "Notification epic lacks stories for actual notification delivery to users - only covers infrastructure and templates"
      ]
    },
    "clarity": {
      "suggestions": [
        "Technical spike stories (US-RAL-6, US-MOB-0, etc.) have acceptance criteria that mix technical validation with implementation requirements - should separate spike validation from implementation criteria",
        "Multiple stories reference '/docs/glossary-error-codes-v1.5.7' but this document is not included in external_standards_links - creates ambiguity about error code standards"
      ]
    },
    "Prioritization": {
      "suggestions": [
        "Mobile Support epic prioritized at 16 but contains must-have stories that depend on multiple high-priority epics - consider elevating mobile core flows if business-critical",
        "System Administration epic (priority 10) has backup/restore stories that should be higher priority given their criticality for data protection"
      ]
    },
    "Technical feasibility": {
      "suggestions": [
        "Audit log requirement of 2,000 events/minute with immutable storage and <100ms latency may require significant infrastructure investment - consider feasibility assessment for smaller deployments",
        "Mobile offline sync for complex CRM relationships (US-MOB-2) presents significant technical challenges for conflict resolution - may require simplified initial implementation"
      ]
    }
  }
}
'''

try:
    # Your JSON string here
    data = json.loads(feedback)
    print("JSON is valid!")
except json.JSONDecodeError as e:
    print(f"Error at position {e.pos}: {e.msg}")
    print(f"Near: ...{feedback[max(0,e.pos-50):e.pos+50]}...")