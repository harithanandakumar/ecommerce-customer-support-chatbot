# Contributing to E-commerce Customer Support Chatbot

Thank you for considering contributing to the e-commerce customer support chatbot project! We welcome contributions from the community and appreciate your interest in improving this project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Questions & Support](#questions--support)

## Code of Conduct

Our community is committed to providing a welcoming and inclusive environment:

- Be respectful and constructive in all interactions
- Welcome contributions from people of all backgrounds
- Maintain professional communication
- Report inappropriate behavior to maintainers
- Work collaboratively to resolve conflicts

## Getting Started

### Prerequisites
- Python 3.9+
- Git for version control
- Virtual environment tool (venv or conda)
- Text editor or IDE (VS Code, PyCharm, etc.)

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ecommerce-customer-support-chatbot.git
   cd ecommerce-customer-support-chatbot
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

5. **Verify installation**
   ```bash
   python -m pytest tests/  # Run test suite
   ```

## Development Workflow

### Branch Naming Convention

```
<type>/<feature-name>

Types:
- feature/: New feature
- fix/: Bug fix
- docs/: Documentation
- refactor/: Code refactoring
- test/: Test additions/modifications
- perf/: Performance improvements

Examples:
- feature/multilingual-support
- fix/order-cancellation-bug
- docs/api-documentation
- perf/query-optimization
```

### Creating a Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make incremental, focused commits
2. Write clear commit messages (see commit format below)
3. Add tests for new functionality
4. Update documentation as needed
5. Run tests locally before pushing

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Example:**
```
feat(intent-classifier): add multilingual support

Add support for detecting intent in Spanish, French, and German.
Implement language detection using nltk.detect.
Update training data to include samples in multiple languages.

Fixes #42
Closes #43
```

**Guidelines:**
- Use imperative mood ("add" not "added")
- Don't capitalize the subject line
- Limit subject to 50 characters
- Wrap body at 72 characters
- Reference issue numbers with "Fixes #123" or "Closes #123"

## Coding Standards

### Python Style Guide

We follow PEP 8 with these additional standards:

```python
# Type hints required
def process_order(order_id: str, customer_id: str) -> Dict[str, Any]:
    """Process customer order.
    
    Args:
        order_id: Unique order identifier
        customer_id: Unique customer identifier
        
    Returns:
        Dictionary containing order status and details
    """
    pass

# Docstrings required for all public functions
def validate_input(text: str) -> bool:
    """Validate customer input for security."""
    pass

# Code formatting with Black
python -m black .

# Linting with Flake8
flake8 chatbot/ --max-line-length=100

# Type checking with mypy
mypy chatbot/
```

### File Organization

```
chatbot/
├── __init__.py          # Package initialization
├── module_name.py       # Implementation
├── __tests__/
│   └── test_module.py   # Unit tests
└── README.md            # Module documentation
```

## Submitting Changes

### Pre-submission Checklist

- [ ] Code follows PEP 8 style guide
- [ ] All tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages follow format
- [ ] No unnecessary files committed
- [ ] Branch is up to date with main

### Push Your Changes

```bash
# Push to your fork
git push origin feature/your-feature-name
```

## Pull Request Process

### Creating a Pull Request

1. Go to GitHub and create Pull Request
2. Fill in PR template completely
3. Link related issues with "Fixes #123"
4. Provide clear description of changes
5. Add screenshots if UI changes

### PR Template

```markdown
## Description
Brief description of changes.

## Related Issue
Fixes #(issue number)

## Type of Change
- [ ] Bug fix (breaking change? yes/no)
- [ ] New feature (breaking change? yes/no)
- [ ] Documentation update
- [ ] Performance improvement

## Testing
Describe tests added/modified.

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No merge conflicts
```

### Review Process

- At least 1 maintainer review required
- Address all feedback
- Rebase before merging if needed
- Squash commits if requested
- Maintainers merge PR when approved

## Reporting Bugs

### Bug Report Template

```markdown
## Description
Clear description of the bug.

## Steps to Reproduce
1. Step 1
2. Step 2
3. See error

## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Environment
- Python version: 
- OS: 
- Chatbot version: 
- Browser (if applicable): 

## Logs/Output
```
Error traceback or output
```
```

### Bug Report Guidelines

- Search existing issues first
- Use descriptive titles
- Include reproducible steps
- Attach logs or screenshots
- Specify environment details

## Suggesting Enhancements

### Enhancement Template

```markdown
## Description
What enhancement would you like?

## Motivation
Why is this enhancement needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches?

## Additional Context
Any other information?
```

## Questions & Support

- **Questions**: Open Discussion in GitHub Discussions
COMMUNITY_GUIDELINES.md- **Features**: Open Issue with enhancement label
- **Security**: Email security@company.com (do not open public issue)
- **Email**: support@company.com

## Recognition

Contributors are recognized in:
- GitHub contributors page
- CHANGELOG.md
- Project website

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Additional Resources

- [Developer Guide](DEVELOPER_GUIDE.md)
- [Architecture Overview](ARCHITECTURE.md)
- [API Specification](API_SPEC.md)
- [Security Guidelines](SECURITY.md)
- [Project Roadmap](ADVANCED_FEATURES_ROADMAP.md)

---

Thank you for contributing to making this chatbot better!
