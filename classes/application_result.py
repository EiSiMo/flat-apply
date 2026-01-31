from language import _

class ApplicationResult:
    def __init__(self, success: bool, message: str=""):
        self.success = success
        self.message = message

    def __str__(self):
        string = ""
        if self.success:
            string += _("application_success")
        else:
            string += _("application_failed")

        if self.message:
            string += "\n"
            string += self.message
        return string

    def __repr__(self):
        string = ""
        if self.success:
            string += "success"
        else:
            string += "failed"

        if self.message:
            string += ": "
            string += self.message
        return string