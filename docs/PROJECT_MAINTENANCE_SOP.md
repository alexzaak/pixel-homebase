# Star-Office-UI Project Maintenance SOP (Lightweight Version)

> Goal: Keep the repository clean, responses friendly, rhythm stable, and community focus clear while Star-Office-UI continues to grow.

---

## 1. General Principles

### 1.1 Always leave a closure reason when closing an issue / PR

Whether it is:
- Fixed
- Duplicate
- Out of current scope
- Canceled by the requester themselves
- Absorbed by another PR / issue

Always try to leave a sentence explaining the reason.

**Minimal Templates:**
- Fixed in `commit/PR #xxx`, thanks for the report!
- Closing as duplicate of #xxx, thank you!
- Out of current scope for now, but welcome a focused PR.
- Canceled by requester / resolved in latest master.

The goal is not to be "formal," but to let newcomers immediately understand why it was closed.

---

## 2. Issue Handling Rules

### 2.1 First determine the issue type

Upon receiving an issue, categorize it into one of four types:

#### A. Bug report
Characteristics: Error thrown, page won't open, feature abnormal, state incorrect

Handling Method:
1. Reproduce / Determine if it's a known issue
2. If fixed: Reply + provide commit / PR number
3. If unfixed: Mark as pending, fix it yourself when necessary / wait for a PR
4. When closing, make sure to state clearly "where it was fixed"

**Recommended Reply Template:**
> Thanks for the feedback! This issue has been fixed in `PR #xx` / `commit xxx`. Please pull the latest master and try again. If there are still issues, feel free to continue the feedback.

---

#### B. Support / setup question
Characteristics: How to deploy, why Unauthorized, how to auto-sync, etc.

Handling Method:
1. Answer the question first
2. Give the shortest path (README / SKILL / Commands)
3. If the documentation can be optimized, note it down for future action
4. When closing, state "Question has been answered, if there are still issues feel free to reopen"

**Recommended Reply Template:**
> This issue is highly likely related to xxx. The latest version has made relevant fixes / documentation additions. You can try the latest master first; if there are still issues, feel free to reopen the issue.

---

#### C. Feature request
Characteristics: Wishing to support a new capability, new direction, new experience

Handling Method:
1. Explicitly state if interested
2. Do not mistakenly close it as "Fixed"
3. If not implementing it for now, also specify "Not doing this currently, but PRs / future discussions are welcome"

**Recommended Reply Template:**
> This is a great direction, and we are interested in this idea. However, it is not an established work item for the current phase. If you are willing to push this forward, PRs with a more focused scope are welcome, and we can discuss the implementation together.

---

#### D. Duplicate / canceled / absorbed
Characteristics: Repeated question, requester abandoned it themselves, absorbed by other issues

Handling Method:
1. Link to the corresponding issue / PR
2. Briefly explain the reason for closing
3. Keep it polite

---

## 3. PR Handling Rules

### 3.1 Check four things before Merging

#### 1) Does this PR solve a real problem?
- Is it a bug fix or just the author's personal preference?
- Does it correspond to an issue / user pain point?

#### 2) Is the scope of changes controllable?
- Small and focused → Lean towards merging
- Large and mixed → Request splitting / hold off

#### 3) Does it introduce extra maintenance burden?
- New dependencies
- New configurations
- New architecture
- New documentation costs

#### 4) Do README / changelog / release notes need syncing?
If it affects the user flow, the documentation must be synced.

---

### 3.2 PR results fall into three categories

#### A. Merge Directly
Suitable for:
- Small bug fixes
- Documentation corrections
- Explicit improvements to onboarding / stability

#### B. Close with thanks
Suitable for:
- Already fixed in master beforehand
- Duplicate PR
- Direction is good but not suitable right now

**Principle: Not merging ≠ Denying the contributor**

#### C. Request author to adjust and review again
Suitable for:
- Right idea, but changes are too large
- Mixed with unrelated content
- Needs to be broken down

---

### 3.3 When closing a PR, try to do three things

1. **Thank them first**
2. **Explain the reason**
3. **If possible, point out a direction that would be easier to accept in the future**

**Recommended Template:**
> Thanks for the PR — this is a thoughtful direction. We’re not merging it right now because xxx. If you’d like, a smaller / more focused PR around yyy would be much easier for us to review and land.

---

## 4. Release / Major Version Wrap-up Process

Applicable when:
- A round of bug fixes is complete
- A documentation refactoring is complete
- A feature bundle release (e.g., v1.0)

### Pre-release checklist
- [ ] Core features verified locally once (at least health / status / agents / set_state)
- [ ] Smoke tests pass
- [ ] README / SKILL / relevant docs synced
- [ ] CHANGELOG updated
- [ ] Relevant issues replied to / closed
- [ ] If there are contributors, consider acknowledging them in README / release notes
- [ ] Ensure the repository worktree is clean, no mistakenly committed files

### Release note structure recommendation
1. What is this version
2. 3-5 core changes
3. What practical impact it has on users
4. Quick experience method
5. Thank the contributors

---

## 5. README / Documentation Maintenance Rules

### 5.1 README must priority answer four questions
1. What is this?
2. Who is it for?
3. What's the fastest way to use it?
4. If I am an OpenClaw user, what is the shortest path?

### 5.2 Documentation Update Triggers
Sync README / docs when the following occurs:
- Default port changes
- Default installation method changes
- Core dependencies or paths change
- Onboarding flow changes
- Fixed high-frequency issues (especially regarding deployment / 401 / loading)

---

## 6. Community Relationship Maintenance

### 6.1 Three things to proactively do
- Acknowledge noticeable contributors in README or release notes
- Maintain respect for early contributors, even if PRs weren't merged
- Timely supplement explanations for misunderstandings / misjudgments

### 6.2 Which contributors are worth focusing on
Prioritize maintaining these individuals:
- Those who consistently submit multiple high-quality PRs
- Those who proactively supplement docs / onboarding
- Those who don't just fix their own issues, but help improve the project's completeness

---

## 7. Most Suitable Maintenance Strategy for Star-Office-UI at Current Stage

### Suitable for priority acceptance
- Bug fixes
- Onboarding improvements
- Documentation optimization
- Small and clear stability fixes
- Enhancements strongly related to OpenClaw / agent experience

### Handle with caution temporarily
- Large-scale refactoring
- Introducing heavy dependencies
- Changes tightly coupled to a specific personal workflow
- Large features with unclear boundaries

---

## 8. Maintenance Principles Star must remember

- Don't obfuscate closure reasons just to "appear enthusiastic"
- Don't close a feature request as a bug fix
- Don't forget to update documentation after merging
- Don't ignore early contributors
- A clean-looking repository is part of the product experience itself

---

## One-sentence version

> **Close small issues promptly, clarify boundaries for large issues; leave a trace upon every closure, and make every release a milestone.**
