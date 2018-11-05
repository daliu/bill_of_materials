#!venv/bin/python

class Part(object):
    """
        Parts are elements of an assembly.
        They can have a color, but default with None unless specified.
        They can have a model, but default to "Generic" unless specified.
        By default, Parts have no parents or children.
    """
    def __init__(self, id_num, name, color="None",
                 model="Generic", parent=None, children=None):
        self.id = id_num
        self.name = name
        self.color = color
        self.model = model
        self.parent = parent
        self.children = children

    # Accessor Functions

    def get_id():
        return self.id

    def get_name():
        return self.name

    def is_parent():
        return self.children is not None

    def is_child():
        return self.parent is not None

    def get_children():
        return self.children

    def jsonify():
        return {self.id, self.name,
                self.color, self.model,
                self.parent, self.children}


class Assembly(Part):
    """
        Assembly has subassemblies, component parts, and regular parts.
        An assembly can add, remove, or change parts. 
    """
    def __init__(self, parts_list):
        self.parts_list = parts_list
        self.sub_assemblies = self.get_subs(parts_list)

    def get_subs(past_list):
        """
        Returns subassemblies within this assembly
        """
        sub_assems = []
        for part in parts_list:
            if part.is_parent:
                pass

    def make_parts():
        pass


    def jsonify():
        pass
