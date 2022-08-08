import numpy as np
from numpy.ma import cos, sin


class Force3D:
    """Set moment and force vector on space point."""

    def __init__(self, force, position=None, orientation_dependent=True):
        if position is None:
            position = [0, 0, 0]
        self.vect = np.array(force)
        self.location = np.array(position)
        self.orientation_dependent = orientation_dependent

    @property
    def magnitude(self) -> float:
        """Magnitude of the force.

        Returns
        -------
        float
            _description_
        """
        return np.linalg.norm(self.vect)

    def moment_around(self, r_vect):
        """Moment around a point.

        Parameters
        ----------
        r_vect : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return np.cross((self.location - r_vect), self.vect)

    def in_frame(self, rotation_matrix: np.ndarray):
        """_summary_.

        Parameters
        ----------
        rotation_matrix : np.ndarray
            _description_

        Returns
        -------
        _type_
            _description_
        """
        if self.orientation_dependent:
            return (rotation_matrix @ self.vect[np.newaxis].T).reshape((3,))
        else:
            return self.vect

    def moment_in_frame(self, r_vect: np.ndarray, rotation_matrix: np.ndarray):
        """_summary_.

        Parameters
        ----------
        r_vect : np.ndarray
            _description_
        rotation_matrix : np.ndarray
            _description_

        Returns
        -------
        _type_
            _description_
        """
        if self.orientation_dependent:
            return (rotation_matrix @ self.moment_around(r_vect)[np.newaxis].T).reshape((3,))
        else:
            return self.moment_around(r_vect)

    def __eq__(self, other):
        if not type(self) == type(other):
            return False
        return np.array_equal(other.vect, self.vect) and np.array_equal(other.location, self.location)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Force {self.vect}, Position {self.location}"


class TimeVaryingForce(Force3D):
    """_summary_.

    Parameters
    ----------
    Force3D : _type_
        _description_
    """

    def __init__(self, func, position=None, orientation_dependent=None):
        super().__init__(func(0), position, orientation_dependent)
        self.function = func

    def update(self, time):
        """_summary_.

        Parameters
        ----------
        time : _type_
            _description_
        """
        self.vect = np.array(self.function(time))

    def __repr__(self):
        return f"Time Varying force currently {self.vect} at {self.location}"


def rotation_quaternion(angle: float, axis: np.ndarray):
    """_summary_.

    Parameters
    ----------
    angle : float
        _description_
    axis : np.ndarray
        _description_

    Returns
    -------
    _type_
        _description_
    """
    if not np.array_equal([0, 0, 0], axis):
        axis = axis / np.linalg.norm(axis)
    a = sin(angle / 2)
    return np.quaternion(cos(angle / 2), a * axis[0], a * axis[1], a * axis[2])


class Moment(Force3D):
    """_summary_.

    Parameters
    ----------
    Force3D : _type_
        _description_
    """

    def __init__(self, moment, orientation_dependent=False):
        super().__init__([0, 0, 0], orientation_dependent=orientation_dependent)
        self.moment = moment

    def moment_around(self, r_vect):
        """_summary_.

        Parameters
        ----------
        r_vect : _type_
            vector

        Returns
        -------
        _type_
            _moment
        """
        return self.moment
