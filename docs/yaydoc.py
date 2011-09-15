import os, fnmatch
from docutils.io import FileInput
from sphinx.util import get_matching_files
from sphinx.util.matching import compile_matchers
from sphinx import environment

class YayFileInput(FileInput):

     def read(self):
         if self.source_path.endswith(".rst"):
             return FileInput.read(self)

         data = FileInput.read(self).split("\n")
         newdata = []

         line = data.pop(0)
         while data:
             if len(line.strip()) == 0:
                 newdata.append('')
                 line = data.pop(0)

             elif line.startswith("#"):
                 while data and line.startswith('#'):
                     newdata.append(line[2:])
                     line = data.pop(0)

             else:
                 newdata.extend(['', '::', ''])

                 while data and not line.startswith('#'):
                     newdata.append('    ' + line)
                     line = data.pop(0)

                 newdata.append('')

         return "\n".join(newdata)


old_doc2path = environment.BuildEnvironment.doc2path

def doc2path(self, docname, base=True, suffix=None):
    """
    Return the filename for the document name.
    """
    if docname.startswith(":cfg:"):
        docname = os.path.join(self.srcdir, "..", docname[5:])

    if suffix:
        return old_doc2path(self, docname, base, suffix)

    for suffix in (".yay", ".rst"):
        path = old_doc2path(self, docname, base, suffix)
        if os.path.exists(path):
            break

    return path


def get_matching_docs(dirname, exclude_matchers=()):
    """
    Get all file names (without suffix) matching a suffix in a
    directory, recursively.

    Exclude files and dirs matching a pattern in *exclude_patterns*.
    """
    for filename in get_matching_files(dirname, exclude_matchers):
        if not fnmatch.fnmatch(filename, "*.rst"):
            continue
        yield filename[:-4]

    for filename in get_matching_files(dirname+"/..", exclude_matchers):
        if not fnmatch.fnmatch(filename, "*.yay"):
            continue
        yield ':cfg:' + filename[:-4]


def find_files(self, config):
    """
    Find all source files in the source dir and put them in self.found_docs.
    """
    matchers = compile_matchers(
        config.exclude_patterns[:] +
        config.exclude_trees +
        [d + ".rst" for d in config.unused_docs] +
        [d + ".yay" for d in config.unused_docs] +
        ['**/' + d for d in config.exclude_dirnames] +
        ['**/_sources']
    )
    self.found_docs = set(get_matching_docs(
        self.srcdir, exclude_matchers=matchers))


def setup(app):
    setattr(environment, "FileInput", YayFileInput)

    environment.BuildEnvironment.doc2path = doc2path
    environment.BuildEnvironment.find_files = find_files

