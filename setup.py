from setuptools import setup

setup(name='sticker-workbench',
      version='0.1.0',
      description='Workbench for sticker',
      url='https://github.com/stickeritis/sticker-workbench',
      author='Daniël de Kok',
      author_email='me@danieldk.eu',
      license='BlueOak-1.0.0',
      # Both tests_require and install_requires need 'sticker'.
      # However, that currently does not work. Missing distinfo?
      tests_require=[
          'pytest',
          'somajo'
      ],
      install_requires=[
          'somajo'
      ],
      packages=['sticker_workbench'],
      scripts=[])
