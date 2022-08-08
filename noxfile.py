"""Nox file to run the dependencies."""
import nox

package = "3DMotionModeller"
nox.options.sessions = "lint", "tests", "coverage"
locations = "tests", "dynamics3d"


# cache configuration
nox.options.envdir = ".cache"
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=["3.8"])
def lint(session):
    """Run linter."""
    args = session.posargs or locations
    session.install(
        "flake8==3.9.2",
        "bandit==1.7.2",
        "flake8-bandit==2.1.2",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=["3.8"])
def tests(session):
    """Run the test suite."""
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("coverage[toml]", "pytest")
    session.run("pytest", "--disable-pytest-warnings")


@nox.session(python=["3.8"])
def coverage(session):
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("coverage[toml]", "pytest", "pytest-cov", "mock")
    session.run("pytest", *args)
