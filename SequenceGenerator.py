import sublime, sublime_plugin

class SequenceGeneratorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.status_message("You could set the sequence format to: {start:end:step} or {start:end} / {end}.")
        self.view.window().show_input_panel("Enter Sequence Format:", "10", self.on_done, self.on_change, None)
    def on_done(self, text):
        parameter = self.VerifyFormat(text)
        if not parameter:
            sublime.status_message("Your input is invalid.")
        else:
            self.view.run_command("generate_sequence", {"parameter": parameter})

    def on_change(self, text):
        if not self.VerifyFormat(text):
            sublime.status_message("Your input is invalid.")
        else:
            sublime.status_message("You could set the sequence format to: {start:end:step} or {start:end} / {end}.")
    def VerifyFormat(self, text):
        splits = text.replace(":", " ").split()
        length = len(splits)
        if not 1<=length<=3:
            return False
        for number in splits:
            if not number.isdigit():
                return False
        
        parameter = {'start':1, 'end':1, 'step':1}

        if length==1:
            parameter['end'] = int(splits[0]) + 1
        elif length==2:
            parameter['start'] = int(splits[0])
            parameter['end'] = int(splits[1]) + 1
        else:
            parameter['start'] = int(splits[0])
            parameter['end'] = int(splits[1]) + 1
            parameter['step'] = int(splits[2])

        return parameter

class GenerateSequenceCommand(sublime_plugin.TextCommand):

    def prepare_padding(self, edit, start):
        def append(string):
            string = str(string)
            self.view.insert(edit, start[0], string)
            start[0] += len(string)
            return sublime.Region(start[0]-len(string), start[0])
        return append

    def generate(self, edit, region, sequence, new_sel):
        contents = self.view.substr(region)
        self.view.erase(edit, region)
        padding_append = self.prepare_padding(edit, [region.begin()])
        for i, x in enumerate(sequence):
            splits = contents.split('#')
            for j, s in enumerate(splits):
                padding_append(s)
                if j!=len(splits)-1:
                    new_sel.append(padding_append(x))
            if i!=len(sequence)-1:
                padding_append('\n')

    def run(self, edit, parameter):
        sequence = list(range(parameter['start'], parameter['end'], parameter['step']))
        new_sel = []

        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)
                self.generate(edit, line, sequence, new_sel)
            else:
                self.generate(edit, region, sequence, new_sel)

        if len(new_sel) > 0:
            self.view.sel().clear()
            for r in new_sel:
                self.view.sel().add(r)

