# Playwright UI Validation Tests

This directory contains UI validation tests for the Software Verification and Validation course site.

## Structure

- `generated/` - Auto-generated tests from PR commit messages (created by CI/CD)
- Manual tests can be added here as `.spec.js` files

## Running Tests Locally

### Prerequisites

```bash
npm install
npx playwright install --with-deps
```

### Start Jekyll Server

```bash
bundle exec jekyll serve
```

### Run Tests

```bash
# Run all tests
npm test

# Run with UI mode
npm run test:ui

# Run in debug mode
npm run test:debug
```

## Test Generation

Tests are automatically generated from PR commit messages by the GitHub Actions workflow. The generator analyzes commit messages for keywords and creates appropriate UI validation tests.

### Supported Keywords

- `navigation`, `menu`, `sidebar` → Navigation tests
- `ui change`, `update page`, `add component` → UI change tests
- `form`, `input`, `submit` → Form validation tests
- `link`, `href`, `url` → Link functionality tests
- `content`, `article`, `post` → Content presence tests
- `assignment`, `due date` → Assignment page tests
- `syllabus`, `schedule` → Syllabus page tests

## Manual Test Creation

You can create manual tests by adding `.spec.js` files in this directory:

```javascript
import { test, expect } from '@playwright/test';

test('My custom test', async ({ page }) => {
  await page.goto('/');
  // Your test code here
});
```
