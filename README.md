# Playwright Python Website Testing Framework

A modern test automation framework using Playwright and Python for website testing, featuring Behavior Driven Development (BDD).

## Features

- Behavior Driven Development with pytest-bdd
- Page Object Model pattern for maintainable test structure
- Strong typing with Python type hints
- Modular test organization (e2e, components, features)
- Configuration management via .env
- Utility functions for common test operations
- Cross-browser testing support
- HTML reporting
- Local test server using Flask

## Project Structure

```
/playwright-python-website
├── config/               # Test configurations
├── page_objects/        # Page object models
├── tests/               # Test files
│   ├── e2e/            # End-to-end tests
│   ├── components/     # Component tests
│   └── features/       # BDD feature files and steps
│       ├── steps/      # Step definitions
│       └── conftest.py # BDD fixtures
├── utils/              # Helper utilities
└── reports/           # Test execution reports
```

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory with the following settings:

```ini
BROWSER=chromium
HEADLESS=false
SLOW_MO=0
BASE_URL=http://localhost:5000
VIEWPORT_WIDTH=1280
VIEWPORT_HEIGHT=720
TIMEOUT=30000
```

## Running Tests

1. Start the local test server:
```bash
python app.py
```

2. Run all tests:
```bash
pytest
```

3. Run specific test file:
```bash
pytest tests/e2e/test_example.py -v
```

4. Run BDD feature tests:
```bash
pytest tests/features/steps/ -v
```

5. Generate HTML report:
```bash
pytest --html=reports/report.html
```

## Test Structure

- **Feature Files**: Gherkin syntax for BDD scenarios
- **Step Definitions**: Python implementations of BDD steps
- **Page Objects**: Reusable functions for page interactions
- **E2E Tests**: End-to-end test scenarios
- **Component Tests**: Individual component testing
- **Utilities**: Helper functions for common operations

## Best Practices

1. **BDD Implementation**
   - Write clear, descriptive feature files
   - Use reusable step definitions
   - Implement strong fixtures
   - Follow Given-When-Then pattern

2. **Code Style**
   - Use functional programming patterns
   - Follow snake_case naming convention
   - Include proper type hints (Dict, Any, Callable)
   - Write modular, reusable code

3. **Error Handling**
   - Implement strong error handling
   - Use proper timeouts and waits
   - Handle network requests properly
   - Include descriptive error messages
   - Handle CAPTCHA and rate limiting gracefully

4. **Documentation**
   - Add docstrings to all functions
   - Document test scenarios clearly
   - Keep README up to date
   - Generate and maintain test reports
   - Document lessons learned

## Contributing

1. Follow the established code style
2. Add proper documentation
3. Write tests for new features
4. Update README as needed
5. Document lessons learned

## Tech Stack

- Python 3.8+
- Playwright 1.42.0
- pytest 7.4.4
- pytest-playwright 0.4.3
- pytest-bdd 7.1.2
- Flask 3.0.2
- pytest-html 4.1.1
- python-dotenv 1.0.0
- parse 1.20.1
- parse-type 0.6.2

## Additional Resources

- [LessonLearned.md](./LessonLearned.md) - Detailed documentation of implementation insights and best practices
- [pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/) - Official pytest-bdd documentation
- [Playwright Documentation](https://playwright.dev/python/) - Official Playwright Python documentation
