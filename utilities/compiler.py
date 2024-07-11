from hardware.asm import ASM

class Compiler:
    """An utility class to create programs from an ASM code"""
    @classmethod
    def compile(self, name, instructions):
        """Compile code and return a new program"""
        expanded = []
        for i in instructions:
            if isinstance(i, list):
                ## is a list of instructions
                expanded.extend(i)
            else:
                ## a single instr (a String)
                expanded.append(i)

        ## Validate that there are no EXIT instructions, as
        ## EXIT should be the last instruction only.
        expanded = [i for i in expanded if not ASM.is_EXIT(i)]

        ## now add EXIT as the last instruction, if it was
        ## added by the user, we removed it in the previous step
        expanded.append(ASM.EXIT())

        # Verify that all are valid instructions, or fail
        for e in expanded:
            if not ASM.is_valid(e):
                raise SyntaxError("Invalid instruction: " + e)
        # Create a program and return it
        return Program(name, expanded)


class Program():
    """A program, as a simplification of what is stored in a persistent drive."""
    def __init__(self, name, instructions):
        """PRECONDITION: The instructions are valid"""
        self._name = name
        self._instructions = instructions

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)
