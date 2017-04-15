import numpy as np
from gnuradio import gr

class decodHomeEasy(gr.sync_block):
    """
    docstring for block decodHomeEasy
    This block analyses the input flow recieved by the usrp, to detect if it corresponds to a valid frame of the HomeEasy protocol.
    It works as a finite-state machine with 4 states. It detects the High-Low edges.
    State 0 : Initial point, waiting for an header
    State 1 : Waiting for a bit
    State 2 : Waiting for the validation of the value '0'
    State 3 : Waiting for the validation of the value '1'
    Time margins are set in parameters.
    """

    def __init__(self, samplerate=1000000, errormargin=0.2, threshold=0.3, filterlength=4):
        """Definition of finite state machine"""
        self.compteur_changestate = 0
        self.state = 0

        """Definition of edges detection filter"""
        self.hightlow_state = False
        self.Threshold = threshold
        self.hightlow_vector = np.zeros(filterlength, dtype=np.float32)

        """Definition of output vector """
        self.vector = np.zeros(32, dtype=np.bool)
        self.indice_vector = 0
        self.enable = False

        """Definition of frame lenght depending on samplerate"""
        longtram = int(round(1660 * samplerate / 1000000))
        shorttram = int(round(575 * samplerate / 1000000))
        headerFrame = int(round(3117 * samplerate / 1000000))

        """Definition of timemargin"""
        self.headerlow = headerFrame * (1 - errormargin)
        self.headerhigh = headerFrame * (1 + errormargin)
        self.shortframelow = shorttram * (1 - errormargin)
        self.shortframehigh = shorttram * (1 + errormargin)
        self.longframelow = longtram * (1 - errormargin)
        self.longframehigh = longtram * (1 + errormargin)

        gr.sync_block.__init__(self,   name="decodHomeEasy", in_sig=[np.float32],  out_sig=[(np.bool, 32), np.bool])

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        out1 = output_items[1]
        for j in range(len(in0)):
            self.hightlow_vector[1: self.FILTERLENGTH] = self.hightlow_vector[0: self.FILTERLENGTH - 1]
            self.hightlow_vector[0] = in0[j]
            self.compteur_changestate += 1

            """Detects high_low edges """
            if (not self.hightlow_state) and np.all(self.hightlow_vector > self.Threshold):
                self.hightlow_state = True
            if self.hightlow_state and np.all(self.hightlow_vector < self.Threshold):
                self.hightlow_state = False
            if self.state == 0:
                """Waiting for a header"""
                if self.headerlow < self.compteur_changestate < self.headerhigh:
                    """If header, go to state 1"""
                    self.state = 1
            elif self.state == 1:
                """Waiting for a bit"""
                self.transmit(self.shortframelow, self.shortframehigh, 0, 2)
                self.transmit(self.shortframelow, self.shortframehigh, 1, 3)
                if self.state == 1:
                    """If not symbol 1 or 0, reset"""
                    self.vector[:] = 0
                    self.indice_vector = 0
                    self.state = 0

            elif self.state == 2:
                """Waiting for a 0 confirmation (long frame)"""
                self.confirmation(self.longframelow, self.longframehigh)
            elif self.state == 3:
                """Waiting for a 1 confirmation (short frame)"""
                self.confirmation(self.shortframelow, self.shortframehigh)
            self.compteur_changestate = 0

        """Write output buffer"""
        out0[j] = self.vector
        out1[j] = self.enable

        if self.enable:
            """If transmitted valid frame , reset """
            self.vector[:] = 0
            self.enable = False

        return len(output_items[0])

    def transmit(self, frame_size, framehigh, indice31, next_state):
        self.state = 0
        if frame_size < self.compteur_changestate < framehigh:
            if self.indice_vector == 31:
                """And if last symbol, transmit vector an reset """
                self.vector[31] = indice31
                self.enable = True
                self.indice_vector = 0
            else:
                """And if not last symbol, go to state 2"""
                self.state = next_state

    def confirmation(self, frame_size, framehigh):
        self.state = 0
        if frame_size < self.compteur_changestate < framehigh:
            """If confirmed, write 1 and go to 1"""
            self.vector[self.indice_vector] = 1
            self.indice_vector += 1
            self.state = 1
        else:
            """If not confirmed, reset"""
            self.vector[:] = 0
            self.indice_vector = 0
