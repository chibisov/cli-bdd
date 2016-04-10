import os
import threading

from invoke import run, task, util


@task(name='deploy-docs')
def deploy_docs():
    """
    Based on https://gist.github.com/domenic/ec8b0fc8ab45f39403dd
    """
    run('rm -rf ./site/')
    build_docs()
    with util.cd('./site/'):
        run('git init')
        run('echo ".*pyc" > .gitignore')
        run('git config user.name "Travis CI"')
        run('git config user.email "%s"' % os.environ['EMAIL'])
        run('git add .')
        run('git commit -m "Deploy to GitHub Pages"')
        run(
            'git push --force --quiet "https://{GH_TOKEN}@{GH_REF}" '
            'master:gh-pages > /dev/null 2>&1'.format(
                GH_TOKEN=os.environ['GH_TOKEN'],
                GH_REF=os.environ['GH_REF'],
            )
        )


@task(name='build-docs')
def build_docs():
    generate_api_reference()
    run('mkdocs build')


@task(name='serve-docs')
def serve_docs():
    generate_api_reference()

    target_cmd = (
        'watchmedo shell-command -R -c '
        '"invoke generate-api-reference" cli_bdd docs'
    )
    p = threading.Thread(target=run, args=(target_cmd,))
    p.daemon = True
    p.start()

    run('mkdocs serve')


@task(name='generate-api-reference')
def generate_api_reference():
    from docs.generator import generate_api_reference
    print 'Generating API reference'
    generate_api_reference()
