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
    def run(self, edit, parameter):
        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)
                line_contents = [ self.view.substr(line).replace('$', str(x)) for x in range(parameter['start'], parameter['end'], parameter['step'])]

                self.view.erase(edit, line)
                self.view.insert(edit, line.begin(), "\n".join(line_contents))
            else:
                region_contents = [ self.view.substr(region).replace('$', str(x)) for x in range(parameter['start'], parameter['end'], parameter['step'])]

                self.view.erase(edit, region)
                self.view.insert(edit, region.begin(), "\n".join(region_contents))
