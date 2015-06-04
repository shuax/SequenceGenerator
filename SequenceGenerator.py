import sublime, sublime_plugin

class SequenceGeneratorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.status_message("You could set the sequence format to: {start:step} or {start}.")
        self.view.window().show_input_panel("Enter Sequence Format:", "1", self.on_done, self.on_change, None)
    def on_done(self, text):
        parameter = self.VerifyFormat(text)
        if not parameter:
            sublime.error_message("Your input is invalid.")
        else:
            self.view.run_command("generate_sequence", {"parameter": parameter})

    def on_change(self, text):
        if not self.VerifyFormat(text):
            sublime.status_message("Your input is invalid.")
        else:
            sublime.status_message("You could set the sequence format to: {start:step} or {start}.")
    def VerifyFormat(self, text):
        splits = text.replace(":", " ").split()
        length = len(splits)
        if not 1<=length<=2:
            return False
        for number in splits:
            try:
                number = int(number)
            except:
                return False

        parameter = {'start':1, 'step':1}

        if length==1:
            parameter['start'] = int(splits[0])
        else:
            parameter['start'] = int(splits[0])
            parameter['step'] = int(splits[1])

        return parameter

class GenerateSequenceCommand(sublime_plugin.TextCommand):
    def run(self, edit, parameter):
        new_sel = []
        for region in self.view.sel():
            self.view.erase(edit, region)

            sequence = str(parameter['start'])
            self.view.insert(edit, region.begin(), sequence)

            new_sel.append(sublime.Region(region.begin(), region.begin() + len(sequence)))

            parameter['start'] += parameter['step']

        if len(new_sel) > 0:
            self.view.sel().clear()
            for r in new_sel:
                self.view.sel().add(r)

