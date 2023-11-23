
class Component:
    def __init__(self):
        pass

class ECS:
    def __init__(self):
        self.entitie_masks = {}
        # self.entities = {}
        self.components = {}
        self.systems = []
        self.entity_count = 0

        self._add_component_types()
    
    def _add_component_types(self):
        for i, cls in enumerate(Component.__subclasses__()):
            self.components[cls.__name__] = {}
            self.entitie_masks[1 << i] = (cls.__name__, [])

    def spawn(self, id, components):
        self.entity_count += 1
        self.entitie_masks[id] = 0
        for component in components:
            self.entitie_masks[id] |= 1 << component.__class__.__name__
            self.components[component.__class__.__name__][id] = component
