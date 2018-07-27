import re
import subprocess

from deoplete.util import globruntime
from .base import Base


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'zsh'
        self.mark = '[zsh]'
        self.filetypes = ['zsh']
        self.input_pattern = '[^. \t0-9]\.\w*'
        self.rank = 500
        self.__executable_zsh = self.vim.call('executable', 'zsh')

    def get_complete_position(self, context):
        m = re.search(r'\S+$', context['input'])
        if not m:
            return -1
        return m.start()

    def gather_candidates(self, context):
        capture = globruntime(self.vim.options['runtimepath'], 'bin/capture.zsh')
        if not self.__executable_zsh or not capture or not context['input']:
            return []

        result = []
        try:
            for pieces in [x.decode(context['encoding']).split(' -- ')
                           for x in subprocess.check_output(
                                   ['zsh', capture[0], context['input']]
                                   , timeout=0.5).splitlines()]:
                if len(pieces) > 1:
                    result.append({ 'word': pieces[0], 'menu': pieces[1] })
                else:
                    result.append({ 'word': pieces[0] })
        except subprocess.SubprocessError:
            return []
        return result
