"""
Module responsible for parsing the input file and creating the
dictionary representation of the Uppaal XML model.
"""
import xml.etree.ElementTree as ET
import re


class UppaalParser:
    """
    Represents an XML parser for an Uppaal model.
    """

    def __init__(self, filename):
        self.parser = ET.XMLPullParser(['start', 'end'])
        self.parser.feed(open(filename, encoding="utf-8").read())

    def parse(self):
        """
        Parses the XML file in templates of the form:
        {
            "name": name,
            "states": states,
            "transitions": transitions,
            "clocks": clocks,
        }
        And returns a dictionary in the form:
        {
            "templates": templates,
            "clocks": clocks,
        }
        """
        allclocks = []
        templates = []
        for event, elem in self.parser.read_events():
            if event == 'end':
                if elem.tag == 'template':
                    states, transitions, clocks = self.parse_template(elem)
                    templates.append({
                        'name': elem.find('name').text,
                        'states': states,
                        'matrix': transitions,
                    })
                    allclocks += clocks
                if elem.tag == 'nta':
                    global_declaration = elem.find('declaration')
                    global_clocks = self.parse_clocks(global_declaration)
                    allclocks += global_clocks
        return {
            "templates": templates,
            "clocks": allclocks,
        }

    def parse_template(self, template):
        """
        Parses a template and returns a list of states, transitions and clocks.
        """
        states = {}
        declaration = template.find('declaration')
        clocks = self.parse_clocks(declaration)
        for child in template:
            if child.tag == 'location':
                state = self.parse_location(child)
                states[state['id']] = state
        transitions = {}
        for child in template:
            if child.tag == 'transition':
                transition = self.parse_transition(child)
                if transition['source'] not in transitions:
                    transitions[transition['source']] = {}
                transitions[transition['source']
                            ][transition["target"]] = transition
        return states, transitions, clocks

    def parse_clocks(self, declaration):
        """
        Parses a declaration and returns a list of clocks.
        """
        clocks = []
        # Match clock declarations of the form "clock c1, c2, c3;"
        for line in declaration.text.splitlines():
            match = re.match(r"clock\s+(.+);", line)
            if match:
                clocks += match.group(1).split(',')
        return clocks

    def parse_location(self, location):
        """
        Parses a location and returns a dictionary in the form:
        {
            "name": name,
            "id": id,
            "invariant": invariant,
        }
        """
        name = ""
        if location.find('name') is not None:
            name = location.find('name').text
        ref = location.get('id')
        label = location.find('label')
        invariant = None
        if label is not None and label.get('kind') == 'invariant':
            invariant = label.text
        return {"name": name, "id": ref, "invariant": invariant}

    def parse_transition(self, transition):
        """
        Parses a transition and returns a dictionary in the form:
        {
            "source": source,
            "target": target,
            "synchronization": synchronization,
            "assignment": assignment,
            "guard": guard,
            "select": select,
        }
        """
        source = transition.find('source').get('ref')
        target = transition.find('target').get('ref')
        synchronization = None
        assignment = None
        guard = None
        select = None
        for label in transition.findall('label'):
            if label.get('kind') == 'synchronisation':
                synchronization = label.text
            if label.get('kind') == 'assignment':
                assignment = label.text
            if label.get('kind') == 'guard':
                guard = label.text
            if label.get('kind') == 'select':
                select = label.text

        return {
            "source": source,
            "target": target,
            "synchronization": synchronization,
            "assignment": assignment,
            "guard": guard,
            "select": select,
        }



