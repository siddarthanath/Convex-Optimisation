"""
This file stores datamodels needed through the optimization frameworks.
"""

# -------------------------------------------------------------------------------------------------------------------- #
# Standard Library
from typing import List, Tuple, Dict

# Third Party
import numpy as np

# Private Party
from src.utils.datamodels import LinearExpression
from src.utils.enum import InequalityType
from src.linear_programming.methods import solve_scipy, solve_cvxopt


# -------------------------------------------------------------------------------------------------------------------- #


class LinearProgrammingProblem:
    """
    Represents a linear programming problem with an objective function and a list of constraints.

    Parameters
    ----------
    objective : LinearExpression
        The objective function to be optimized.
    constraints : List[LinearExpression]
        A list of constraints for the linear programming problem.
    """

    def __init__(
        self, objective: LinearExpression, constraints: List[LinearExpression]
    ):
        self.objective = objective
        self.constraints = constraints
        self.variables = self._get_variable_names()

    def _get_variable_names(self):
        """
        Extracts all variable names used in the objective function and constraints.

        Returns
        -------
        List[str]
            A list of variable names.
        """
        variable_names = set(self.objective.coefficients.keys())
        for constraint in self.constraints:
            variable_names.update(constraint.coefficients.keys())
        return sorted(list(variable_names))

    def solve(self, method="simplex", lib_type="scipy"):
        """
        Solves the linear programming problem using the specified method.

        Parameters
        ----------
        method : str
            The method to be used for solving the problem.
            Choices are 'auto', 'simplex', or 'interior-point'.
            Default is 'auto', which uses the default method.
        lib_type : str
            The type of execution e.g. scipy, cvxopt or manual.

        Returns
        -------
        Solution
            The solution of the linear programming problem.
        """
        if lib_type == "scipy":
            return solve_scipy(method, **self._convert_to_matrices())
        elif lib_type == "cvxopt":
            return solve_cvxopt(**self._convert_to_matrices())
        else:
            raise ValueError(
                "Invalid type specified. Choose 'scipy', 'cvxopt', or 'manual'."
            )

    def _convert_to_matrices(
        self,
    ) -> Dict:
        """
        Converts the objective function and constraints into the matrices and vectors required by the linprog function.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[Tuple[float, float]]]
            Matrices and vectors required by the linprog function.
        """
        # Get the number of variables
        num_vars = len(self.variables)
        # Extract coefficients and constant terms from the objective function
        c = np.array(
            [self.objective.coefficients.get(var, 0.0) for var in self.variables]
        )
        # Initialise matrices and vectors for constraints
        A_ub = []
        b_ub = []
        A_eq = []
        b_eq = []
        # Bounds for the decision variables (assume non-negativity by default)
        bounds = [(0, None)] * num_vars
        # Extract coefficients and constant terms from the constraints
        for constraint in self.constraints:
            coefficients = [
                constraint.coefficients.get(var, 0.0) for var in self.variables
            ]
            constant = constraint.constant_term
            if constraint.type == InequalityType.LESS_THAN_EQUAL:
                A_ub.append(coefficients)
                b_ub.append(constant)
            elif constraint.type == InequalityType.GREATER_THAN_EQUAL:
                A_ub.append([-coef for coef in coefficients])
                b_ub.append(-constant)
            elif constraint.type == InequalityType.EQUAL:
                A_eq.append(coefficients)
                b_eq.append(constant)
        # Convert lists to numpy arrays
        A_ub = np.array(A_ub)
        b_ub = np.array(b_ub)
        A_eq = np.array(A_eq)
        b_eq = np.array(b_eq)
        return {
            "c": c,
            "A_ub": A_ub,
            "b_ub": b_ub,
            "A_eq": A_eq,
            "b_eq": b_eq,
            "bounds": bounds,
        }


__all__ = ["LinearProgrammingProblem"]
