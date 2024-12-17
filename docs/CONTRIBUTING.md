# Contributing to Investment App Demo

Thank you for your interest in contributing to the **Investment App Demo**! Before you begin, please read the guidelines below to ensure your contributions align with the purpose and scope of this project.

---

## Purpose of the Project

The **Investment App Demo** is a **technical demonstration** of backend development skills, showcasing the use of technologies like FastAPI, SQLAlchemy, and Docker.  
- **This project is not under active maintenance**, and its primary purpose is to serve as a reference for learning or extending backend features.
- Contributions are welcome but will be reviewed based on relevance and availability of time.

---

## Contribution Guidelines

### Scope of Contributions

Contributions should align with the project's purpose. Examples of acceptable contributions include:

1. **Bug Fixes**:  
   - Fixing existing functionality without altering the project's core objectives.

2. **Documentation Improvements**:  
   - Enhancing the clarity or completeness of documentation, such as the README or code comments.

3. **Small Feature Enhancements**:  
   - Adding minor, self-contained features that demonstrate extensibility or improve usability.

---

### How to Contribute

1. **Fork the Repository**:  
   - Create a fork of this repository on your GitHub account.

2. **Clone Your Fork**:  
   ```bash
   git clone https://github.com/and-reis/investment-app-demo.git
   cd investment-app-demo
   ```

3. **Create a Feature Branch**:  
   - Use descriptive names for your branches:
     ```bash
     git checkout -b feature/my-feature-name
     ```

4. **Make Your Changes**:  
   - Ensure your code adheres to the PEP 8 style guide for Python.
   - Add relevant tests for new functionality or bug fixes.

5. **Run Tests**:  
   - Verify that your changes do not break the existing functionality:
     ```bash
     pytest  # For local testing
     docker-compose up --build  # For testing with Docker
     ```

6. **Commit Your Changes**:  
   - Use a meaningful commit message:
     ```bash
     git add .
     git commit -m "Fix: Resolved issue with XYZ"
     ```

7. **Push to Your Fork**:  
   ```bash
   git push origin feature/my-feature-name
   ```

8. **Create a Pull Request**:  
   - Go to the original repository and submit a pull request. Include:
     - A clear description of the changes.
     - Links to related issues (if any).

---

### Reporting Issues

If you encounter a bug or have a feature request, please **create an issue** with the following details:

- A clear and concise description of the issue or feature.
- Steps to reproduce the issue (if applicable).
- Suggestions for a solution (optional).

---

## Notes

- This project is **not actively maintained**, and responses to issues or pull requests may be delayed.
- For users interested in deploying or extending the application, consider forking the repository and customizing it to your needs.