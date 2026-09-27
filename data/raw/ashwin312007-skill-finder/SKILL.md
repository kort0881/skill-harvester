---
name: Skill_Finder
description: Searches the available skills repository and matches relevant ones to the user's project workspace technologies, files, or requirements.
---
# Skill Finder

This skill helps identify and choose appropriate domain-specific skills from the local skills repository that are relevant to the current project/workspace.

## Purpose
When working on a project, using targeted skills (such as `python-testing-patterns`, `react-state-management`, `firebase-basics`, etc.) ensures high-quality code aligned with best practices. This skill automates discovery of these skills.

## Guidelines

### 1. Discovery
To find relevant skills for the active workspace/project:
- Run the python helper script:
  ```powershell
  python C:\Users\teash\.gemini\config\skills\Skill_Finder\scripts\find_skills.py
  ```
- Alternatively, you can specify the target directory:
  ```powershell
  python C:\Users\teash\.gemini\config\skills\Skill_Finder\scripts\find_skills.py "C:\path\to\your\workspace"
  ```

### 2. Matching and Choosing
The script scans files and configurations in the current project, detects key programming languages and frameworks, matches them to the skills in the repository, and outputs a ranked list of relevant skills.

### 3. Activating / Using Skills
To "add" or use a matched skill in your development workflow:
1. Locate the path of the recommended skill from the script output.
2. Read the recommended skill's `SKILL.md` using the `view_file` tool.
3. Integrate its specific rules, architectural patterns, and guidelines into your current coding session.
4. Inform the user which skills you have activated/found for the project.
