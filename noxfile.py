import nox


@nox.session
def tests(session):
    pass


@nox.session
def lint(session):
    session.install('toml', 'yapf', 'flake8', 'pyproject-flake8')
    session.run('yapf', '--in-place', '--recursive', './package_name')
    session.run('flake8', 'package_name')


@nox.session
def build_docs(session):
    session.install('pdoc')
    session.run('pdoc', '--html', '--output-dir', 'docs', '-d', 'google', 'package_name')
