# Contributing to WhisperTube

First off, thank you for considering contributing to WhisperTube! 🎉

## Development Process

1. Fork the repository
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

4. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

5. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style

We use several tools to maintain code quality:

- black for code formatting
- isort for import sorting
- flake8 for style checking
- mypy for type checking

These are automatically run via pre-commit hooks.

## Testing

- Write tests for new features using pytest
- Run the test suite:
  ```bash
  pytest
  ```

## Pull Request Process

1. Update the CHANGELOG.md with your changes
2. Ensure all tests pass
3. Update documentation if needed
4. Create a Pull Request with a clear description
5. Link any relevant issues

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Test updates
- chore: Routine tasks, maintenance

## Questions?

Feel free to open an issue for any questions!
