---
name: cronjob-investigation
category: devops
description: Investigate the execution path and actions of a scheduled cron job.
---

## Purpose

This skill outlines the steps to investigate a scheduled cron job, including identifying the script it runs and tracing its execution to understand its full functionality. This is useful for verifying backup configurations, troubleshooting unexpected behavior, or understanding automated tasks.

## Trigger Conditions

Use this skill when:
- You need to verify what a cron job is actually doing.
- You need to confirm if specific actions (e.g., "Obsidian yedeklemeye dahil edildi mi?") are part of a scheduled task.
- You are troubleshooting a cron job or a scheduled automated process.

## Steps

1.  **List all active cron jobs:**
    ```tool_code
    print(default_api.cronjob(action="list"))
    ```

2.  **Identify the relevant cron job:** From the output, find the `name` and `script` fields of the job you want to investigate. Note the `script` path.

3.  **Read the main cron script:** Use `read_file` to view the content of the script identified in step 2.
    `read_file(path="/path/to/script.sh")`

4.  **Trace nested scripts (if any):** If the main script calls other scripts (e.g., `./backup.sh` or `python3 ./some_script.py`), repeat step 3 for each nested script until you reach the core logic that performs the desired actions. Pay attention to `cd` commands that change directories, as relative paths will be resolved from the new working directory.

5.  **Analyze the script logic:** Examine the script(s) to understand what files and directories are being accessed, what commands are being executed, and if the specific task you're looking for (e.g., Obsidian backup) is present.

## Pitfalls

-   **Relative Paths:** Scripts often use relative paths. Ensure you understand the current working directory (`cd` commands) when interpreting file paths within the script. The `SOURCE_ROOT` variable in Python scripts (like `backup_state.py`) is crucial for understanding the base directory for operations.
-   **Environment Variables:** Cron jobs run in a minimal environment. Scripts might rely on environment variables that are not set in the cron context, leading to unexpected behavior. This investigation focuses on what the script *intends* to do, but actual execution issues might require checking the cron environment.
-   **Dynamic Script Generation:** Some complex systems might dynamically generate scripts. This skill focuses on static script analysis.
-   **Permissions:** Ensure the agent has permission to read the script files.

## Verification

After tracing the scripts, explicitly state whether the desired action is confirmed to be part of the scheduled task, and provide the relevant code snippets or lines that support your conclusion.
