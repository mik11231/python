"""Shared Intcode computer for Advent of Code 2019."""

from collections import defaultdict, deque


class IntcodeComputer:
    """Stateful Intcode VM supporting pause-on-input/output and relative base."""

    def __init__(self, program):
        """
        Run `__init__` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: self, program.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        self.mem = defaultdict(int)
        for i, v in enumerate(program):
            self.mem[i] = v
        self.ip = 0
        self.rb = 0
        self.halted = False

    def _get(self, mode, k):
        """
        Run `_get` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: self, mode, k.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        if mode == 0:
            return self.mem[self.mem[self.ip + k]]
        if mode == 1:
            return self.mem[self.ip + k]
        if mode == 2:
            return self.mem[self.rb + self.mem[self.ip + k]]
        raise ValueError(mode)

    def _addr(self, mode, k):
        """
        Run `_addr` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: self, mode, k.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        if mode == 0:
            return self.mem[self.ip + k]
        if mode == 2:
            return self.rb + self.mem[self.ip + k]
        raise ValueError(mode)

    def run(self, inputs=(), stop_on_output=False):
        """
        Run `run` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: self, inputs, stop_on_output.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        q = deque(inputs)
        outputs = []

        while not self.halted:
            op = self.mem[self.ip] % 100
            m1 = (self.mem[self.ip] // 100) % 10
            m2 = (self.mem[self.ip] // 1000) % 10
            m3 = (self.mem[self.ip] // 10000) % 10

            if op == 99:
                self.halted = True
                break
            if op in (1, 2, 7, 8):
                a = self._get(m1, 1)
                b = self._get(m2, 2)
                c = self._addr(m3, 3)
                if op == 1:
                    self.mem[c] = a + b
                elif op == 2:
                    self.mem[c] = a * b
                elif op == 7:
                    self.mem[c] = 1 if a < b else 0
                else:
                    self.mem[c] = 1 if a == b else 0
                self.ip += 4
            elif op == 3:
                if not q:
                    return outputs, False  # waiting for input
                self.mem[self._addr(m1, 1)] = q.popleft()
                self.ip += 2
            elif op == 4:
                outputs.append(self._get(m1, 1))
                self.ip += 2
                if stop_on_output:
                    return outputs, False
            elif op in (5, 6):
                a = self._get(m1, 1)
                b = self._get(m2, 2)
                self.ip = b if ((op == 5 and a != 0) or (op == 6 and a == 0)) else self.ip + 3
            elif op == 9:
                self.rb += self._get(m1, 1)
                self.ip += 2
            else:
                raise ValueError(f'bad opcode {op}')

        return outputs, True
