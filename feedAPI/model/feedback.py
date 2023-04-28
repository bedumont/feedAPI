class Feedback(object):
    def __init__(self, id, ip, text, grade, datetime):
        self.id = id
        self.ip = ip
        self.text = text
        self.grade = grade
        self.grade = datetime

    def __repr__(self):
        # Represents a feedback as a string for logging
        return '<Feedback(id={self.id} source={self.ip} datetime={self.datetime})>'.format(self=self)
