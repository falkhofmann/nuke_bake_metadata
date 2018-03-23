"""Builder function for rez."""

import os
import os.path
import shutil


def build(source_path, build_path, install_path, targets):
    package = os.environ['REZ_BUILD_PROJECT_NAME']

    def _build():
        src_py = os.path.join(source_path, package)
        dest_py = os.path.join(build_path, package)

        if not os.path.exists(dest_py):
            shutil.copytree(src_py, dest_py)

    def _install():
        for name in ( package,):
            src = os.path.join(build_path, name)
            dest = os.path.join(install_path, name)

            if os.path.exists(dest):
                shutil.rmtree(dest)

            shutil.copytree(src, dest)

    _build()

    if "install" in (targets or []):
        _install()
