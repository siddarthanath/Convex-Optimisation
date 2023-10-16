"""
This file creates methods for the Linear Programming class.
"""

# -------------------------------------------------------------------------------------------------------------------- #
# Standard Library

# Third Party
from scipy.optimize import linprog
from cvxopt.solvers import lp
from cvxopt import matrix

# Private Party


# -------------------------------------------------------------------------------------------------------------------- #


def solve_scipy(method: str, **kwargs):
    """
    Solves the linear programming problem using the scipy library.

    Parameters
    ----------
    method : str
        The method to be used for solving the problem.
        Choices are 'auto', 'simplex', or 'interior-point'.
        Default is 'auto', which uses the default method.
    kwargs: dict
        Dictionary containing the variables needed in linprog library.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the solution of the optimization problem.
    """
    return linprog(**kwargs, method=method)


def solve_cvxopt(**kwargs):
    """
    Solves the linear programming problem using the scipy library.

    Parameters
    ----------
    kwargs: dict
        Dictionary containing the variables needed in cvxopt library.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the solution of the optimization problem.
    """
    # Change letters
    c = matrix(kwargs["c"])
    G = matrix(kwargs["A_ub"])
    h = matrix(kwargs["b_ub"])
    A = matrix(kwargs["A_eq"])
    b = matrix(kwargs["b_eq"])
    return lp(c, -G, -h, A, b)
