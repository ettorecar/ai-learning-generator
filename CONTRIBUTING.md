# Contributing to AI-Powered E-Learning Generator

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs
- Clearly describe the issue including steps to reproduce
- Include information about your environment (OS, Python version, etc.)

### Suggesting Features
- Open an issue with the `enhancement` label
- Provide a clear description of the feature and its use case
- Discuss the feature before starting implementation

### Pull Requests

1. **Fork the repository** and create your feature branch from `main`
2. **Write clear commit messages** describing your changes
3. **Test your changes** thoroughly
4. **Update documentation** if necessary
5. **Submit a pull request** with a clear description

#### Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build
2. Update the README.md with details of changes to the interface, if applicable
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent
4. Your pull request will be reviewed by maintainers

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

## Testing

- Test your changes manually before submitting
- Include test cases for new features
- Ensure existing functionality is not broken

## Commit Message Format

Use clear and descriptive commit messages:
- `feat: add new quiz type support`
- `fix: resolve API timeout issue`
- `docs: update installation instructions`
- `style: improve CSS responsiveness`

## Questions?

If you have questions about contributing, feel free to open an issue or reach out to the maintainers.

Thank you for contributing! 🎉
