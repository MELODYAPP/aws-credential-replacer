#!/usr/bin/env python
import os
import sys

import click
from credstash import getSecret, listSecrets
from jinja2 import Environment, FileSystemLoader


def render_with_credentials(file, region, context):
    """Render file argument with credstash credentials

    Load file as jinja2 template and render it with context where keys are 
    credstash keys and values are credstash values

    Args:
        file (str): jinja2 template file path

    Returns:
        str: Rendered string

    """
    env = Environment(loader=FileSystemLoader(os.path.dirname(file)))
    template = env.get_template(os.path.basename(file))

    secrets = {
        secret['name']: getSecret(
            secret['name'], region=region, context=context
        ) for secret in listSecrets(region=region)}
    return template.render(**secrets)


def parse_key_value(ctx, param, value):
    d = {
        key: value for key, value 
        in map(lambda s: s.split('='), value)
    }
    return d


@click.command()
@click.option('-r', default='us-east-1', help='DynamoDB region')
@click.argument('file', nargs=1)
@click.argument('context', nargs=-1, callback=parse_key_value, 
                help='Encryption context key/value pairs to pass as `key=value`')
def main(r, file, context=None):
    """Output rendered template

    Args:
        file (str): jinja2 template file path

    """
    sys.stdout.write(render_with_credentials(file, r, context))


if __name__ == '__main__':
    main()
