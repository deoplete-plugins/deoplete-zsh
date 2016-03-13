import string

from deoplete.sources.base import Base


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'zsh'
        self.mark = '[zsh]'
        self.filetypes = ['zsh']
        self.input_pattern = '[^. \t0-9]\.\w*'
        self.rank = 500

        self.candidates = dict.fromkeys(string.ascii_lowercase, None)

    def get_complete_position(self, context):
        return self.vim.call('zsh_completion#Complete', 1, 0)

    def gather_candidates(self, context):
        # Get current first letter input and caching
        if context['input'][0] and context['input'][0] in string.ascii_lowercase:
            f_input = context['input'][0]

            if self.candidates[f_input]:
                return self.candidates[f_input]
            elif f_input in string.ascii_lowercase:
                self.candidates[f_input] = \
                        self.vim.call('zsh_completion#Complete', 0, 0)
                return self.candidates[f_input]

        else:
            return []
