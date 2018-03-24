name = "nuke_bake_metadata"

version = "0.1.0"

authors = ["Falk Hofmann"]

homepage = "https://gitlab.com/falkolon/nuke_bake_metadata"

description = \
    """
    Bake framebased metadata into Nuke Knobs.
    """

requires = [
    "python-2.7",
    "qt_py"
]


def commands():
    env.PYTHONPATH.append("{root}/{name}".format(name=name))
