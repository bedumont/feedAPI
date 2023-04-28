class Reaction(object):
    def __init__(self, id, ip, target, value, comment):
        self.id = id
        self.ip = ip
        self.target = target
        self.value = value
        self.comment = comment

    def __repr__(self):
        return '<Reaction(id={self.id} source={self.ip} target={self.target} datetime={self.datetime})>'.format(self=self)
