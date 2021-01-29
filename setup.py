import distutils.cmd
import distutils.command.build
import distutils.spawn
import glob
import os
import sys

from setuptools import setup, find_packages


class build_i18n(distutils.cmd.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def build_lib(self):
        pass

    def run(self):
        data_files = self.distribution.data_files

        with open('po/POTFILES.in') as in_fp:
            with open('po/POTFILES.in.tmp', 'w') as out_fp:
                for line in in_fp:
                    if line.startswith('['):
                        continue
                    out_fp.write('../' + line)

        os.chdir('po')
        distutils.spawn.spawn([
            'xgettext',
            '--directory=.',
            '--add-comments',
            '--from-code=UTF-8',
            '--keyword=pgettext:1c,2',
            '--output=ubuntuwslctl.pot',
            '--files-from=POTFILES.in.tmp',
        ])
        os.chdir('..')
        os.unlink('po/POTFILES.in.tmp')

        for po_file in glob.glob("po/*.po"):
            lang = os.path.basename(po_file[:-3])
            mo_dir = os.path.join("build", "mo", lang, "LC_MESSAGES")
            mo_file = os.path.join(mo_dir, "ubuntuwslctl.mo")
            if not os.path.exists(mo_dir):
                os.makedirs(mo_dir)
            distutils.spawn.spawn(["msgfmt", "-o", mo_file, po_file])
            targetpath = os.path.join("share/locale", lang, "LC_MESSAGES")
            data_files.append((targetpath, (mo_file,)))


class build(distutils.command.build.build):

    sub_commands = distutils.command.build.build.sub_commands + [
        ("build_i18n", None)]


# nothing to clean, quit
if sys.argv[-1] == 'clean':
    os.system('rm -rf build')
    sys.exit()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='ubuntuwslctl',
      version='0.27.1',
      description="Ubuntu WSL Utility to manage Ubuntu WSL settings",
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords=[
          'ubuntu',
          'wsl',
      ],
      author='Patrick Wu',
      author_email='patrick.wu@canonical.com',
      url='https://github.com/canonical/ubuntu-wsl-integration',
      license="GPLv3+",
      packages=find_packages(exclude=["tests"]),
      entry_points={
          'console_scripts': [
              'ubuntuwsl = ubuntuwslctl.main:main'
          ],
      },
      install_requires=[
          'setuptools',
      ],
      data_files=[],
      cmdclass={
          'build': build,
          'build_i18n': build_i18n,
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Utilities',
      ],
      )
