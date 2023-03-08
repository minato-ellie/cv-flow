import nox


@nox.session
def tests(session):
    session.install('poetry')
    session.run('poetry', 'export', '--with', 'test', '--without-hashes',
                '--format=requirements.txt', '--output=requirements-test.txt')
    session.install('-r', 'requirements-test.txt')

    session.run('pytest', '--cov=cvflow', '--cov-report=term-missing', '--cov-report=html')
    session.notify('coverage')


@nox.session
def lint(session):
    session.install('toml', 'yapf', 'flake8', 'pyproject-flake8')
    session.run('yapf', '--in-place', '--recursive', './cvflow')
    session.run('flake8', 'cvflow')


@nox.session
def build_docs(session):
    session.install('pdoc')
    session.run('pdoc', '--html', '--output-dir', 'docs', '-d', 'google', 'cvflow')
