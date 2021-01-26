# Implementing the Trickle algorithm

from random import random


class Node:
    def __init__(self, id_number, i_min, i_max, k, i, tau, c, messages, ld, md):
        self.id_number = id_number  # identifies the node, Int
        self.i_min = i_min  # minimum of interval I
        self.i_max = i_max  # maximum of interval I
        self.k = k  # redundancy indicator k
        self.i = i  # current value of I
        self.tau = tau  # at what time does the node transfer its version
        self.c = c  # number of neighbouring nodes with the same version
        # mailbox, messages from other nodes will be stored in this list as tuples (id_number, ld, md)
        self.messages = messages
        self.ld = ld  # LD, contains the current fragments of software
        self.md = md  # MD, contains the current number of version

    def check_version(self, message, k):
        """
        Compares the current version to a version sent in a message
        :param message: a received message (id_number, ld, md)
        :type message: Tuple
        :param k: the number of the fragment to check in ld and md
        :type k: Int
        :return: 1 if the current version is lower, 0 if it is the same, -1 if it is higher
        :rtype: Int
        """
        if self.ld[k] == message[1][k]:
            return 0
        elif self.ld[k] == True and message[1][k] == False:
            return -1
        elif self.ld[k] == False and message[1][k] == True:
            return 1

    def send_message(self):
        # Sends a message with the current version to neighbouring nodes
        for recipient in neighbors[self.id_number]:
            recipient.messages.append(self.id_number, self.ld, self.md)

    def act(self, t):
        # Acts according to the time t
        if t == 0:
            # Reset c and tau if t = 0
            self.c = 0
            self.tau = random()*self.i/2 + self.i/2

        if t == self.tau and self.c < self.k:
            # at time tau, if c < k, send our version to neighbouring
            self.send_message()

        # check if any version received in messages is different from the current one
        version_change = True

        while len(self.messages) > 0:
            # check the messages, if the current version is lower, update; if it is higher, send it to neighbouring nodes
            message = self.messages.pop()
            for k in range(n_fragments):
                check = self.check_version(message, k)
                if check == 0:
                    self.c += 1
                elif check == -1:
                    version_change = False
                    self.send_message()
                elif check == 1:
                    version_change = False
                    self.ld[k] = message[1][k]
                    self.md[k] = message[2][k]

        if t > self.i:
            if version_change == True:
                # if a version was different, extend i
                self.i = self.i*2
            else:
                # if not, reset i and c
                self.i = self.i_min
                self.c = 0


nodes = [Node(0, 0, 10, 2, 5, 100, 0, [], [True, True], [1, 1]),
         Node(1, 0, 10, 2, 5, 100, 0, [], [False, False], [2, 2])]

nodes[1].messages = [(0, nodes[0].ld, nodes[0].md)]

t = 2
n_nodes = 2
n_fragments = 2
neighbors = {0: [1], 1: [0]}

nodes[1].act(t)
print(nodes[1].md)