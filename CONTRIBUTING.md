# Contributing Guidelines

Thank you for your interest in contributing to the E-Commerce Customer Support Chatbot! This document provides guidelines for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on code quality and functionality
- Help others learn and grow

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Provide a clear description of the bug
3. Include reproduction steps
4. Attach error logs and screenshots if applicable
5. Specify Python version and OS

**Bug Report Template:**
```
## Description
Clear description of the bug

## Steps to Reproduce
1. First step
2. Second step
3. Expected vs Actual behavior

## Environment
- Python: [version]
- OS: [operating system]
- Module: [affected module]
```

### Suggesting Enhancements

1. Use a clear title
2. Provide detailed description
3. Explain the motivation and use cases
4. List possible alternatives
5. Provide examples if applicable

### Pull Requests

#### Prerequisites

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Set up development environment
4. Make your changes
5. Test thoroughly

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/ecommerce-customer-support-chatbot.git
cd ecommerce-customer-support-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pylint flake8
```

#### Code Style Guidelines

1. **Python Style**: Follow PEP 8
   ```bash
   pylint chatbot/
   flake8 chatbot/
   ```

2. **Naming Conventions**
   - Classes: CamelCase
   - Functions/Methods: snake_case
   - Constants: UPPER_CASE
   - Private methods: _leading_underscore

3. **Docstrings**: Use Google-style docstrings
   ```python
   def function_name(arg1: str, arg2: int) -> bool:
       """Brief description.
       
       Longer description if needed.
       
       Args:
           arg1: Description of arg1.
           arg2: Description of arg2.
           
       Returns:
           Description of return value.
           
       Raises:
           ValueError: When invalid input is provided.
       """
   ```

4. **Comments**: Use inline comments for complex logic
   - Explain WHY, not WHAT
   - Keep comments concise

#### Testing Requirements

1. **Write tests** for new features
2. **Maintain coverage** (minimum 80%)
3. **Run tests** before submitting PR

```bash
# Run tests with coverage
pytest tests/ -v --cov=chatbot --cov-report=html
```

4. **Test checklist:**
   - Unit tests for new functions
   - Integration tests for features
   - Edge case handling
   - Error handling

#### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Code style changes
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance

**Examples:**
```
feat(intent_classifier): Add confidence scoring

Implement confidence scoring for intent classification.
Returns score between 0 and 1.

Fixes #123
```

#### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests are added/updated
- [ ] Documentation is updated
- [ ] No breaking changes
- [ ] Commit messages are clear
- [ ] PR description is complete
- [ ] All tests pass locally
- [ ] No linting errors

#### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #issue_number

## Testing Done
Describe testing performed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Self-review completed
- [ ] Tests added
- [ ] Documentation updated
```

## Project Structure

```
ecommerce-customer-support-chatbot/
├── chatbot/              # Core chatbot modules
│   ├── __init__.py
│   ├── api_wrapper.py   # REST API interface
│   ├── dialogue_system.py
│   ├── intent_classifier.py
│   ├── ir_based_qa.py
│   ├── logger.py
│   ├── order_tracker.py
│   └── response_generator.py
├── data/                # Configuration and data
│   ├── faq.json
│   ├── intents.json
│   └── sample_orders.json
├── tests/               # Test suite
│   ├── __init__.py
│   └── test_intent_classifier.py
├── .github/workflows/   # CI/CD pipelines
├── config.json          # Configuration file
├── main.py             # CLI interface
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## Coding Best Practices

### Do's
- ✓ Write clear, descriptive variable names
- ✓ Use type hints
- ✓ Handle exceptions gracefully
- ✓ Write comprehensive docstrings
- ✓ Use constants for magic values
- ✓ Test edge cases
- ✓ Keep functions small and focused

### Don'ts
- ✗ Use single-letter variables (except i, j for loops)
- ✗ Ignore exceptions
- ✗ Skip testing
- ✗ Make large functions
- ✗ Hardcode values
- ✗ Use global variables
- ✗ Commit commented code

## Review Process

1. **Initial Review**: Maintainer checks requirements
2. **Testing**: Automated tests run
3. **Code Review**: Team reviews code quality
4. **Feedback**: Comments and suggestions provided
5. **Revision**: Author makes requested changes
6. **Approval**: Maintainer approves and merges

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues for similar questions
- Join our community discussions

## License

By contributing to this project, you agree that your contributions will be licensed under its existing license.

## Acknowledgments

Thank you for contributing! Your efforts help make this project better for everyone.
