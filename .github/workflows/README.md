# GitHub Actions Workflows

## UI Validation Workflow

The `ui-validation.yml` workflow automatically:

1. **Triggers on PR events** (opened, synchronized, reopened)
2. **Extracts commit messages** from the PR
3. **Generates Playwright tests** based on commit message content
4. **Runs UI validation tests** against the Jekyll site
5. **Comments on the PR** with test results

### How it works

1. When a PR is created or updated, the workflow:
   - Checks out the repository
   - Extracts all commit messages from the PR
   - Runs `scripts/generate_ui_tests.py` to analyze commit messages
   - Generates Playwright tests based on detected features (navigation, forms, links, etc.)
   - Runs the generated tests against a local Jekyll server
   - Posts results as a PR comment

### Test Generation Logic

The test generator analyzes commit messages for keywords:
- **navigation**: Tests menu, sidebar, nav elements
- **ui_change**: General UI validation
- **form**: Form input and submission tests
- **link**: Link functionality tests
- **content**: Content presence and readability
- **assignment**: Assignment-related page tests
- **syllabus**: Syllabus page validation

### Manual Trigger

You can also manually trigger the workflow from the Actions tab in GitHub.
