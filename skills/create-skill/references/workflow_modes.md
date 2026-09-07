# Evaluation modes

Choose a mode that the actual environment supports. Do not assume a particular CLI, browser, paid API, or subagent tool exists.

## Independent behavioral runs

Use independent agents or fresh host sessions for broad changes when permitted. Give each run the task, candidate skill, and minimum raw inputs. Keep the author's notes, expected solution, graders, and other run outputs out of the execution context. Use isolated writable folders and existing authorized tools; do not let fixtures affect production systems.

For a new skill, compare `with_skill` and `without_skill`. For updates, compare `with_skill` and the saved `old_skill`; a no-skill arm can also test whether the instructions still add value. Both arms need the same model, runtime, settings, tools, permissions, task, and input bytes. A baseline that can still discover the candidate is contaminated.

Separate these questions:

1. **Execution:** When explicitly given the skill, can the agent complete the task?
2. **Discovery:** Does the host select the skill when it should, and leave adjacent tasks alone?
3. **Value:** Does it improve the chosen outcome over a fair baseline at an acceptable time or token cost?

A fresh subagent may still inherit host instructions or a global skills catalogue. Record that limitation. It is not enough to label two output folders differently.

Use the existing evaluation schema. Keep the reference version fixed for regression tests; if you also compare with the previous iteration, label that separately. Repeat uncertain or variable cases. Record actual timing and token data only when available; capture model identity and settings from the runner rather than guessing.

For subjective outputs, use task-specific criteria and inspect the artifacts. An independent judge can compare anonymized A/B outputs; vary presentation order when the result matters. Treat judgment as evidence with limits, not an objective ground truth.

## No independent runner

Perform the supported structural checks and representative task walkthroughs. Save the resulting artifacts and label the walkthroughs as checks by the author. Do not fabricate baseline scores or call self-simulated trigger decisions observed host behavior. Deliver the work with the remaining test scope stated clearly.

## No browser

The review generator produces a static `review.html`. Link the file or show the relevant output in conversation. It does not collect or infer user approval.

## No filesystem

Return the proposed files as copyable content and explain which checks require a writable environment. Do not claim that helpers ran or an archive was created.

## Installed or read-only source

Copy the skill to a permitted writable folder, preserving its directory name and frontmatter name. Keep the original as a baseline. Edit and validate the copy. Deliver the copy or archive, and identify the source that would need updating. Do not silently overwrite a separate installed copy or publish the repository.

## Stopping and handoff

Complete the requested checks and review any observed failures. Stop an optional tuning loop when the intended outcome is met, the agreed budget is reached, or further trials no longer change the decision. Do not use a fixed iteration count or missing optional tools to block a small authorized edit. Label unfinished evaluation work accurately.
