"""
This file stores datamodels needed through the optimization frameworks.
"""

# -------------------------------------------------------------------------------------------------------------------- #
# Standard Library
import re
from typing import Dict, Union, Optional, List

# Third Party
from pydantic import BaseModel, Field

# Private Party
from src.utils.enum import OptimizationType, InequalityType


# -------------------------------------------------------------------------------------------------------------------- #
class LinearExpression(BaseModel):
    """
    A class to represent a linear expression.

    Attributes
    ----------
    expression : str
        The string representation of the linear expression.
    type : Union[OptimizationType, InequalityType]
        The type of the linear expression, either optimization or inequality.
    constant_term : float
        The constant term of the linear expression.
    coefficients : Dict[str, float]
        The coefficients of the variables in the linear expression.

    Methods
    -------
    __init__(self, **data)
        Initializes a LinearExpression instance.
    _set_coefficients(self)
        Sets the coefficients dictionary by parsing the expression.
    constraint_representation(self) -> Optional[str]
        Constructs a string representation of the linear constraint.
    variable_names(self) -> List[str]
        Gets the variable names of the linear expression.
    _coeff_array(self, var_order: List[str]) -> List[float]
        Converts the coefficients of the linear expression to a list.
    """

    expression: str
    type: Union[OptimizationType, InequalityType]
    constant_term: Union[int, float]
    coefficients: Dict[str, float] = Field(default_factory=dict)

    def __init__(self, **data: object):
        """
        Initializes a LinearExpression instance.

        Parameters
        ----------
        data : dict
            The data to initialize the instance with.
        """
        super().__init__(**data)
        self._set_coefficients()

    def _set_coefficients(self):
        """
        Sets the coefficients dictionary by parsing the expression.
        """
        term_regex = re.compile(r"([+-]?\d*\.?\d*)([a-zA-Z]+)")
        coefficients = {}
        for term, variable in term_regex.findall(self.expression):
            coefficients[variable] = float(term) if term else 1.0
        self.coefficients = coefficients

    def constraint_representation(self) -> Optional[str]:
        """
        Constructs a string representation of the linear constraint.

        Returns
        -------
        Optional[str]
            The string representation of the linear constraint, or None if the type is not an inequality.
        """
        if self.type in [InequalityType.LESS_THAN, InequalityType.GREATER_THAN]:
            terms = []
            for variable, coefficient in self.coefficients.items():
                if coefficient == 1:
                    terms.append(variable)
                else:
                    terms.append(f"{coefficient}{variable}")
            if self.constant_term:
                terms.append(str(self.constant_term))
            expression_str = " + ".join(terms)
            inequality_symbol = (
                ">=" if self.type == InequalityType.GREATER_THAN else "<="
            )
            return f"{expression_str} {inequality_symbol} {self.constant_term}"
        return None

    def variable_names(self) -> List[str]:
        """
        Gets the variable names of the linear expression.

        Returns
        -------
        List[str]
            The variable names of the linear expression.
        """
        return list(self.coefficients.keys())

    def _coeff_array(self, var_order: List[str]) -> List[float]:
        """
        Converts the coefficients of the linear expression to a list.

        Parameters
        ----------
        var_order : List[str]
            The ordered list of variable names.

        Returns
        -------
        List[float]
            The coefficients of the linear expression in the order specified.
        """
        return [self.coefficients.get(var, 0.0) for var in var_order]
