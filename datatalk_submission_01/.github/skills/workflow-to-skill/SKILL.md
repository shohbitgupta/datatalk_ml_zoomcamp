---
name: workflow-to-skill
description: 'Turn a repeated multi-step workflow or methodology into a reusable SKILL.md. Use for packaging debugging approaches, review checklists, implementation patterns, and decision trees into discoverable project or personal skills.'
argument-hint: 'What workflow should be turned into a reusable skill?'
user-invocable: true
disable-model-invocation: false
---

# Workflow to Skill

## When to Use
- The user is following a repeatable process across tasks
- You need to convert a working method into a reusable workflow
- The task involves debugging, review, implementation, triage, or decision-making patterns
- The workflow should be available again later as a discoverable skill

## Procedure
1. Identify the actual workflow.
   - Look for repeated stages, explicit steps, recurring decisions, and completion checks.
   - Generalize from the specific task into a reusable process.
2. Extract the step-by-step sequence.
   - Write the process in the order it normally happens.
   - Preserve the real logic the user follows rather than inventing an idealized version.
3. Capture decision points.
   - Note branching logic such as "if the bug is reproduced, then ...", "if the scope is unclear, then ...".
   - Convert decisions into actionable instructions and fallback paths.
4. Define quality criteria.
   - Add completion checks such as verifying scope, validating outputs, checking assumptions, and confirming unresolved issues are addressed.
5. Choose the right scope.
   - Use a project-scoped skill when the workflow applies to a repository or team.
   - Use a personal skill when it is reusable across workspaces or individual practice.
6. Draft the SKILL.md.
   - Include frontmatter with a clear name and keyword-rich description.
   - Add sections for when to use, procedure, decision points, and completion checks.
7. Refine weak spots.
   - Ask the user to clarify ambiguous parts, missing conditions, or unclear success criteria.
   - Tighten the final instructions so the workflow is practical and reusable.
8. Finalize and summarize.
   - Confirm the file is in the correct skill location.
   - Explain what the skill produces and how to invoke or reuse it.
   - Suggest example prompts and related customizations to create next.

## Decision Points
- If the workflow is clear and repeatable, create a full skill.
- If the workflow is still fuzzy, ask what outcome is desired and what scope it should apply to.
- If the task is a single one-off action, prefer a prompt instead of a skill.
- If the behavior should apply broadly and always be loaded, prefer project or user instructions instead of a skill.
- If the work requires context isolation or separate tool restrictions, prefer a custom agent instead of a skill.

## Completion Checklist
- The skill name matches the folder name.
- The description includes action-oriented trigger words.
- The procedure includes the real sequence of work.
- Decision branches are explicit where they matter.
- Completion checks or validation criteria are included.
- The file is saved in the correct customization location.
- The final summary explains the skill output and example use cases.

## Example Prompts
- "Turn my debugging workflow into a reusable skill for this repo."
- "Package my review checklist as a project skill."
- "Convert my implementation process into a workflow skill with decision points and completion checks."
- "Create a personal skill for issue triage and validation."

## Related Customizations
- Project instructions for routine rules that apply across the workspace
- File-specific instructions for project patterns and conventions
- Custom agents for multi-stage workflows with restricted tools or isolated context
- Prompt files for single-purpose tasks that need parameterized inputs
