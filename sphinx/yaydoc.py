from docutils.io import FileInput
from sphinx import environment

class YayFileInput(FileInput):

     def read(self):
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

def setup(app):
    setattr(environment, "FileInput", YayFileInput)

