import copy


class Coefficient:
    """
    An imaginary or real coefficient.
    """
    
    def __init__(self, magnitude=0.00, imaginary=False):
        """
        Initializes a coefficient.

        :param magnitude: The coefficient's magnitude.
        :param imaginary: Whether the coefficient is imaginary.
        """
        self.set_magnitude(magnitude)
        if imaginary == True:
            self.set_imaginary()
        else:
            self.clear_imaginary()
        
    def equals(self, other):
        """
        Checks whether the coefficient is equal to another.

        :param other: The other coefficient.
        :raises: ValueError
        """
        if isinstance(other, Coefficient):
            return (self.magnitude == other.get_magnitude()) and (self.imaginary == other.get_imaginary())
        elif isinstance(other, ComplexCoefficient) and self.imaginary == False:
            return self.magnitude == other.get_real_component().get_magnitude() \
                and (other.get_imaginary_component().get_magnitude() == 0)
        elif isinstance(other, ComplexCoefficient) and self.imaginary == True:
            return self.magnitude == other.get_imaginary_component().get_magnitude() \
                and (other.get_real_component().get_magnitude() == 0)
        else:
            raise ValueError("equating coefficient to object of incorrect type was attempted")
    
    def add(self, other):
        """
        Adds the coefficient to another.

        :param other: The other coefficient.
        :raises: ValueError
        """
        if isinstance(other, Coefficient):
            if other.get_imaginary() == self.imaginary:
                new_imaginary = copy.deepcopy(self.imaginary)
                new_magnitude = self.magnitude + other.get_magnitude()
                return Coefficient(magnitude=new_magnitude, imaginary=new_imaginary)
            elif self.imaginary == False and other.get_imaginary() == True:
                return ComplexCoefficient(real_component=self, imaginary_component=other)
            elif self.imaginary == True and other.get_imaginary() == False:
                return ComplexCoefficient(real_component=other, imaginary_component=self)
        elif isinstance(other, ComplexCoefficient):
            if self.imaginary == True:
                new_imaginary_component = other.get_imaginary_component() + self
                result = copy.deepcopy(other)
                result.set_imaginary_component(new_imaginary_component)
                return result
            elif self.imaginary == False:
                new_real_component = other.get_real_component().add(self)
                result = copy.deepcopy(other)
                result.set_real_component(new_real_component)
                return result
        else:
            raise ValueError("adding coefficient to object of incorrect type was attempted")

    def multiply(self, other):
        """
        Multiplies the coefficient by another.

        :param other: The other coefficient.
        :raises: ValueError
        """
        if isinstance(other, Coefficient):
            if other.get_imaginary() == self.imaginary:
                new_imaginary = False
                new_magnitude = self.magnitude * other.get_magnitude()
                new_coeff = Coefficient(magnitude=new_magnitude, imaginary=new_imaginary)
                if self.imaginary:
                    new_coeff.negate_magnitude()
                return new_coeff
            elif self.imaginary != other.get_imaginary():
                new_imaginary = True
                new_magnitude = self.magnitude * other.get_magnitude()
                return Coefficient(magnitude=new_magnitude, imaginary=new_imaginary)
        elif isinstance(other, ComplexCoefficient):
            new_imaginary_component = other.get_imaginary_component().multiply(self)
            new_real_component = other.get_real_component().multiply(self)
            result = copy.deepcopy(other)
            result.set_imaginary_component(new_imaginary_component)
            result.set_real_component(new_real_component)
            return result
        else:
            raise ValueError("adding coefficient to object of incorrect type was attempted")

    def get_magnitude(self):
        """
        Gets the magnitude of the coefficient.

        :return: The coefficient's magnitude.
        """
        return self.magnitude
    
    def get_imaginary(self):
        """
        Whether the coefficient is imaginary or real.

        :return: Whether the coefficient is imaginary.
        """
        return self.imaginary
            
    def set_magnitude(self, magnitude):
        """
        Sets the magnitude of the coefficient.

        :param magnitude: The new magnitude.
        :raises: ValueError
        """
        if isinstance(magnitude, float):
            self.magnitude = magnitude
        else:
            raise ValueError("setting magnitude to value of incorrect type was attempted")
            
    def set_imaginary(self):
        """
        Makes this coefficient imaginary.
        """
        self.imaginary = True
            
    def clear_imaginary(self):
        """
        Makes this coefficient real.
        """
        self.imaginary = False
            
    def negate_magnitude(self):
        """
        Negates the coefficient.
        """
        self.magnitude = -self.magnitude
    
    def multiply_by_i(self):
        """
        Multiplies the coefficient by i.
        """
        if self.imaginary:
            self.negate_magnitude()
            self.clear_imaginary()
        elif not self.imaginary == True:
            self.set_imaginary()
            
    def multiply_by_number(self, number):
        """
        Multiplies the coefficient by a number.

        :param number: The number to multiply the coefficient by.
        :raises: ValueError
        """
        if isinstance(number, float):
            self.magnitude = self.magnitude*number
        else:
            raise ValueError("multiplying coefficient by value of incorrect type was attempted")
            
    def to_probability(self):
        """
        Determines the probabilistic weight of the coefficient.

        :return: The coefficient's probabilistic weight.
        """
        return self.magnitude**2
    
    def complex_conjugate(self):
        """
        Takes the complex conjugate of the coefficient in place.
        """
        if self.imaginary == True:
            self.negate_magnitude()

    def print(self):
        """
        Prints the coefficient.
        """
        print(" {0} {1}{2:.3f}".format('-' if self.get_magnitude() < 0 else '+', 'i' if self.get_imaginary() else '', abs(self.get_magnitude())), end='')
        
        
class ComplexCoefficient:
    """
    A complex coefficient.
    """

    def __init__(self, real_component=None, imaginary_component=None):
        """
        Initializes a complex coefficient with optional real and imaginary components.

        :param real_component: The real component.
        :param imaginary_component: The imaginary component.
        """
        if isinstance(real_component, Coefficient):
            self.set_real_component(real_component)
        if isinstance(imaginary_component, Coefficient):
            self.set_imaginary_component(imaginary_component)
        
    def equals(self, other):
        """
        Checks if the coefficient is equal to another.

        :param other: The other coefficient.
        :raises: ValueError
        """
        if isinstance(other, ComplexCoefficient):
            return (self.real_component.equals(other.get_real_component())) and (self.imaginary_component.equals(other.get_imaginary_component()))
        elif isinstance(other, Coefficient):
            if other.get_imaginary() == True:
                return (self.real_component.get_magnitude() == 0) and (self.imaginary_component.get_magnitude() == other.get_magnitude())
            elif other.get_imaginary() == False:
                return (self.imaginary_component.get_magnitude() == 0) and (self.real_component.get_magnitude() == other.get_magnitude())
        else:
            raise ValueError("equating complex coefficient to object of incorrect type was attempted")
    
    def add(self, other):
        """
        Adds the coefficient to another.

        :param other: The other coefficient.
        :raises: ValueError
        """
        if isinstance(other, ComplexCoefficient):
            new_imaginary_component = other.get_imaginary_component().add(self.imaginary_component)
            new_real_component = self.real_component.add(other.get_real_component())
            return ComplexCoefficient(real_component=new_real_component, imaginary_component=new_imaginary_component)
        elif isinstance(other, Coefficient):
            if other.get_imaginary() == True:
                new_imaginary_component = other.add(self.imaginary_component)
                return ComplexCoefficient(real_component=self.real_component, imaginary_component=new_imaginary_component)
            elif other.get_imaginary() == False:
                new_real_component = other.add(self.real_component)
                return ComplexCoefficient(real_component=new_real_component, imaginary_component=self.imaginary_component)
        else:
            raise ValueError("adding a complex coefficient with an object of incorrect type was attempted")

    def multiply(self, other):
        """
        Multiplies the coefficient by another.

        :param other: The other coefficient.
        :raises: ValueError
        """
        if isinstance(other, ComplexCoefficient):
            new_imaginary_component = other.get_real_component().multiply(self.imaginary_component).add(other.get_imaginary_component().multiply(self.real_component))
            new_real_component = other.get_real_component().multiply(self.real_component).add(other.get_imaginary_component().multiply(self.imaginary_component))
            return ComplexCoefficient(real_component=new_real_component, imaginary_component=new_imaginary_component)
        elif isinstance(other, Coefficient):
            return other.multiply(self)
        else:
            raise ValueError("adding a complex coefficient with an object of incorrect type was attempted")

    def get_real_component(self):
        """
        Gets the complex coefficient's real component.

        :return: The real component.
        """
        return self.real_component
    
    def get_imaginary_component(self):
        """
        Gets the complex coefficient's imaginary component.

        :return: The imaginary component.
        """
        return self.imaginary_component
            
    def set_real_component(self, real_component=None):
        """
        Sets the real component of the complex coefficient.

        :param real_component: The new real component.
        :raises: ValueError
        """
        if isinstance(real_component, Coefficient) and real_component.get_imaginary() == False:
            self.real_component = real_component
        else:
            raise ValueError("setting real component to value of incorrect type was attempted")
            
    def set_imaginary_component(self, imaginary_component=None):
        """
        Sets the imaginary component of the complex coefficient.

        :param imaginary_component: The new imaginary component.
        :raises: ValueError
        """
        if isinstance(imaginary_component, Coefficient) and imaginary_component.get_imaginary() == True:
            self.imaginary_component = imaginary_component
        else:
            raise ValueError("setting imaginary component to value of incorrect type was attempted")
    
    def negate_magnitude(self):
        """
        Negates the coefficient.
        """
        self.real_component.negate_magnitude()
        self.imaginary_component.negate_magnitude()
    
    def multiply_by_i(self):
        """
        Multiplies the coefficient by i.
        """
        new_real_component = copy.deepcopy(self.imaginary_component)
        new_real_component.clear_imaginary()
        new_real_component.negate_magnitude()
        new_imaginary_component = copy.deepcopy(self.real_component)
        new_imaginary_component.set_imaginary()
        self.real_component = new_real_component
        self.imaginary_component = new_imaginary_component

    def multiply_by_number(self, number):
        """
        Multiplies the coefficient by a number.

        :param number: The number to multiply the coefficient by.
        :raises: ValueError
        """
        if isinstance(number, float):
            self.real_component.multiply_by_number(number)
            self.imaginary_component.multiply_by_number(number)
        else:
            raise ValueError("multiplying complex coefficient by number of incorrect type was attempted")
            
    def to_probability(self):
        """
        Determines the probabilistic weight of the coefficient.

        :return: The coefficient's probabilistic weight.
        """
        return self.real_component.get_magnitude()**2 + self.imaginary_component.get_magnitude()**2
    
    def complex_conjugate(self):
        """
        Takes the complex conjugate of the coefficient in place.
        """
        self.imaginary_component.negate_magnitude()

    def print(self):
        """
        Prints the complex coefficient.
        """
        print(" + (", end="")
        self.real_component.print()
        self.imaginary_component.print()
        print(" )", end="")
