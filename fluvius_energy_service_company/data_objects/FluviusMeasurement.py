

class FluviusMeasurement:

    def __init__(self, unit: str, offtake_value: float, offtake_validation_state: str, injection_value: float,
                 injection_validation_state: str):
        self.unit = unit
        self.offtake_value = offtake_value
        self.offtake_validation_state = offtake_validation_state
        self.injection_value = injection_value
        self.injection_validation_state = injection_validation_state

    def __eq__(self, other):
        if not isinstance(other, FluviusMeasurement):
            return NotImplemented
        return (self.unit, self.offtake_value, self.offtake_validation_state,
                self.injection_value, self.injection_validation_state) == \
               (other.unit, other.offtake_value, other.offtake_validation_state,
                other.injection_value, other.injection_validation_state)

    def __hash__(self):
        return hash((self.unit, self.offtake_value, self.offtake_validation_state,
                     self.injection_value, self.injection_validation_state))

    def get_offtake_array(self):
        return [self.offtake_value]

    def get_injection_array(self):
        return [self.injection_value]
